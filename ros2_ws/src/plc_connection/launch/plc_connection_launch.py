import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('plc_ip', default_value='192.168.0.43', description='PLC IP address'),
        DeclareLaunchArgument('plc_port', default_value='50000', description='PLC Port'),
        DeclareLaunchArgument('xavier_ip', default_value='192.168.0.42', description='Xavier IP address'),
        DeclareLaunchArgument('xavier_port', default_value='50000', description='Xavier Port'),
        DeclareLaunchArgument('plc_timeout', default_value='1.5', description='PLC Timeout'),
        DeclareLaunchArgument('zero_count_encoder', default_value='41229', description='Zero count encoder'),
        DeclareLaunchArgument('count_per_rotation_encoder', default_value='4096', description='Count per rotation encoder'),
        DeclareLaunchArgument('engine_acceleration', default_value='1000', description='Engine acceleration'),
        DeclareLaunchArgument('engine_jerk', default_value='10000', description='Engine jerk'),
        DeclareLaunchArgument('period_send_read', default_value='0.05', description='Period for sending and reading data'),

        Node(
            package='plc_connection',
            executable='plc_connection_node',
            name='PLC_Connection',
            output='screen',
            parameters=[
                {'PLC_IP': launch.substitutions.LaunchConfiguration('plc_ip')},
                {'PLC_Port': launch.substitutions.LaunchConfiguration('plc_port')},
                {'PLC_Timeout': launch.substitutions.LaunchConfiguration('plc_timeout')},
                {'Xavier_Port': launch.substitutions.LaunchConfiguration('xavier_port')},
                {'Xavier_IP': launch.substitutions.LaunchConfiguration('xavier_ip')},
                {'ZeroCount_Encoder': launch.substitutions.LaunchConfiguration('zero_count_encoder')},
                {'CountPerRotation_Encoder': launch.substitutions.LaunchConfiguration('count_per_rotation_encoder')},
                {'Engine_Acceleration': launch.substitutions.LaunchConfiguration('engine_acceleration')},
                {'Engine_Jerk': launch.substitutions.LaunchConfiguration('engine_jerk')},
                {'Period_Send_Read': launch.substitutions.LaunchConfiguration('period_send_read')}
            ],
            remappings=[
                # Add remaps if needed, for example:
                # ('/engine/actualSpeed', '/engine/actualSpeed')
            ]
        ),
        LogInfo(
            condition=launch.conditions.LaunchConfigurationEquals('plc_ip', '192.168.0.43'),
            msg="PLC IP is set to default value of 192.168.0.43"
        )
    ])
