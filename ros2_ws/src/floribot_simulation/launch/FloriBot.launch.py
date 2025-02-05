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
    # Define arguments

    paused = LaunchConfiguration('paused', default='false')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    gui = LaunchConfiguration('gui', default='true')
    headless = LaunchConfiguration('headless', default='false')
    debug = LaunchConfiguration('debug', default='false')
    
    #model_xacro = os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro')
    #xacro_path = LaunchConfiguration('xacro_path', default=os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'))
    doc = xacro.process_file(os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'))
    robot_desc = doc.toprettyxml(indent='  ')
    params = {'robot_description': robot_desc}

        
    #rvizconfig = LaunchConfiguration('rvizconfig', default=os.path.join(get_package_share_directory('floribot_simulation'), 'rviz', 'urdf.rviz'))
    #world_path = LaunchConfiguration('world_path', default=os.path.join(get_package_share_directory('virtual_maize_field'), 'worlds'))
    #world_name = LaunchConfiguration('world_name', default='generated.world')

    # LaunchDescription
    return LaunchDescription([
        # Declare arguments

        DeclareLaunchArgument('paused', default_value='false', description='Paused simulation flag'),
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation time'),
        DeclareLaunchArgument('gui', default_value='true', description='Enable GUI'),
        DeclareLaunchArgument('headless', default_value='false', description='Enable headless mode'),
        DeclareLaunchArgument('debug', default_value='false', description='Enable debug mode'),
        DeclareLaunchArgument('xacro_path', default_value=os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'), description='URDF model path'),

        #DeclareLaunchArgument('model', default_value=os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'), description='URDF model path'),
        #DeclareLaunchArgument('rvizconfig', default_value=os.path.join(get_package_share_directory('floribot_simulation'), 'rviz', 'urdf.rviz'), description='RViz configuration file'),
        #DeclareLaunchArgument('world_path', default_value=os.path.join(get_package_share_directory('virtual_maize_field'), 'worlds'), description='World path'),
        #DeclareLaunchArgument('world_name', default_value='generated.world', description='World file name'),

        # Include Base Node

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('maize_navigation'), 'launch'),
                '/maize_navigation.launch.py']
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('base'), 'launch'),
                '/base_node.launch.py'])
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('scan_tools'), 'launch'),
                '/cart_merger.launch.py'])

        ),
        #IncludeLaunchDescription(get_package_share_directory('sick_scan_xd') + '/launch/sick_tim_5xx.launch.py'),

        # Start robot_state_publisher

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params]
            #arguments=[model_urdf]
        ),

    ])
