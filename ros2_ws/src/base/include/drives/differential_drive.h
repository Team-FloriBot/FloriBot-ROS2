#ifndef DIFFERENTIAL_DRIVE_H
#define DIFFERENTIAL_DRIVE_H

#include <rclcpp/rclcpp.hpp>  // ROS2 Header für Node und Zeit
#include <geometry_msgs/msg/twist.hpp>  // ROS2 Nachricht
#include <geometry_msgs/msg/pose2_d.hpp>  // ROS2 Nachricht
#include <cmath>  // Für mathematische Operationen (Math.h zu cmath)

#include <tf2_ros/transform_listener.h>
#include <base/msg/wheels.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <stdexcept>

namespace kinematics
{
    struct DifferentialWheelSpeed
    {
        double leftWheel;
        double rightWheel;
    };

    class differentialDrive
    {
    public:
        differentialDrive(double axesLength, double wheelDiameter);
        differentialDrive();
        ~differentialDrive();

        DifferentialWheelSpeed inverseKinematics(geometry_msgs::msg::Twist cmdVelMsg);  // Änderung zu ROS2 Nachricht
        geometry_msgs::msg::Pose2D forwardKinematics(DifferentialWheelSpeed WheelSpeed, rclcpp::Time Timestamp);  // Änderung zu ROS2 Zeit
        geometry_msgs::msg::Pose2D getActualPose();
        geometry_msgs::msg::Twist getSpeed();

        void reset();
        void setParam(double axesLength, double wheelDiameter);

    private:
        geometry_msgs::msg::Pose2D Pose_;  // Änderung zu ROS2 Nachricht
        DifferentialWheelSpeed WheelSpeed_;
        geometry_msgs::msg::Twist Speed_;  // Änderung zu ROS2 Nachricht
        rclcpp::Time TimeStamp_;  // Änderung zu ROS2 Zeit
        double axesLength_, wheelDiameter_, wheelCircumference_, wheelRadius_;
    };
} 

#endif

