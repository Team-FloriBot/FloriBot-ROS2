import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, PushRosNamespace
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Argumente definieren
    return LaunchDescription([
        DeclareLaunchArgument('frontLength', default_value='-0.38'),
        DeclareLaunchArgument('rearLength', default_value='-0.38'),
        DeclareLaunchArgument('wheelDiameter', default_value='0.280'),
        DeclareLaunchArgument('axesLength', default_value='0.335'),

        # Knoten: base_node
        Node(
            package='base',
            executable='base_node',
            name='base',
            output='screen',
            parameters=[{
                'wheelDiameter': LaunchConfiguration('wheelDiameter'),
                'axesLength': LaunchConfiguration('axesLength'),
            }]
        ),
        
        # tf2 static_transform_publisher Knoten
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='AxesFront2JointFront',
            output='screen',
            arguments=[LaunchConfiguration('frontLength'), '0', '0', '0', '0', '0', '1', 'axesFront', 'jointFront']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='AxesRear2JointRear',
            output='screen',
            arguments=[LaunchConfiguration('rearLength'), '0', '0', '0', '0', '0', '1', 'jointRear', 'axesRear']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='Front',
            output='screen',
            arguments=['0', '0', '0', '0', '0', '0', '1', 'base_link', 'axesFront']
        ),
        
        # Remapping
        LogInfo(
            condition=LaunchConfiguration('remap') == 'true',
            msg="Remapping topics"
        ),
    ])

