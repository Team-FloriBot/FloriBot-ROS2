#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from base2gazebo.msg import Wheels
from std_msgs.msg import Float64

class WheelSpeedPublisher(Node):

    def __init__(self):
        super().__init__('wheel_speed_publisher')
        
        # Erstelle Publisher für jede Achse
        self.pub_fl = self.create_publisher(Float64, '/gazebo/joint_fl_controller/command', 10)
        self.pub_fr = self.create_publisher(Float64, '/gazebo/joint_fr_controller/command', 10)
        self.pub_rl = self.create_publisher(Float64, '/gazebo/joint_rl_controller/command', 10)
        self.pub_rr = self.create_publisher(Float64, '/gazebo/joint_rr_controller/command', 10)
        
        # Erstelle Subscriber, um die Geschwindigkeiten zu empfangen
        self.create_subscription(Wheels, '/engine/targetSpeed', self.callback, 10)

    def callback(self, data):
        # Publizieren der Werte für jede Achse
        self.pub_fl.publish(Float64(data.front_left))
        self.pub_fr.publish(Float64(data.front_right))
        self.pub_rl.publish(Float64(data.rear_left))
        self.pub_rr.publish(Float64(data.rear_right))

def main(args=None):
    rclpy.init(args=args)

    # Erstelle den Node
    node = WheelSpeedPublisher()

    # Spin, um den Node am Laufen zu halten
    rclpy.spin(node)

    # Am Ende des Programms, shutdown
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
