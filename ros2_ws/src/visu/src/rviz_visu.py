#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

class BoundingBoxPublisher(Node):
    def __init__(self):
        super().__init__('bounding_box_publisher')
        self.publisher_ = self.create_publisher(Marker, 'bounding_boxes', 10)
        self.timer = self.create_timer(0.2, self.publish_bounding_boxes)  # Timer to run periodically
        self.previous_box = 'initial'
        self.previous_sides = 'initial'
        self.declare_parameter('box', 'drive')
        self.declare_parameter('both_sides', 'both')
        self.get_logger().info("Start with default Drive BOX")
        self.idx = 0

    def publish_bounding_boxes(self):
        # Deleting old markers
        if self.idx <= 2:
            marker_left_msg = Marker()
            marker_left_msg.header.frame_id = "front_laser"
            marker_left_msg.ns = "bounding_boxes"
            marker_left_msg.id = 0  # ID of the left marker
            marker_left_msg.action = Marker.DELETE  # Set the action to DELETE
            marker_left_msg.lifetime = rclpy.duration.Duration(seconds=0)  # Set a short lifetime (0 seconds)

            marker_right_msg = Marker()
            marker_right_msg.header.frame_id = "front_laser"
            marker_right_msg.ns = "bounding_boxes"
            marker_right_msg.id = 1  # ID of the right marker
            marker_right_msg.action = Marker.DELETE  # Set the action to DELETE
            marker_right_msg.lifetime = rclpy.duration.Duration(seconds=0)  # Set a short lifetime (0 seconds)

            # Publish deletion messages for both markers
            self.publisher_.publish(marker_left_msg)
            self.publisher_.publish(marker_right_msg)
            self.get_logger().info("Deleting old markers...")
            self.idx += 1
            return  # Wait for next call, don't proceed with bounding box logic yet

        box = self.get_parameter('box').get_parameter_value().string_value
        sides = self.get_parameter('both_sides').get_parameter_value().string_value

        if sides != self.previous_sides or box != self.previous_box:
            # Define the bounding box coordinates based on the selected 'box'
            if box == 'drive':
                x_min = self.get_parameter('x_min_drive_in_row').get_parameter_value().double_value
                x_max = self.get_parameter('x_max_drive_in_row').get_parameter_value().double_value
                y_min = self.get_parameter('y_min_drive_in_row').get_parameter_value().double_value
                y_max = self.get_parameter('y_max_drive_in_row').get_parameter_value().double_value
            elif box == 'exit':
                x_min = self.get_parameter('x_min_turn_and_exit').get_parameter_value().double_value
                x_max = self.get_parameter('x_max_turn_and_exit').get_parameter_value().double_value
                y_min = self.get_parameter('y_min_turn_and_exit').get_parameter_value().double_value
                y_max = self.get_parameter('y_max_turn_and_exit').get_parameter_value().double_value
            elif box == 'count':
                x_min = self.get_parameter('x_min_counting_rows').get_parameter_value().double_value
                x_max = self.get_parameter('x_max_counting_rows').get_parameter_value().double_value
                y_min = self.get_parameter('y_min_counting_rows').get_parameter_value().double_value
                y_max = self.get_parameter('y_max_counting_rows').get_parameter_value().double_value
            elif box == 'turn':
                x_min = self.get_parameter('x_min_turn_to_row').get_parameter_value().double_value
                x_max = self.get_parameter('x_max_turn_to_row').get_parameter_value().double_value
                y_min = self.get_parameter('y_min_turn_to_row').get_parameter_value().double_value
                y_max = self.get_parameter('y_max_turn_to_row').get_parameter_value().double_value
            elif box == 'turn_crit':
                x_min = self.get_parameter('x_min_turn_to_row_critic').get_parameter_value().double_value
                x_max = self.get_parameter('x_max_turn_to_row_critic').get_parameter_value().double_value
                y_min = self.get_parameter('y_min_turn_to_row_critic').get_parameter_value().double_value
                y_max = self.get_parameter('y_max_turn_to_row_critic').get_parameter_value().double_value
            else:
                self.get_logger().info("wrong box type")

            center_x = (x_min + x_max) / 2.0
            center_y = (y_min + y_max) / 2.0

            # Create and configure the left bounding box marker
            marker_left_msg = Marker()
            marker_left_msg.header.frame_id = "front_laser"
            marker_left_msg.type = Marker.CUBE
            marker_left_msg.action = Marker.ADD
            marker_left_msg.id = 0
            marker_left_msg.pose.position.x = center_x
            marker_left_msg.pose.position.y = -center_y
            marker_left_msg.pose.position.z = 0.0
            marker_left_msg.pose.orientation.x = 0.0
            marker_left_msg.pose.orientation.y = 0.0
            marker_left_msg.pose.orientation.z = 0.0
            marker_left_msg.pose.orientation.w = 1.0
            marker_left_msg.scale.x = abs(x_max - x_min)
            marker_left_msg.scale.y = abs(y_max - y_min)
            marker_left_msg.scale.z = 0.1
            marker_left_msg.color.a = 0.5
            marker_left_msg.color.r = 0.0
            marker_left_msg.color.g = 1.0
            marker_left_msg.color.b = 0.0

            # Create and configure the right bounding box marker
            marker_right_msg = Marker()
            marker_right_msg.header.frame_id = "front_laser"
            marker_right_msg.type = Marker.CUBE
            marker_right_msg.action = Marker.ADD
            marker_right_msg.id = 1
            marker_right_msg.pose.position.x = center_x
            marker_right_msg.pose.position.y = center_y
            marker_right_msg.pose.position.z = 0.0
            marker_right_msg.pose.orientation.x = 0.0
            marker_right_msg.pose.orientation.y = 0.0
            marker_right_msg.pose.orientation.z = 0.0
            marker_right_msg.pose.orientation.w = 1.0
            marker_right_msg.scale.x = abs(x_max - x_min)
            marker_right_msg.scale.y = abs(y_max - y_min)
            marker_right_msg.scale.z = 0.1
            marker_right_msg.color.a = 0.5
            marker_right_msg.color.r = 0.0
            marker_right_msg.color.g = 1.0
            marker_right_msg.color.b = 0.0

            # Publish based on the 'sides' parameter
            if sides == 'R':
                self.publisher_.publish(marker_right_msg)
                marker_left_msg.action = Marker.DELETE
                self.publisher_.publish(marker_left_msg)
            elif sides == 'both':
                self.publisher_.publish(marker_right_msg)
                self.publisher_.publish(marker_left_msg)
                self.get_logger().info("Publish both Boxes")
            elif sides == 'L':
                self.publisher_.publish(marker_left_msg)
                marker_right_msg.action = Marker.DELETE
                self.publisher_.publish(marker_right_msg)
            else:
                self.get_logger().info("No valid side")

            self.previous_box = box
            self.previous_sides = sides

def main(args=None):
    rclpy.init(args=args)
    node = BoundingBoxPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
