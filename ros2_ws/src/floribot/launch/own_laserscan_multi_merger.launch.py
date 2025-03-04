import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare the launch arguments
    return LaunchDescription([
        
        DeclareLaunchArgument('destination_frame', default_value='laserFront'),
        DeclareLaunchArgument('cloud_destination_topic', default_value='/merged_cloud'),  
        DeclareLaunchArgument('scan_destination_topic', default_value='/sensors/scanMulti'),
        DeclareLaunchArgument('laserscan_topics', default_value='/sensors/scanFront /sensors/scanRear'), 
        DeclareLaunchArgument('angle_min', default_value='-3.14159265359'),
        DeclareLaunchArgument('angle_max', default_value='3.14159265359'),
        DeclareLaunchArgument('angle_increment', default_value='0.005817763973027468'),
        DeclareLaunchArgument('scan_time', default_value='0.0667'),
        DeclareLaunchArgument('range_min', default_value='0.05'),
        DeclareLaunchArgument('range_max', default_value='25.0'),

        # Define the node
        Node(
            package='ira_laser_tools',
            #executable='plc_connection_node',
            name='laserscan_multi_merger',
            output='screen',
            parameters=[{
                'destination_frame': LaunchConfiguration('destination_frame'),
                'cloud_destination_topic': LaunchConfiguration('cloud_destination_topic'),
                'scan_destination_topic': LaunchConfiguration('scan_destination_topic'),
                'laserscan_topics': LaunchConfiguration('laserscan_topics'),
                'angle_min': LaunchConfiguration('angle_min'),
                'angle_max': LaunchConfiguration('angle_max'),
                'angle_increment': LaunchConfiguration('angle_increment'),
                'scan_time': LaunchConfiguration('scan_time'),
                'range_min': LaunchConfiguration('range_min'),
                'range_max': LaunchConfiguration('range_max'),
            }],
        ),
    ])
