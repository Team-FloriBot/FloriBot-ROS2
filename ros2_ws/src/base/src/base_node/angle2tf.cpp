#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <tf2_ros/transform_broadcaster.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <base/msg/angle.hpp>
#include <base/msg/wheels.hpp>

class Angle2TFNode : public rclcpp::Node
{
public:
    Angle2TFNode()
    : Node("angle2tf")
    {
        // Erstelle den TransformBroadcaster
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

        // Subscriber erstellen
        angle_subscriber_ = this->create_subscription<sensor_msgs::msg::JointState>(
            "/floribot/joint_states", 10, std::bind(&Angle2TFNode::AngleCallback, this, std::placeholders::_1));

        // Publisher erstellen
        actual_speed_publisher_ = this->create_publisher<base::msg::Wheels>("engine/actualSpeed", 10);
    }

private:
    void AngleCallback(const sensor_msgs::msg::JointState::SharedPtr msg)
    {
        if (msg->velocity.size() > 0) {
            tf2::Quaternion q;
            geometry_msgs::msg::TransformStamped tf_msg;
            tf_msg.header.seq = msg->header.seq;
            tf_msg.child_frame_id = "jointRear";
            tf_msg.header.frame_id = "jointFront";
            tf_msg.header.stamp = this->get_clock()->now();

            q.setRPY(0, 0, msg->position[0]);
            tf_msg.transform.translation.x = 0;
            tf_msg.transform.translation.y = 0;
            tf_msg.transform.translation.z = 0;

            tf_msg.transform.rotation.x = q.x();
            tf_msg.transform.rotation.y = q.y();
            tf_msg.transform.rotation.z = q.z();
            tf_msg.transform.rotation.w = q.w();

            tf_broadcaster_->sendTransform(tf_msg);

            // Actual Speed Nachricht zusammenstellen
            base::msg::Wheels wheels_msg;
            wheels_msg.header.seq = msg->header.seq;
            wheels_msg.header.stamp = this->get_clock()->now();

            wheels_msg.front_left = msg->velocity[1];
            wheels_msg.front_right = msg->velocity[2];
            wheels_msg.rear_left = msg->velocity[3];
            wheels_msg.rear_right = msg->velocity[4];

            actual_speed_publisher_->publish(wheels_msg);
        }
    }

    // Subscriber, Publisher und TransformBroadcaster
    rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr

