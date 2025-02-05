import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='scan_tools',
            executable='cart_merger',
            name='cart_merger',
            # Optional: Falls du den Parameter für den tf frame hinzufügen möchtest
            # parameters=[{'merge_frame': 'base_link'}]
        ),
        Node(
            package='scan_tools',
            executable='scan2cart',
            name='scan2cart_front',
            # Optional: Falls du den Parameter für den tf frame hinzufügen möchtest
            parameters=[{'scan_topic': '/laser_scanner_front'},
                        {'pointcloud_topic': '/laser_scanner_front_cart'}]
        ),
        Node(
            package='scan_tools',
            executable='scan2cart',
            name='scan2cart_rear',
            # Optional: Falls du den Parameter für den tf frame hinzufügen möchtest
            parameters=[{'scan_topic': '/laser_scanner_rear'},
                        {'pointcloud_topic': '/laser_scanner_rear_cart'}]
        ),
    ])
