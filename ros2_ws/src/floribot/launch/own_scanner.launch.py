from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("ParentFrame", default_value="odom"),
        DeclareLaunchArgument("LaserFrame", default_value="laserFront"),
        DeclareLaunchArgument("LaserTopic", default_value="scanFront"),
        DeclareLaunchArgument("TX", default_value="0"),
        DeclareLaunchArgument("TY", default_value="0"),
        DeclareLaunchArgument("TZ", default_value="-0.1"),
        DeclareLaunchArgument("RX", default_value="0"),
        DeclareLaunchArgument("RY", default_value="0"),
        DeclareLaunchArgument("RZ", default_value="0"),
        DeclareLaunchArgument("RW", default_value="1"),
        DeclareLaunchArgument("IPAddress", default_value="192.168.0.1"),

        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name=LaunchConfiguration("LaserTopic"),
            arguments=[
                LaunchConfiguration("TX"),
                LaunchConfiguration("TY"),
                LaunchConfiguration("TZ"),
                LaunchConfiguration("RX"),
                LaunchConfiguration("RY"),
                LaunchConfiguration("RZ"),
                LaunchConfiguration("RW"),
                LaunchConfiguration("ParentFrame"),
                LaunchConfiguration("LaserFrame")
            ]
        ),

        Node(
            package="sick_scan2",
            executable="sick_generic_caller",
            name=["sick_tim_5xx_", LaunchConfiguration("LaserTopic")],
            output="screen",
            parameters=[{
                "scanner_type": "sick_tim_5xx",
                "min_ang": -2.00712864,
                "max_ang": 2.00712864,
                "use_binary_protocol": True,
                "range_max": 100.0,
                "intensity": True,
                "hostname": LaunchConfiguration("IPAddress"),
                "cloud_topic": ["sensors/", LaunchConfiguration("LaserTopic"), "/cloud"],
                "frame_id": LaunchConfiguration("LaserFrame"),
                "port": "2112",
                "timelimit": 5,
                "sw_pll_only_publish": True
            }],
            remappings=[
                ("scan", ["sensors/", LaunchConfiguration("LaserTopic")])
            ]
        )
    ])