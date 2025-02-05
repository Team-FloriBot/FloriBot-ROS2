#ifndef KINEMATICS_PUBLISHER_H
#define KINEMATICS_PUBLISHER_H

#include "drives/articulated_drive.h"
#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_ros/transform_listener.h>
#include <tf2/LinearMath/Quaternion.h>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <base/msg/angle.hpp>
#include <nav_msgs/msg/odometry.hpp>

#include <base/msg/wheels.hpp>

class KinematicsPublisher : public rclcpp::Node  // Vererbung von rclcpp::Node statt ros::NodeHandle
{
public:
    KinematicsPublisher(kinematics::coordinate Base);
    ~KinematicsPublisher();

private:
    void getParam();
    void createPublisherSubscriber();    
    void PublishSpeed();  // TimerEvent in ROS2 ist TimerBase::SharedPtr
    void CmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg);  // Änderung zu SharedPtr
    void SpeedCallback(const base::msg::Wheels::SharedPtr msg);  // Änderung zu SharedPtr

    kinematics::ArticulatedDrive Drive_;
    base::msg::Wheels Speedmsg_;
    //std::shared_ptr<rclcpp::Node> pNh_;  // NodeHandle wird durch Node ersetzt und als shared_ptr verwendet
    
    rclcpp::TimerBase::SharedPtr CmdVelTimer_;  // Timer-Typen haben sich geändert
    rclcpp::Publisher<base::msg::Wheels>::SharedPtr SpeedPublisher_;  // Publisher-Typ geändert
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr OdometryPublisher_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr CmdVelSubscriber_;  // Subscriber-Typ geändert
    rclcpp::Subscription<base::msg::Wheels>::SharedPtr SpeedSubscriber_;

    std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadaster_;
    double AxesLength_, WheelDiameter_;
    
};

#endif
