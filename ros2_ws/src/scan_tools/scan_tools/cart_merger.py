import rclpy
from rclpy.node import Node
import tf2_ros
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
import geometry_msgs.msg


class PointCloudTransformer(Node):
    def __init__(self):
        super().__init__('point_cloud_transformer')
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Publisher und Subscriber
        self.pub_merged = self.create_publisher(PointCloud2, '/merged_point_cloud', 10)
        self.sub_front = self.create_subscription(PointCloud2, '/laser_scanner_front_cart', self.transform_callback_front, 10)
        self.sub_rear = self.create_subscription(PointCloud2, '/laser_scanner_rear_cart', self.transform_callback_rear, 10)

        # Initialisierte Variablen
        self.front_points = None
        self.rear_points = None
        self.current_header = None

    def transform_callback_front(self, cloud_msg):
        try:
            merge_frame = self.get_parameter('merge_frame').get_parameter_value().string_value
            transform = self.tf_buffer.lookup_transform(merge_frame, cloud_msg.header.frame_id, rclpy.time.Time())
            
            # Transformiere die Punktwolke manuell
            transformed_cloud_msg = self.transform_cloud(cloud_msg, transform)
            transformed_cloud_msg.header.frame_id = merge_frame
            self.front_points = transformed_cloud_msg
            self.check_and_publish()
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().warn('Error transforming point cloud: %s' % e)

    def transform_callback_rear(self, cloud_msg):
        try:
            merge_frame = self.get_parameter('merge_frame').get_parameter_value().string_value
            transform = self.tf_buffer.lookup_transform(merge_frame, cloud_msg.header.frame_id, rclpy.time.Time())
            
            # Transformiere die Punktwolke manuell
            transformed_cloud_msg = self.transform_cloud(cloud_msg, transform)
            transformed_cloud_msg.header.frame_id = merge_frame
            self.rear_points = transformed_cloud_msg
            self.check_and_publish()
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().warn('Error transforming point cloud: %s' % e)

    def transform_cloud(self, cloud_msg, transform):
        # Durchlaufe alle Punkte in der PointCloud2-Nachricht
        points = list(point_cloud2.read_points(cloud_msg, field_names=("x", "y", "z"), skip_nans=True))
        
        # Erstelle eine neue Liste für die transformierten Punkte
        transformed_points = []
        
        for point in points:
            # Transformiere jeden Punkt
            point_msg = geometry_msgs.msg.PointStamped()
            point_msg.header = cloud_msg.header
            point_msg.point.x = point[0]
            point_msg.point.y = point[1]
            point_msg.point.z = point[2]
            
            # Transformiere den Punkt
            transformed_point_msg = self.tf_buffer.transform(point_msg, transform.header.frame_id)
            transformed_points.append([transformed_point_msg.point.x, transformed_point_msg.point.y, transformed_point_msg.point.z])
        
        # Erstelle eine neue PointCloud2-Nachricht mit den transformierten Punkten
        transformed_cloud = point_cloud2.create_cloud_xyz32(cloud_msg.header, transformed_points)
        return transformed_cloud

    def check_and_publish(self):
        if self.front_points is not None and self.rear_points is not None:
            self.merge_points()
            merged_cloud = point_cloud2.create_cloud_xyz32(self.current_header, self.merged_points)
            self.pub_merged.publish(merged_cloud)
            self.merged_points = []
            self.front_points = None
            self.rear_points = None

    def merge_points(self):
        merged_points = []
        for point in point_cloud2.read_points(self.front_points, field_names=("x", "y", "z")):
            merged_points.append(point)
        for point in point_cloud2.read_points(self.rear_points, field_names=("x", "y", "z")):
            merged_points.append(point)
        self.current_header = self.front_points.header
        self.merged_points = merged_points


def main(args=None):
    rclpy.init(args=args)
    node = PointCloudTransformer()

    # Set default parameter for merge_frame
    node.declare_parameter('merge_frame', 'front_laser')

    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
