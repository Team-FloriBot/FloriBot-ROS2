import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point32
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs_py import point_cloud2
import time as t

class FieldRobotNavigator(Node):
    def __init__(self):
        super().__init__('field_robot_navigator')

        # Set up subscribers and publishers
        self.create_subscription(PointCloud2, '/merged_point_cloud', self.point_cloud_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.points_pub = self.create_publisher(PointCloud2, '/field_points', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        # Initialize member variables
        self.robot_pose = None
        self.points = None

        self.declare_parameter('box', 'drive')
        self.declare_parameter('both_sides', 'both')
          # Parameter deklarieren
        self.declare_parameter('x_min_drive_in_row', -0.2)
        self.declare_parameter('x_max_drive_in_row', 1.15)
        self.declare_parameter('y_min_drive_in_row', 0.1)
        self.declare_parameter('y_max_drive_in_row', 0.75)
        self.declare_parameter('row_width', 0.6)
        self.declare_parameter('drive_out_dist', 0.5)
        self.declare_parameter('max_dist_in_row', 0.5)
        self.declare_parameter('critic_row', [0, 1])
        self.declare_parameter('vel_linear_drive', 0.2)
        self.declare_parameter('vel_linear_count', 0.1)
        self.declare_parameter('vel_linear_turn', 0.1)
        self.declare_parameter('x_min_turn_and_exit', -0.2)
        self.declare_parameter('x_max_turn_and_exit', 1.15)
        self.declare_parameter('y_min_turn_and_exit', 0.1)
        self.declare_parameter('y_max_turn_and_exit', 0.75)
        self.declare_parameter('x_min_counting_rows', -0.2)
        self.declare_parameter('x_max_counting_rows', 1.15)
        self.declare_parameter('y_min_counting_rows', 0.1)
        self.declare_parameter('y_max_counting_rows', 0.75)
        self.declare_parameter('x_min_turn_to_row', -0.2)
        self.declare_parameter('x_max_turn_to_row', 1.15)
        self.declare_parameter('y_min_turn_to_row', 0.1)
        self.declare_parameter('y_max_turn_to_row', 0.75)
        self.declare_parameter('x_min_turn_to_row_critic', -0.2)
        self.declare_parameter('x_max_turn_to_row_critic', 1.15)
        self.declare_parameter('y_min_turn_to_row_critic', 0.1)
        self.declare_parameter('y_max_turn_to_row_critic', 0.75)

        
        # Hier deklarierst du den Parameter pattern
        self.declare_parameter('pattern_steps', [3, 1, 1, 1, 1, 1])
        self.declare_parameter('pattern_direction', ['L', 'R', 'L', 'R', 'L', 'R'])

        # Initialize parameters
        self.x_min = self.get_parameter('x_min_drive_in_row').get_parameter_value().double_value
        self.x_max = self.get_parameter('x_max_drive_in_row').get_parameter_value().double_value
        self.y_min = self.get_parameter('y_min_drive_in_row').get_parameter_value().double_value
        self.y_max = self.get_parameter('y_max_drive_in_row').get_parameter_value().double_value

        self.row_width = self.get_parameter('row_width').get_parameter_value().double_value
        self.drive_out_dist = self.get_parameter('drive_out_dist').get_parameter_value().double_value
        self.max_dist_in_row = self.get_parameter('max_dist_in_row').get_parameter_value().double_value
        self.critic_row = self.get_parameter('critic_row').get_parameter_value().integer_array_value

        self.vel_linear_drive = self.get_parameter('vel_linear_drive').get_parameter_value().double_value
        self.vel_linear_count = self.get_parameter('vel_linear_count').get_parameter_value().double_value
        self.vel_linear_turn = self.get_parameter('vel_linear_turn').get_parameter_value().double_value
        
        # Initialize state variables
        self.current_state = 'drive_in_row'
        self.pattern_steps = self.get_parameter('pattern_steps').get_parameter_value().integer_array_value
        self.pattern_direction = self.get_parameter('pattern_direction').get_parameter_value().string_array_value

        self.driven_row = 0

    def point_cloud_callback(self, msg):
        points = []
        both_sides = self.get_parameter('both_sides').get_parameter_value().string_value
        min_distance = float('inf')  # initialize minimum distance with infinity

        for p in point_cloud2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True):
            point = Point32()
            x, y, z = p
            point.x = x
            point.y = y
            point.z = z
            distance = np.sqrt(point.x**2 + point.y**2)  # calculate Euclidean distance
            if distance < min_distance:
                min_distance = distance
            if both_sides == 'both':
                if self.y_min < np.abs(point.y) < self.y_max and self.x_min < point.x < self.x_max:
                    points.append(point)
            elif both_sides == 'L':
                if -self.y_max < point.y < -self.y_min and self.x_min < point.x < self.x_max:
                    points.append(point)
            elif both_sides == 'R':
                if self.y_min < point.y < self.y_max and self.x_min < point.x < self.x_max:
                    points.append(point)
        self.min_dist = min_distance
        self.points = points

        # Publish self.points
        header = msg.header
        header.frame_id = "front_laser"
        fields = [PointField(),
                  PointField(),
                  PointField()]
        fields[0].name = 'x'
        fields[0].offset = 0
        fields[0].datatype = PointField.FLOAT32
        fields[0].count = 1
        fields[1].name = 'y'
        fields[1].offset = 4
        fields[1].datatype = PointField.FLOAT32
        fields[1].count = 1
        fields[2].name = 'z'
        fields[2].offset = 8
        fields[2].datatype = PointField.FLOAT32
        fields[2].count = 1
        #[PointField('x', 0, PointField.FLOAT32, 1),
        #PointField('y', 4, PointField.FLOAT32, 1),
        #PointField('z', 8, PointField.FLOAT32, 1)]
        points = [(p.x, p.y, p.z) for p in self.points]
        cloud = point_cloud2.create_cloud(header, fields, points)
        self.points_pub.publish(cloud)

    def timer_callback(self):
        if self.points is not None:
            if self.current_state == 'drive_in_row':
                self.drive_in_row()
            elif self.current_state == 'turn_and_exit':
                self.turn_and_exit()
            elif self.current_state == 'counting_rows':
                self.counting_rows()
            elif self.current_state == 'turn_to_row':
                self.turn_to_row()

            

    def drive_in_row(self):
        self.get_logger().info("Driving in row...")
        # Calculate the average distance to the robot on both sides within x and y limits
        self.set_parameters([rclpy.parameter.Parameter('box', rclpy.Parameter.Type.STRING, 'drive')])
        self.set_parameters([rclpy.parameter.Parameter('both_sides', rclpy.Parameter.Type.STRING, 'both')])

        left_y = [p.y for p in self.points if p.y < 0]
        right_y = [p.y for p in self.points if p.y >= 0]
        left_dist = np.mean(np.abs(left_y)) if len(left_y) > 1 else np.inf  # left is negative usually
        right_dist = np.mean(np.abs(right_y)) if len(right_y) > 1 else np.inf

        if np.isinf(left_dist) or np.isinf(right_dist):
            # Not enough data to calculate center
            self.get_logger().info("At least one side has no maize")
            self.get_logger().info("Reached the end of a row.")
            cmd_vel = Twist()
            cmd_vel.linear.x = self.vel_linear_drive
            time = self.drive_out_dist / self.vel_linear_drive
            start_time = self.get_clock().now().seconds_nanoseconds()[0]
            while (self.get_clock().now().seconds_nanoseconds()[0] - start_time) < time:
                self.cmd_vel_pub.publish(cmd_vel)
                self.get_logger().info("Leaving the row...")
                t.sleep(0.1)

            self.x_min = self.get_parameter('x_min_turn_and_exit').get_parameter_value().double_value
            self.x_max = self.get_parameter('x_max_turn_and_exit').get_parameter_value().double_value
            self.y_min = self.get_parameter('y_min_turn_and_exit').get_parameter_value().double_value
            self.y_max = self.get_parameter('y_max_turn_and_exit').get_parameter_value().double_value
            self.set_parameters([rclpy.parameter.Parameter('box', rclpy.Parameter.Type.STRING, 'exit')])
            self.set_parameters([rclpy.parameter.Parameter('both_sides', rclpy.Parameter.Type.STRING, self.pattern_direction[self.driven_row])])
            self.driven_row += 1 
            self.current_state = 'turn_and_exit'
        else:
            # Calculate the actual distance to the center of both sides
            center_dist = (right_dist - left_dist) / 2.0
            self.get_logger().info("Distance to center: %f" % center_dist)
         # Adjust the angular velocity to center the robot between the rows
            cmd_vel = Twist()
            cmd_vel.angular.z = -center_dist * 5 * self.vel_linear_drive
            if np.abs(center_dist) > 0.15:
                cmd_vel.linear.x = 0.1
                if np.abs(center_dist) > 0.20:
                    self.get_logger().warn('Too close to row!!!')
            else:
                cmd_vel.linear.x = self.vel_linear_drive * (self.max_dist_in_row - np.abs(center_dist)) / self.max_dist_in_row
            self.get_logger().info("Publishing to cmd_vel: %s" % cmd_vel)
        self.cmd_vel_pub.publish(cmd_vel)

    # The other methods (turn_and_exit, counting_rows, etc.) would follow the same pattern as above.
    # Please repeat the similar transformations for the rest of the methods.


    def turn_and_exit(self):
        self.get_logger().info("Turn and exit...")
        # Calculate the average distance to the robot on both sides within x and y limits
        points_x = [p.x for p in self.points]
        x_mean = np.mean(points_x) if len(points_x) > 0 else np.inf 
        self.get_logger().info("xmean: %f"% x_mean)
        if -0.25 < x_mean < 0.25:
            cmd_vel = Twist()
            self.get_logger().info("Aligned to the rows...")
            self.x_min = self.get_parameter('x_min_counting_rows').get_parameter_value().double_value
            self.x_max = self.get_parameter('x_max_counting_rows').get_parameter_value().double_value
            self.y_min = self.get_parameter('y_min_counting_rows').get_parameter_value().double_value
            self.y_max = self.get_parameter('y_max_counting_rows').get_parameter_value().double_value
            if self.pattern_steps[self.driven_row-1]==1:
                if self.driven_row in self.critic_row:
                    self.x_min = self.get_parameter('x_min_turn_to_row_critic').get_parameter_value().double_value
                    self.x_max = self.get_parameter('x_max_turn_to_row_critic').get_parameter_value().double_value
                    self.y_min = self.get_parameter('y_min_turn_to_row_critic').get_parameter_value().double_value
                    self.y_max = self.get_parameter('y_max_turn_to_row_critic').get_parameter_value().double_value
                    self.set_parameters([rclpy.parameter.Parameter('box', rclpy.Parameter.Type.STRING, 'turn_crit')])
                else:
                    self.x_min = self.get_parameter('x_min_turn_to_row').get_parameter_value().double_value
                    self.x_max = self.get_parameter('x_max_turn_to_row').get_parameter_value().double_value
                    self.y_min = self.get_parameter('y_min_turn_to_row').get_parameter_value().double_value
                    self.y_max = self.get_parameter('y_max_turn_to_row').get_parameter_value().double_value
                    self.set_parameters([rclpy.parameter.Parameter('box', rclpy.Parameter.Type.STRING, 'turn')])

                self.set_parameters([rclpy.parameter.Parameter('both_sides', rclpy.Parameter.Type.STRING, 'both')])
                self.current_state = 'turn_to_row'
            else:    
                self.set_parameters([rclpy.parameter.Parameter('box', rclpy.Parameter.Type.STRING, 'count')])
                self.row_counter = 1
                self.previous_row = 1
                self.actual_row = 1
                self.actual_dist = self.min_dist
                self.current_state = 'counting_rows'

        else:
            if 0 <= self.driven_row < len(self.pattern_direction):
                if self.pattern_direction[self.driven_row-1] == 'L':
                    # Calculate the actual distance to the center of both sides
                    self.get_logger().info("Turning left until parallel...")
                    # Adjust the angular velocity to center the robot between the rows
                    cmd_vel = Twist()
                    cmd_vel.linear.x = self.vel_linear_turn
                    radius = self.row_width/2
                    cmd_vel.angular.z = self.vel_linear_turn/radius
                elif self.pattern_direction[self.driven_row-1] == 'R':
                    self.get_logger().info("Turning right until parallel...")
                    cmd_vel = Twist()
                    cmd_vel.linear.x = self.vel_linear_turn
                    radius = -self.row_width/2
                    cmd_vel.angular.z = self.vel_linear_turn/radius
                else:
                    self.get_logger().warn("Invalid direction at driven_row index")
                    cmd_vel = Twist()
            else:
                self.get_logger().info("Pattern is now finished")
                cmd_vel = Twist()
                

            self.get_logger().info("Publishing to cmd_vel: %s"% cmd_vel)

        self.cmd_vel_pub.publish(cmd_vel)

    def counting_rows(self):
        self.get_logger().info("counting rows...")
        # Calculate the average distance to the robot on both sides within x and y limits
        if self.pattern_steps[self.driven_row-1] == self.row_counter:
            self.get_logger().info("start turning to row...")
            if self.driven_row in self.critic_row:
                self.x_min = self.get_parameter('x_min_turn_to_row_critic').get_parameter_value().double_value
                self.x_max = self.get_parameter('x_max_turn_to_row_critic').get_parameter_value().double_value
                self.y_min = self.get_parameter('y_min_turn_to_row_critic').get_parameter_value().double_value
                self.y_max = self.get_parameter('y_max_turn_to_row_critic').get_parameter_value().double_value
                self.set_parameters([rclpy.parameter.Parameter('box', rclpy.Parameter.Type.STRING, 'turn_crit')])
            else:
                self.x_min = self.get_parameter('x_min_turn_to_row').get_parameter_value().double_value
                self.x_max = self.get_parameter('x_max_turn_to_row').get_parameter_value().double_value
                self.y_min = self.get_parameter('y_min_turn_to_row').get_parameter_value().double_value
                self.y_max = self.get_parameter('y_max_turn_to_row').get_parameter_value().double_value
                self.set_parameters([rclpy.parameter.Parameter('box', rclpy.Parameter.Type.STRING, 'turn')])
            self.set_parameters([rclpy.parameter.Parameter('both_sides', rclpy.Parameter.Type.STRING, 'both')])
            self.current_state = 'turn_to_row'
        else:
            if self.pattern_direction[self.driven_row-1]=='L':
                gain=2.5
            elif self.pattern_direction[self.driven_row-1]=='R':
                gain=-2.5

            # Calculate the actual distance to the center of both sides
            self.get_logger().info("Holding Distance, driving parallel")
            # Adjust the angular velocity to center the robot between the rows
            cmd_vel = Twist()
            cmd_vel.linear.x = self.vel_linear_count
            self.get_logger().info("No. of points in Box %i"% len(self.points))
            if  len(self.points)>0:
                 # Compute the shortest y distance
                cmd_vel.angular.z = gain*(self.min_dist - self.actual_dist)
                diff=self.min_dist - self.actual_dist
                self.get_logger().info("Gap to desired distance:%f"% diff)
                self.actual_row = 1
            else:
                    cmd_vel.angular.z = 0.0
                    self.actual_row = 0
            if self.actual_row > self.previous_row:
               self.row_counter+=1
               self.get_logger().info("Increment row_counter to %i"% self.row_counter)

            self.get_logger().info("Passing row %i of %i"% (self.row_counter, self.pattern_steps[self.driven_row-1]))
            self.previous_row=self.actual_row     
            self.get_logger().info("Publishing to cmd_vel: %s"% cmd_vel)
            self.cmd_vel_pub.publish(cmd_vel)

    def turn_to_row(self):
        self.get_logger().info("Turn to row...")
        # Calculate the average distance to the robot on both sides within x and y limits
        points_y = [p.y for p in self.points]
        y_mean = np.mean((points_y)) if len(points_y) > 0 else np.inf #left is negative usually
        self.get_logger().info("ymean: %f"% y_mean)
        if -0.25 < y_mean < 0.25:
            cmd_vel = Twist()
            self.get_logger().info("Start driving in row...")
            self.x_min = self.get_parameter('x_min_drive_in_row').get_parameter_value().double_value
            self.x_max = self.get_parameter('x_max_drive_in_row').get_parameter_value().double_value
            self.y_min = self.get_parameter('y_min_drive_in_row').get_parameter_value().double_value
            self.y_max = self.get_parameter('y_max_drive_in_row').get_parameter_value().double_value
            self.current_state = 'drive_in_row'
        else:
            if 0 <= self.driven_row < len(self.pattern_direction):
                if self.pattern_direction[self.driven_row-1] == 'L':
                    gain = 1
                elif self.pattern_direction[self.driven_row-1] == 'R':
                    gain=-1
                else:
                    self.get_logger().warn("Invalid direction at driven_row index")
                    cmd_vel = Twist()

                self.get_logger().info("Turning right until parallel...")
                cmd_vel = Twist()
                cmd_vel.linear.x = self.vel_linear_turn
                radius = gain*self.row_width/2
                cmd_vel.angular.z = self.vel_linear_turn/radius
            else:
                self.get_logger().warn("Driven_row index out of range")
                cmd_vel = Twist()

            self.get_logger().info("Publishing to cmd_vel: %s"% cmd_vel)

        self.cmd_vel_pub.publish(cmd_vel)


def main(args=None):
    rclpy.init(args=args)
    navigator = FieldRobotNavigator()
    rclpy.spin(navigator)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
