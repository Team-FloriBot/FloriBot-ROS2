import rclpy
from rclpy.node import Node
import tf2_ros
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
import PyKDL
from sensor_msgs_py.point_cloud2 import create_cloud, read_points, create_cloud_xyz32
#


class PointCloudTransformer(Node):
    # Initialisierung
    # -------------------------
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

    # Laser Scanner front Subscriber
    # -------------------------
    def transform_callback_front(self, cloud_msg):
        try:
            merge_frame = self.get_parameter('merge_frame').get_parameter_value().string_value
            transform = self.tf_buffer.lookup_transform(merge_frame, cloud_msg.header.frame_id, rclpy.time.Time())
            
            # Transformiere die Punktwolke manuell
            transformed_cloud_msg = self.do_transform_cloud(cloud_msg, transform)
            transformed_cloud_msg.header.frame_id = merge_frame
            self.front_points = transformed_cloud_msg
            self.check_and_publish()
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().warn('Error transforming point cloud: %s' % e)

    # Laser Scanner rear Subscriber
    # -------------------------
    def transform_callback_rear(self, cloud_msg):
        try:
            merge_frame = self.get_parameter('merge_frame').get_parameter_value().string_value
            transform = self.tf_buffer.lookup_transform(merge_frame, cloud_msg.header.frame_id, rclpy.time.Time())
            
            # Transformiere die Punktwolke manuell
            transformed_cloud_msg = self.do_transform_cloud(cloud_msg, transform)
            transformed_cloud_msg.header.frame_id = merge_frame
            self.rear_points = transformed_cloud_msg
            self.check_and_publish()
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().warn('Error transforming point cloud: %s' % e)

    # Transformation
    # -------------------------
    def transform_to_kdl(self, t):
        return PyKDL.Frame(PyKDL.Rotation.Quaternion(
            t.transform.rotation.x, t.transform.rotation.y,
            t.transform.rotation.z, t.transform.rotation.w),
            PyKDL.Vector(t.transform.translation.x,
                        t.transform.translation.y,
                        t.transform.translation.z))
    # Cloud-Transformations-Funktion
    # -------------------------    
    def do_transform_cloud(self, cloud, transform):
        t_kdl = self.transform_to_kdl(transform)
        points_out = []
        for p_in in read_points(cloud, field_names=("x", "y", "z")):
            p_out = t_kdl * PyKDL.Vector(p_in[0], p_in[1], p_in[2])
            points_out.append([p_out[0], p_out[1], p_out[2]])
        res = create_cloud_xyz32(transform.header, points_out)
        return res

    # Publishen wenn eine Punktewolke da ist
    # -------------------------
    def check_and_publish(self):
        if self.front_points is not None and self.rear_points is not None:
            self.merge_points()
            merged_cloud = point_cloud2.create_cloud_xyz32(self.current_header, self.merged_points)
            self.pub_merged.publish(merged_cloud)
            self.merged_points = []
            self.front_points = None
            self.rear_points = None

    # Punkte zusammenführen
    # -------------------------
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

    # Logge, ob der Node erfolgreich initialisiert wurde
    node.get_logger().info('Node erfolgreich gestartet')

    node.declare_parameter('merge_frame', 'front_laser')

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node wurde durch den Benutzer unterbrochen')
    finally:
        rclpy.shutdown()
        node.get_logger().info('ROS2 shutdown abgeschlossen')

if __name__ == '__main__':
    main()
