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
    ])
