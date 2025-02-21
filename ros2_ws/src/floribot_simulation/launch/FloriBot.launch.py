from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from virtual_maize_field import get_spawner_launch_file

import os
import xacro

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    xacro_file = os.path.join(get_package_share_directory('floribot_simulation'), 'urdf', 'Floribot_reduced.urdf.xacro')
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml(), 'use_sim_time': use_sim_time}

    # Robot State Publisher Node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params],
    )

    # Controller initialisieren
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_broad'], output='screen')
    load_controller_fl = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_fl_controller'], output='screen')
    load_controller_fr = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_fr_controller'], output='screen')
    load_controller_rl = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_rl_controller'], output='screen')
    load_controller_rr = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_rr_controller'], output='screen')


    rvizconfig = LaunchConfiguration('rvizconfig', default=os.path.join(get_package_share_directory('floribot_simulation'), 'rviz', 'urdf.rviz'))

    # RViz Node
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        output='screen',
    )

    # LaunchDescription
    return LaunchDescription([
        # Declare arguments
        DeclareLaunchArgument('rvizconfig', default_value=os.path.join(get_package_share_directory('floribot_simulation'), 'rviz', 'urdf.rviz'), description='RViz configuration file'),
              
        #IncludeLaunchDescription(
        #    PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('sick_scan_xd'), 'launch', 'sick_tim_5xx.launch.py')),
        #),

        # Launch the Gazebo simulation
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('virtual_maize_field'), 'launch', 'simulation.launch.py')),
        ),
        # Launch gazebo environment
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(get_package_share_directory('ros_ign_gazebo'), 'launch', 'ign_gazebo.launch.py')])),

        # Include RViz visualization
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('visu'), 'launch', 'rviz_visu.launch.py'))
        ),

        # Include the maize_navigation
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('maize_navigation'), 'launch'), '/maize_navigation.launch.py'])
        ),

        # Include the base
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('base'), 'launch'), '/base_node.launch.py'])
        ),

        # Include the base2gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('base2gazebo'), 'launch'), '/base2gazebo.launch.py'])
        ),

        # Include the scan_tools
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('scan_tools'), 'launch'), '/cart_merger.launch.py'])
        ),

        # Start RViz
        #rviz,
        # Start joint state broadcaster
        load_joint_state_broadcaster,
        # Start robot state publisher
        robot_state_publisher,
        # Start controllers
        load_controller_fl,
        load_controller_fr,
        load_controller_rl,
        load_controller_rr,
        
        # Robot Spawner (robot model in the world)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([get_spawner_launch_file()]),
            launch_arguments={"robot_name": "Floribot"}.items(),
        ),
    ])
