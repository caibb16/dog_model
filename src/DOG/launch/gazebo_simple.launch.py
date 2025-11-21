#!/usr/bin/env python3
"""
Gazebo Classic 11.10.2 启动文件
适配 Gazebo Classic 11.x，通过 spawn_entity.py 将机器人加载到仿真环境
"""

import os
import time
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, 
    ExecuteProcess, 
    OpaqueFunction,
    TimerAction
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xml.etree.ElementTree as ET


def add_gazebo_tags_to_urdf(urdf_content, pkg_path):
    """为URDF添加Gazebo物理引擎标签"""
    try:
        root = ET.fromstring(urdf_content)
        
        # 为所有link添加Gazebo标签（如果不存在）
        for link in root.findall('link'):
            link_name = link.get('name')
            # 检查是否已有gazebo标签
            if link.find('gazebo') is None:
                gazebo_tag = ET.Element('gazebo', reference=link_name)
                material = ET.SubElement(gazebo_tag, 'material')
                material.text = 'Gazebo/Grey'
                link.append(gazebo_tag)
        
        # 为所有joint添加Gazebo标签以启用物理仿真
        for joint in root.findall('joint'):
            joint_name = joint.get('name')
            if joint.find('gazebo') is None:
                gazebo_tag = ET.Element('gazebo', reference=joint_name)
                provide_feedback = ET.SubElement(gazebo_tag, 'provideFeedback')
                provide_feedback.text = 'true'
                joint.append(gazebo_tag)
        
        return ET.tostring(root, encoding='unicode')
    except Exception as e:
        print(f"警告: 无法解析URDF: {e}")
        return urdf_content


def spawn_robot(context, *args, **kwargs):
    """延迟生成机器人，确保Gazebo已启动"""
    pkg_dog = get_package_share_directory('DOG')
    urdf_file = os.path.join(pkg_dog, 'urdf', 'DOG.urdf')
    
    with open(urdf_file, 'r') as f:
        robot_description_content = f.read()
    
    # 替换包路径
    robot_description_content = robot_description_content.replace('package://DOG', 'file://' + pkg_dog)
    # 添加Gazebo标签
    robot_description_content = add_gazebo_tags_to_urdf(robot_description_content, pkg_dog)
    
    return [
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'DOG',
                '-x', '0.0',
                '-y', '0.0',
                '-z', '0.5'
            ],
            output='screen'
        )
    ]


def generate_launch_description():
    pkg_dog = get_package_share_directory('DOG')
    world_file = os.path.join(pkg_dog, 'worlds', 'dog_world.sdf')
    urdf_file = os.path.join(pkg_dog, 'urdf', 'DOG.urdf')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', 
        default_value='true', 
        description='Use simulation (Gazebo) clock if true'
    )

    # 读取 URDF 并替换 package:// 路径为绝对路径，添加Gazebo标签
    with open(urdf_file, 'r') as f:
        robot_description_content = f.read()
    robot_description_content = robot_description_content.replace('package://DOG', 'file://' + pkg_dog)
    robot_description_content = add_gazebo_tags_to_urdf(robot_description_content, pkg_dog)

    # Robot State Publisher - 首先启动，确保TF树可用
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }]
    )

    # Joint State Publisher（发布关节状态）
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'publish_frequency': 100.0
        }],
        output='screen'
    )

    # 直接调用 gzserver 和 gzclient，确保加载ROS插件
    gzserver = ExecuteProcess(
        cmd=[
            'gzserver',
            '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so',
            world_file
        ],
        output='screen'
    )

    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    # 延迟生成机器人实体（等待Gazebo充分启动）
    spawn_entity_delayed = TimerAction(
        period=3.0,
        actions=[
            OpaqueFunction(function=spawn_robot)
        ]
    )

    return LaunchDescription([
        declare_use_sim_time,
        robot_state_publisher,
        joint_state_publisher,
        gzserver,
        gzclient,
        spawn_entity_delayed,
    ])
