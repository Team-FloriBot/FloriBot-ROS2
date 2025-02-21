import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    params_file = os.path.join(get_package_share_directory('floribot_simulation'), 'config', 'floribot_parameter.yaml')
    return LaunchDescription([

        # Node starten
        Node(
            package='visu',
            executable='rviz_visu.py',
            name='rviz_visu',
            output='screen',
            parameters=[params_file]  # Parameter: 'drive', 'exit', 'count'
        )
    ])

