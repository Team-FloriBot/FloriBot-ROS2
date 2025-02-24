from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, TextSubstitution, Command
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_path
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
import xacro

def generate_launch_description():
    
    # Verarbeitung der xacro Datei    
    doc = xacro.process_file(os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'))
    robot_desc = doc.toprettyxml(indent='  ')
    # Parameter für den Robot State Publisher
    params = {'robot_description': robot_desc}


    # LaunchDescription
    return LaunchDescription([
 
        # Include maize_navigation Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('maize_navigation'), 'launch'),
                '/maize_navigation.launch.py'])
        ),
	# Include base Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('base'), 'launch'),
                '/base_node.launch.py'])
        ),
        # Include cart_merger Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('scan_tools'), 'launch'),
                '/cart_merger.launch.py'])

        ),
        # Include base2gazebo Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('base2gazebo'), 'launch'),
                '/base2gazebo.launch.py'])

        ),
	# Include plc_connection Launch
        #        IncludeLaunchDescription(
        #    PythonLaunchDescriptionSource([os.path.join(
        #        get_package_share_directory('plc_connection'), 'launch'),
        #        '/plc_connection_launch.py'])
        #),
        
        # Start robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params]
        ),

    ])
