#!/usr/bin/env python3
"""
RViz2 Only Launch File
======================
Use this to visualize the robot model without Gazebo.
Launches robot_state_publisher + joint_state_publisher_gui + rviz2.

Usage:
  ros2 launch quadruped_robot quadruped_rviz.launch.py
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, FindExecutable
def generate_launch_description():

    pkg_share   = get_package_share_directory("quadruped_robot")
    xacro_file  = os.path.join(pkg_share, "urdf", "quadruped.urdf.xacro")
    rviz_config = os.path.join(pkg_share, "config", "quadruped.rviz")

    robot_description_content = Command(
        [FindExecutable(name="xacro"), " ", xacro_file]
    )
    robot_description = {
    "robot_description": ParameterValue(
        robot_description_content,
        value_type=str
    )
   }

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description, {"use_sim_time": False}],
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config] if os.path.exists(rviz_config) else [],
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz2,
    ])
