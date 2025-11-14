#!/usr/bin/env python3
"""
简单测试 - 在 RViz2 中查看模型（无物理仿真）
用于验证 URDF 和网格文件是否正确
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dog = get_package_share_directory('DOG')
    urdf_file = os.path.join(pkg_dog, 'urdf', 'DOG.urdf')
    
    # 读取并转换路径
    with open(urdf_file, 'r') as f:
        robot_description_content = f.read()
    
    robot_description_content = robot_description_content.replace(
        'package://DOG', 'file://' + pkg_dog
    )
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )
    
    # Joint State Publisher GUI
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )
    
    # RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg_dog, 'config', 'rviz', 'dog_view.rviz')] if os.path.exists(os.path.join(pkg_dog, 'config', 'rviz', 'dog_view.rviz')) else []
    )
    
    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz_node
    ])
