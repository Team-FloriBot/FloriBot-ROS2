from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, TextSubstitution, Command
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_path
from launch.launch_description_sources import PythonLaunchDescriptionSource
from virtual_maize_field import get_spawner_launch_file
import os
import xacro
import yaml

def generate_launch_description():
    # Define arguments

    paused = LaunchConfiguration('paused', default='False')
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    gui = LaunchConfiguration('gui', default='True')
    headless = LaunchConfiguration('headless', default='False')
    debug = LaunchConfiguration('debug', default='False')
    
    #model_xacro = os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro')
    #xacro_path = LaunchConfiguration('xacro_path', default=os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'))
    doc = xacro.process_file(os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'))
    robot_desc = doc.toprettyxml(indent='  ')
    params = {'robot_description': robot_desc}

        
    rvizconfig = LaunchConfiguration('rvizconfig', default=os.path.join(get_package_share_directory('floribot_simulation'), 'rviz', 'urdf.rviz'))
    #world_path = LaunchConfiguration('world_path', default=os.path.join(get_package_share_directory('virtual_maize_field'), 'worlds', 'generated.world'))
    #world_name = LaunchConfiguration('world_name', default='generated.world')

    config_dir = os.path.join(
        get_package_share_directory('floribot_simulation'), 'config')
    yaml_file = os.path.join(config_dir, 'joints.yaml')

    # Lade die Argumente aus der .yaml-Datei
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
        controllers = config['gazebo']

    # LaunchDescription
    return LaunchDescription([
        # Declare arguments

        DeclareLaunchArgument('paused', default_value='False', description='Paused simulation flag'),
        DeclareLaunchArgument('use_sim_time', default_value='True', description='Use simulation time'),
        DeclareLaunchArgument('gui', default_value='True', description='Enable GUI'),
        DeclareLaunchArgument('headless', default_value='False', description='Enable headless mode'),
        DeclareLaunchArgument('debug', default_value='False', description='Enable debug mode'),
        DeclareLaunchArgument('xacro_path', default_value=os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'), description='URDF model path'),

        #DeclareLaunchArgument('model', default_value=os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro'), description='URDF model path'),
        DeclareLaunchArgument('rvizconfig', default_value=os.path.join(get_package_share_directory('floribot_simulation'), 'rviz', 'urdf.rviz'), description='RViz configuration file'),
        #DeclareLaunchArgument('world_path', default_value=os.path.join(get_package_share_directory('virtual_maize_field'), 'worlds'), description='World path'),
        #DeclareLaunchArgument('world_name', default_value='generated.world', description='World file name'),


        # Launch the Gazebo simulation
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('virtual_maize_field'), 'launch', 'simulation.launch.py')),
        ),
        
        # Include Laserscanners
        #IncludeLaunchDescription(
        #    PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('sick_scan_xd'), 'launch', 'sick_tim_5xx.launch.py'))
        #),
        # Include RViz visualization
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('visu'), 'launch', 'rviz_visu.launch.py'))
        ),

        # Include Base Node

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('maize_navigation'), 'launch'),
                '/maize_navigation.launch.py'])
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

        
        # Start RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            arguments=['-d', LaunchConfiguration('rvizconfig')],
            output='screen',
        ),
        # Joint State Publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'publish_frequency': 30.0}],
            output='screen'
        ),
        # Start robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params]
            #arguments=[model_urdf]
        ),
        Node(
            package='controller_manager',
            executable='spawner.py',
            name='controller_spawner',
            respawn='False',
            arguments=[controllers],
            output='screen'
        ),

        # Robot Spawner (robot model in the world)

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([get_spawner_launch_file()]),
            launch_arguments={"robot_name": "floribot", 
            'initial_joint_pose': '-J j_revolute_front_rear -1.57'}.items(),

        ),

    ])
