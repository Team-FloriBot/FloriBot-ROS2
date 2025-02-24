#include "drives/articulated_drive.h"
#include <rclcpp/rclcpp.hpp>
#include <rclcpp/time.hpp>
#include <tf2_ros/transform_listener.h>
#include <geometry_msgs/msg/twist.hpp>
#include <geometry_msgs/msg/pose2_d.hpp>
#include <base/msg/wheels.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <stdexcept>

// Konstruktoren
// ----------------------
kinematics::ArticulatedDrive::ArticulatedDrive()
{
    clock_ = std::make_shared<rclcpp::Clock>(RCL_SYSTEM_TIME);
    tf_buffer_ = std::make_unique<tf2_ros::Buffer>(clock_);
    tf_listener_= std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
}
kinematics::ArticulatedDrive::ArticulatedDrive(double axesLength, double wheelDiameter, coordinate Base):
        frontDrive_(axesLength, wheelDiameter), rearDrive_(axesLength, wheelDiameter), Base_(Base)
        {
            clock_ = std::make_shared<rclcpp::Clock>(RCL_SYSTEM_TIME);
            tf_buffer_ = std::make_unique<tf2_ros::Buffer>(clock_);
            tf_listener_= std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
        }


kinematics::ArticulatedDrive::~ArticulatedDrive() {}

// Inverse Kinematic
// ----------------------
kinematics::articulatedWheelSpeed kinematics::ArticulatedDrive::inverseKinematics(geometry_msgs::msg::Twist cmdVelMsg)
{
    articulatedWheelSpeed retVal;
    geometry_msgs::msg::Twist FrontMsg, RearMsg;
    geometry_msgs::msg::TransformStamped Axes2Joint, Joint2Joint, Joint2Axes;

    tf2::Vector3 SpeedAxesFront, SpeedJointFront, SpeedJointRear, SpeedAxesRear;
    tf2::Vector3 OmegaFront, OmegaRear;
    tf2::Vector3 TranslationFront, TranslationRear;
    tf2::Quaternion Rotation;


    //Calculate Speeds for the two differential drives regarding the base frame
    try
    {
        switch (Base_)
        {
        //Front Speed is given
        case coordinate::Front:
            //Get latest Transforms
            Axes2Joint=tf_buffer_->lookupTransform("jointFront", "axesFront", rclcpp::Time(0));
            Joint2Joint=tf_buffer_->lookupTransform("jointRear", "jointFront", rclcpp::Time(0));
            Joint2Axes=tf_buffer_->lookupTransform("axesRear", "jointRear", rclcpp::Time(0));

            // Vektor für Frontaxengeschwindigkeit
            SpeedAxesFront.setValue(cmdVelMsg.linear.x,cmdVelMsg.linear.y,cmdVelMsg.linear.z);
            //Vektor für Frontdrehgeschwindigkeit
            OmegaFront.setValue(cmdVelMsg.angular.x,cmdVelMsg.angular.y,cmdVelMsg.angular.z);
            
            //Vektor für Fronttranslation
            TranslationFront.setValue(-Axes2Joint.transform.translation.x, -Axes2Joint.transform.translation.y, -Axes2Joint.transform.translation.z);
            //Vektor für Reartranslation
            TranslationRear.setValue(-Joint2Axes.transform.translation.x, -Joint2Axes.transform.translation.y, -Joint2Axes.transform.translation.z);
            
            //Quaternion für die Rotation
            Rotation.setValue(Joint2Joint.transform.rotation.x,Joint2Joint.transform.rotation.y, Joint2Joint.transform.rotation.z, Joint2Joint.transform.rotation.w);           


            if (abs((double)Rotation.getAngle()>M_PI/2))
            {
                retVal.Front.leftWheel=0;
                retVal.Front.rightWheel=0;
                retVal.Rear.leftWheel=0;
                retVal.Rear.rightWheel=0;
                return retVal;
            }


            //Calculate Speed Joint Front
            SpeedJointFront=SpeedAxesFront+OmegaFront.cross(TranslationFront);

            //Transform Speed in JointRear, because they have to move with the same Speed
            SpeedJointRear=SpeedJointFront.rotate(Rotation.getAxis(), Rotation.getAngle());

            //Calculate needed Speed and Omega for AxesRear, assuming that Z and Y for the Translation from the Joint to the Axes are zero
            OmegaRear.setValue(0,0,-SpeedJointRear.y()/TranslationRear.x());
            SpeedAxesRear.setValue(SpeedJointRear.x(),0,0);

            break;

        //RearSpeed is given
        case coordinate::Rear:

            //Get latest Transforms
            Axes2Joint=tf_buffer_->lookupTransform("jointRear", "axesRear", rclcpp::Time(0));
            Joint2Joint=tf_buffer_->lookupTransform("jointFront", "jointRear", rclcpp::Time(0));
            Joint2Axes=tf_buffer_->lookupTransform("axesFront", "jointFront", rclcpp::Time(0));

            // Vektor für Rearaxengeschwindigkeit
            SpeedAxesRear.setValue(cmdVelMsg.linear.x,cmdVelMsg.linear.y,cmdVelMsg.linear.z);
            // Vektor für Reardrehgeschwindigkeit
            OmegaRear.setValue(cmdVelMsg.angular.x,cmdVelMsg.angular.y,cmdVelMsg.angular.z);
            
            // Vektor für Reartranslation
            TranslationRear.setValue(-Axes2Joint.transform.translation.x, -Axes2Joint.transform.translation.y, -Axes2Joint.transform.translation.z);
            // Vektor für Fronttranslation
            TranslationFront.setValue(-Joint2Axes.transform.translation.x, -Joint2Axes.transform.translation.y, -Joint2Axes.transform.translation.z);
            
            // Quaternion für die Rotation
            Rotation.setValue(Joint2Joint.transform.rotation.x,Joint2Joint.transform.rotation.y, Joint2Joint.transform.rotation.z, Joint2Joint.transform.rotation.w);
            
            if (abs(Rotation.getAngle()>M_PI/2))
            {
                retVal.Front.leftWheel=0;
                retVal.Front.rightWheel=0;
                retVal.Rear.leftWheel=0;
                retVal.Rear.rightWheel=0;
                return retVal;
            }
            
            //Calculate Speed Joint Rear
            SpeedJointRear=SpeedAxesRear+OmegaRear.cross(TranslationRear);

            //Transform Speed in JointFront, because they have to move with the same Speed
            SpeedJointFront=SpeedJointRear.rotate(Rotation.getAxis(), Rotation.getAngle());

            //Calculate needed Speed and Omega for AxesFront, assuming that Z and Y for the Translation from the Joint to the Axes are zero
            OmegaFront.setValue(0,0,-SpeedJointFront.y()/TranslationFront.x());
            SpeedAxesFront.setValue(SpeedJointFront.x(),0,0);
            break;

        //Do not calculate when any other Frame is given
        default:
            throw new std::runtime_error("Only Front and Rear Frames are allowed for inverse kinematics");
        }
    }
    catch(tf2::TransformException &e)
    {
        RCLCPP_ERROR(rclcpp::get_logger("global_logger"), "tf not connected! Can not calculate Transform");
        retVal.Front.leftWheel=0;
        retVal.Front.rightWheel=0;
        retVal.Rear.leftWheel=0;
        retVal.Rear.rightWheel=0;
        return retVal;
    }

    //Set Messages for further Calculation
    // SpeedAxesFront
    FrontMsg.linear.x=SpeedAxesFront.x();
    FrontMsg.linear.y=SpeedAxesFront.y();
    FrontMsg.linear.z=SpeedAxesFront.z();
    // OmegaFront
    FrontMsg.angular.x=OmegaFront.x();
    FrontMsg.angular.y=OmegaFront.y();
    FrontMsg.angular.z=OmegaFront.z();
    // SpeedAxesRear
    RearMsg.linear.x=SpeedAxesRear.x();
    RearMsg.linear.y=SpeedAxesRear.y();
    RearMsg.linear.z=SpeedAxesRear.z();
    // OmegaRear
    RearMsg.angular.x=OmegaRear.x();
    RearMsg.angular.y=OmegaRear.y();
    RearMsg.angular.z=OmegaRear.z();

    // Berechnung der Radgeschwindidkeiten über die Inverse (siehe differential_drive.cpp)
    retVal.Front=frontDrive_.inverseKinematics(FrontMsg);
    retVal.Rear=rearDrive_.inverseKinematics(RearMsg);

    return retVal;
}

// Forward Kinematic
// ----------------------
geometry_msgs::msg::Pose2D kinematics::ArticulatedDrive::forwardKinematics(articulatedWheelSpeed WheelSpeed, rclcpp::Time Timestamp)
{
    geometry_msgs::msg::Pose2D FrontPose=frontDrive_.forwardKinematics(WheelSpeed.Front, Timestamp);
    geometry_msgs::msg::Pose2D RearPose=rearDrive_.forwardKinematics(WheelSpeed.Rear, Timestamp);

    switch (Base_)
    {
        case coordinate::Front:
            return FrontPose;
            break;

        case coordinate::Rear:
            return RearPose;
            break;

        default:
            throw new std::runtime_error("Can not calculate forward kinematics for given Frame");
    }
}

// Parameter setzen
// ----------------------
void kinematics::ArticulatedDrive::setParam(double AxesLength, double WheelDiameter, coordinate Base)
{
    frontDrive_.setParam(AxesLength, WheelDiameter);
    rearDrive_.setParam(AxesLength, WheelDiameter);
    Base_=Base;
}

// Aktuelle Position zurückgeben
// ----------------------
geometry_msgs::msg::Pose2D kinematics::ArticulatedDrive::getActualPose(coordinate Frame)
{
    switch (Base_)
    {
        case coordinate::Front:
            return frontDrive_.getActualPose();
            break;
        case coordinate::Rear:
            return rearDrive_.getActualPose();
            break;
        default:
            throw new std::runtime_error("Can not get Pose for given Frame");
    }
}

// Aktuelle Geschwindigkeit zurückgeben
// ----------------------
geometry_msgs::msg::Twist kinematics::ArticulatedDrive::getSpeed()
{
    switch (Base_)
    {
        case coordinate::Front:
            return frontDrive_.getSpeed();
            break;

        case coordinate::Rear:
            return rearDrive_.getSpeed();
            break;

        default:
            throw new std::runtime_error("Can not get Speed for given Frame");
    }
}

