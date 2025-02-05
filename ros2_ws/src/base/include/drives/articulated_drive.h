#ifndef ARTICULATED_DRIVE_H
#define ARTICULATED_DRIVE_H

#include "drives/differential_drive.h"
#include <rclcpp/rclcpp.hpp>  // ROS2 Header für Node und Zeit

#include <rclcpp/time.hpp>
#include <geometry_msgs/msg/twist.hpp>  // ROS2 Nachricht
#include <geometry_msgs/msg/pose2_d.hpp>  // ROS2 Nachricht
#include <geometry_msgs/msg/transform_stamped.hpp>  // ROS2 Nachricht
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>


namespace kinematics

{

struct articulatedWheelSpeed
{
    DifferentialWheelSpeed Front, Rear;
};

enum coordinate
{
    Front,
    Rear,
    JointFront,
    JointRear
};

class ArticulatedDrive
{
    public:
    ArticulatedDrive();
    ArticulatedDrive(double axesLength, double wheelDiameter, coordinate Base);
    ~ArticulatedDrive();

    articulatedWheelSpeed inverseKinematics(geometry_msgs::msg::Twist cmdVelMsg);
    geometry_msgs::msg::Pose2D forwardKinematics(articulatedWheelSpeed WheelSpeed, rclcpp::Time Timestamp);
    geometry_msgs::msg::Pose2D getActualPose(coordinate Frame);
    geometry_msgs::msg::Twist getSpeed();

    void setParam(double AxesLength, double WheelDiameter, coordinate Base);
    private:
    std::shared_ptr<rclcpp::Clock> clock_;
    std::unique_ptr<tf2_ros::Buffer> tf_buffer_;
    std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};
    kinematics::coordinate Base_;
    kinematics::differentialDrive frontDrive_, rearDrive_;
    double frontlength_, rearlength_;
};
}
#endif

