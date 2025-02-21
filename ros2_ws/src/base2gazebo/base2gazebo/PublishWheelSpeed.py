#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from base.msg import Wheels
from std_msgs.msg import Float64
from trajectory_msgs.msg import JointTrajectory

class WheelSpeedPublisher(Node):

    def __init__(self):
        super().__init__('wheel_speed_publisher')
        
        # Erstelle Publisher für jede Achse
        self.pub_fl = self.create_publisher(Float64, '/joint_fl_controller/command', 10)
        self.pub_fr = self.create_publisher(Float64, '/joint_fr_controller/command', 10)
        self.pub_rl = self.create_publisher(Float64, '/joint_rl_controller/command', 10)
        self.pub_rr = self.create_publisher(Float64, '/joint_rr_controller/command', 10)
        
        # Erstelle Subscriber, um die Geschwindigkeiten zu empfangen
        self.create_subscription(Wheels, '/engine/targetSpeed', self.callback, 10)

    def callback(self, data):
        msg_fl = Float64()
        msg_fl.data = data.front_left
        self.pub_fl.publish(msg_fl)

        msg_fr = Float64()
        msg_fr.data = data.front_right
        self.pub_fr.publish(msg_fr)

        msg_rl = Float64()
        msg_rl.data = data.rear_left
        self.pub_rl.publish(msg_rl)

        msg_rr = Float64()
        msg_rr.data = data.rear_right
        self.pub_rr.publish(msg_rr)

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
