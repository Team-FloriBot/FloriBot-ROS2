import launch
from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription

def generate_launch_description():
    params_file = os.path.join(get_package_share_directory('floribot_simulation'), 'config', 'floribot_parameter.yaml')

    return LaunchDescription([
        
        Node(
            package='maize_navigation',
            executable='maize_navigation',
            name='maize_navigation',
            output='screen',
            parameters=[params_file]  # YAML-Datei wird hier übergeben
        ),
    ])

