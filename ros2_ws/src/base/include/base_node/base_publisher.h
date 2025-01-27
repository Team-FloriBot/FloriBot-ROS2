#ifndef KINEMATICS_PUBLISHER_H
#define KINEMATICS_PUBLISHER_H

#include "drives/articulated_drive.h"
#include <rclcpp/rclpcpp.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_ros/transform_listener.h>
#include <tf2/LinearMath/Quaternion.h>
#include <geometry_msgs/pose_stamped.h>
#include <base/angle.hpp>
#include <nav_msgs/odometry.h>

#include <base/wheels.hpp>

class KinematicsPublisher : public rclcpp::Node  // Vererbung von rclcpp::Node statt ros::NodeHandle
{
public:
    KinematicsPublisher(std::shared_ptr<rclcpp::Node> pnh, kinematics::coordinate Base);
    ~KinematicsPublisher();

private:
    void getParam();
    void createPublisherSubscriber();    
    void PublishSpeed(const rclcpp::TimerBase::SharedPtr e);  // TimerEvent in ROS2 ist TimerBase::SharedPtr
    void CmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg);  // Änderung zu SharedPtr
    void SpeedCallback(const base::Wheels::SharedPtr msg);  // Änderung zu SharedPtr

    kinematics::ArticulatedDrive Drive_;
    base::Wheels Speedmsg_;
    std::shared_ptr<rclcpp::Node> pNh_;  // NodeHandle wird durch Node ersetzt und als shared_ptr verwendet
    rclcpp::TimerBase::SharedPtr CmdVelTimer_;  // Timer-Typen haben sich geändert
    rclcpp::Publisher<base::Wheels>::SharedPtr SpeedPublisher_, OdometryPublisher_;  // Publisher-Typ geändert
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr CmdVelSubscriber_, SpeedSubscriber_;  // Subscriber-Typ geändert
    tf2_ros::TransformBroadcaster TFBroadaster_;
    double AxesLength_, WheelDiameter_;
    unsigned int seq_;
};

#endif
