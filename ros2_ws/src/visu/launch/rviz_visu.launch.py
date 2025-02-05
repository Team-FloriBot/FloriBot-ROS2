import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([

        # Node starten
        Node(
            package='visu',
            executable='rviz_visu.py',
            name='rviz_visu',
            output='screen',
            parameters=[{'box': 'drive'}]  # Parameter: 'drive', 'exit', 'count'
        )
    ])
