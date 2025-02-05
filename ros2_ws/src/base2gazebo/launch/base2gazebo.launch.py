#!/usr/bin/env python3

import launch
from launch import LaunchDescription
from launch_ros.actions import Node  # Korrekte Import-Quelle

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='base2gazebo',
            executable='PublishWheelSpeed',
            name='base2gazebo',
            output='screen'
        ),
    ])
