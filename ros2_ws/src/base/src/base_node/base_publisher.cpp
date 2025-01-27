#include "base_node/base_publisher.hpp"
#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <base/msg/wheels.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/transform_broadcaster.hpp>
#include <tf2_ros/buffer.hpp>
#include <tf2_ros/transform_listener.hpp>
#include <memory>

KinematicsPublisher::KinematicsPublisher(rclcpp::Node::SharedPtr node, kinematics::coordinate Base)
{
    seq_ = 0;
    pNh_ = node;

    getParam();
    Drive_.setParam(AxesLength_, WheelDiameter_, Base);
    createPublisherSubscriber();
    CmdVelTimer_ = node->create_wall_timer(std::chrono::milliseconds(100), std::bind(&KinematicsPublisher::PublishSpeed, this));
}

KinematicsPublisher::~KinematicsPublisher() {}

void KinematicsPublisher::PublishSpeed()
{
    base::Wheels tmp;

    tmp.header.stamp = pNh_->get_clock()->now();
    tmp.header.seq = seq_++;
    tmp.front_left = Speedmsg_.front_left;
    tmp.front_right = Speedmsg_.front_right;
    tmp.rear_left = Speedmsg_.rear_left;
    tmp.rear_left = Speedmsg_.rear_right;

    SpeedPublisher_->publish(Speedmsg_);

    Speedmsg_.front_left = 0;
    Speedmsg_.front_right = 0;
    Speedmsg_.rear_right = 0;
    Speedmsg_.rear_left = 0;
}

void KinematicsPublisher::getParam()
{
    pNh_->get_parameter_or("/" + pNh_->get_name() + "/axesLength", AxesLength_, 0.4);
    pNh_->get_parameter_or("/" + pNh_->get_name() + "/wheelDiameter", WheelDiameter_, 0.4);
}

void KinematicsPublisher::createPublisherSubscriber()
{
    OdometryPublisher_ = pNh_->create_publisher<nav_msgs::msg::Odometry>("/odom", 1);
    SpeedPublisher_ = pNh_->create_publisher<base::msg::Wheels>("engine/targetSpeed", 1);

    CmdVelSubscriber_ = pNh_->create_subscription<geometry_msgs::msg::Twist>(
        "cmd_vel", 1, std::bind(&KinematicsPublisher::CmdVelCallback, this, std::placeholders::_1));

    SpeedSubscriber_ = pNh_->create_subscription<base::msg::Wheels>(
        "engine/actualSpeed", 1, std::bind(&KinematicsPublisher::SpeedCallback, this, std::placeholders::_1));
}

void KinematicsPublisher::CmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg)
{
    kinematics::articulatedWheelSpeed Wheelspeed;

    Wheelspeed = Drive_.inverseKinematics(*msg);

    Speedmsg_.front_left = Wheelspeed.Front.leftWheel;
    Speedmsg_.front_right = Wheelspeed.Front.rightWheel;

    Speedmsg_.rear_left = Wheelspeed.Rear.leftWheel;
    Speedmsg_.rear_right = Wheelspeed.Rear.rightWheel;
}

void KinematicsPublisher::SpeedCallback(const base::msg::Wheels::SharedPtr msg)
{
    kinematics::articulatedWheelSpeed ActualSpeed;
    geometry_msgs::msg::Pose2D OdomPose;
    geometry_msgs::msg::TransformStamped Transform;
    nav_msgs::msg::Odometry OdomMsg;
    tf2::Quaternion q;

    ActualSpeed.Front.leftWheel = msg->front_left;
    ActualSpeed.Front.rightWheel = msg->front_right;
    ActualSpeed.Rear.leftWheel = msg->rear_left;
    ActualSpeed.Rear.rightWheel = msg->rear_right;

    OdomPose = Drive_.forwardKinematics(ActualSpeed, msg->header.stamp);

    // Front Msg
    q.setRPY(0, 0, OdomPose.theta);

    // TF Msg
    Transform.child_frame_id = "base_link";
    Transform.header.frame_id = "odom";
    Transform.header.seq = msg->header.seq;
    Transform.header.stamp = msg->header.stamp;

    Transform.transform.translation.x = OdomPose.x;
    Transform.transform.translation.y = OdomPose.y;
    Transform.transform.translation.z = WheelDiameter_ / 2;

    Transform.transform.rotation.w = q.getW();
    Transform.transform.rotation.x = q.getX();
    Transform.transform.rotation.y = q.getY();
    Transform.transform.rotation.z = q.getZ();

    // ToDo: Add Covariance
    // Odom Msg
    OdomMsg.child_frame_id = "base_link";
    OdomMsg.header.frame_id = "odom";
    OdomMsg.header.seq = msg->header.seq;
    OdomMsg.header.stamp = msg->header.stamp;

    OdomMsg.pose.pose.orientation.w = q.getW();
    OdomMsg.pose.pose.orientation.x = q.getX();
    OdomMsg.pose.pose.orientation.y = q.getY();
    OdomMsg.pose.pose.orientation.z = q.getZ();

    OdomMsg.pose.pose.position.x = OdomPose.x;
    OdomMsg.pose.pose.position.y = OdomPose.y;
    OdomMsg.pose.pose.position.z = WheelDiameter_ / 2;

    // According to http://wiki.ros.org/navigation/Tutorials/RobotSetup/Odom the speed has to be in the child_frame
    // in our case base_link which means the robot itself

    OdomMsg.twist.twist = Drive_.getSpeed();

    // publish
    OdometryPublisher_->publish(OdomMsg);

    TFBroadaster_.sendTransform(Transform);
}

