import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
from laser_geometry import LaserProjection

class LaserScanToPointCloud(Node):
    def __init__(self, node_name='laser_scan_to_pointcloud'):
        super().__init__(node_name)

        # Declare parameters with default values
        self.declare_parameter('scan_topic', '/laser_scanner_front')
        self.declare_parameter('pointcloud_topic', '/laser_scanner_front_cart')

        # Get parameters
        scan_topic = self.get_parameter('scan_topic').get_parameter_value().string_value
        pointcloud_topic = self.get_parameter('pointcloud_topic').get_parameter_value().string_value

        # Create LaserProjection object
        self.lp = LaserProjection()

        # Create subscriber and publisher
        self.sub = self.create_subscription(LaserScan, scan_topic, self.callback, 10)
        self.pub = self.create_publisher(PointCloud2, pointcloud_topic, 10)

        self.get_logger().info(f'Node "{node_name}" initialized.')
        self.get_logger().info(f'Subscribed to "{scan_topic}", publishing to "{pointcloud_topic}".')

    def callback(self, data):
        # Convert LaserScan to PointCloud2
        cloud = self.lp.projectLaser(data)

        # Publish the PointCloud2 data
        self.pub.publish(cloud)


def main(args=None):
    rclpy.init(args=args)

    # Initialize and run the node
    node = LaserScanToPointCloud()
    rclpy.spin(node)

    # Shutdown and clean up
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
