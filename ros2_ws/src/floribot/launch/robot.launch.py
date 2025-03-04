from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os


def generate_launch_description():
    use_sim = DeclareLaunchArgument(
        'use_sim', default_value='false', description='Use simulation mode')

    sim_group = GroupAction(
        condition=IfCondition(use_sim),
        actions=[
            Node(
                package='floribot', executable='own_laserscan_multi_merger',
                parameters=[{'use_sim_time': True}]
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(os.getenv('BASE_PACKAGE_PATH', ''), 'launch', 'base_node.launch.py')
                ),
                launch_arguments={
                    'frontLength': '-0.383',
                    'frontLaserLength': '0.387',
                    'rearLength': '-0.383',
                    'rearLaserLength': '-0.387',
                    'wheelDiameter': '0.280',
                    'axesLength': '0.335',
                    'pubFrequency': '10.0',
                    'stopTimeout': '0.5'
                }.items()
            )
        ]
    )

    real_robot_group = GroupAction(
        condition=UnlessCondition(use_sim),
        actions=[
            Node(
                package='floribot', executable='own_laserscan_multi_merger',
                parameters=[{'use_sim_time': False}]
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(os.getenv('BASE_PACKAGE_PATH', ''), 'launch', 'base_node.launch.py')
                ),
                launch_arguments={
                    'frontLength': '-0.383',
                    'frontLaserLength': '0.327',
                    'rearLength': '-0.383',
                    'rearLaserLength': '-0.327',
                    'wheelDiameter': '0.280',
                    'axesLength': '0.335',
                    'pubFrequency': '10.0',
                    'stopTimeout': '0.2'
                }.items()
            ),
            Node(
                package='base', executable='angle2tf', name='angle2tf'
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(os.getenv('FLORIBOT_PACKAGE_PATH', ''), 'launch', 'own_scanner.launch.py')
                ),
                launch_arguments={
                    'ParentFrame': 'axesFront',
                    'LaserFrame': 'laserFront',
                    'LaserTopic': 'scanFront',
                    'TX': '0.327',
                    'TY': '0',
                    'TZ': '0',
                    'RX': '1',
                    'RY': '0',
                    'RZ': '0',
                    'RW': '0',
                    'IPAddress': '192.168.0.52'
                }.items()
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(os.getenv('FLORIBOT_PACKAGE_PATH', ''), 'launch', 'own_scanner.launch.py')
                ),
                launch_arguments={
                    'ParentFrame': 'axesRear',
                    'LaserFrame': 'laserRear',
                    'LaserTopic': 'scanRear',
                    'TX': '-0.334',
                    'TY': '0',
                    'TZ': '0',
                    'RX': '0',
                    'RY': '-1',
                    'RZ': '0',
                    'RW': '0',
                    'IPAddress': '192.168.0.51'
                }.items()
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(os.getenv('PLC_CONNECTION_PACKAGE_PATH', ''), 'launch', 'plc_connection.launch.py')
                )
            )
        ]
    )

    return LaunchDescription([
        use_sim,
        sim_group,
        real_robot_group
    ])
