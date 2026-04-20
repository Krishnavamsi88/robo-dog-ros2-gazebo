#!/usr/bin/env python3
"""
ROS 2 Launch File for Quadruped Robot (RoboDog)
================================================
Launches:
  1. Gazebo with office_world.world
  2. Robot spawner (spawn quadruped URDF from xacro)
  3. Robot State Publisher (TF tree)
  4. Joint State Publisher GUI (manual joint control)
  5. RViz2 (optional, set rviz:=true)

Usage:
  ros2 launch quadruped_robot quadruped_gazebo.launch.py
  ros2 launch quadruped_robot quadruped_gazebo.launch.py rviz:=true
  ros2 launch quadruped_robot quadruped_gazebo.launch.py use_sim_time:=true rviz:=true
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    ExecuteProcess,
    RegisterEventHandler,
    LogInfo,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # ── Package paths ─────────────────────────────────────────────────────────
    pkg_name        = "quadruped_robot"
    pkg_share       = get_package_share_directory(pkg_name)
    urdf_dir        = os.path.join(pkg_share, "urdf")
    world_dir       = os.path.join(pkg_share, "worlds")
    config_dir      = os.path.join(pkg_share, "config")
    rviz_config     = os.path.join(config_dir, "quadruped.rviz")

    xacro_file      = os.path.join(urdf_dir,  "quadruped.urdf.xacro")
    world_file      = os.path.join(world_dir, "office_world.world")

    # ── Declare launch arguments ──────────────────────────────────────────────
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock",
    )

    rviz_arg = DeclareLaunchArgument(
        "rviz",
        default_value="false",
        description="Launch RViz2 alongside Gazebo",
    )

    x_arg = DeclareLaunchArgument("spawn_x", default_value="0.0",  description="Robot spawn X")
    y_arg = DeclareLaunchArgument("spawn_y", default_value="0.0",  description="Robot spawn Y")
    z_arg = DeclareLaunchArgument("spawn_z", default_value="0.35", description="Robot spawn Z (above ground)")
    yaw_arg = DeclareLaunchArgument("spawn_yaw", default_value="0.0", description="Robot spawn yaw")

    # ── LaunchConfiguration references ───────────────────────────────────────
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz     = LaunchConfiguration("rviz")
    spawn_x      = LaunchConfiguration("spawn_x")
    spawn_y      = LaunchConfiguration("spawn_y")
    spawn_z      = LaunchConfiguration("spawn_z")
    spawn_yaw    = LaunchConfiguration("spawn_yaw")

    # ── Robot description (xacro → URDF string) ───────────────────────────────
    robot_description_content = Command(
        [FindExecutable(name="xacro"), " ", xacro_file]
    )
    robot_description = {"robot_description": robot_description_content}

    # ── Robot State Publisher ─────────────────────────────────────────────────
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            robot_description,
            {"use_sim_time": use_sim_time},
        ],
    )

    # ── Joint State Publisher GUI (for manual testing) ────────────────────────
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )

    # ── Gazebo (with office world) ────────────────────────────────────────────
    gazebo_env = {
        "GAZEBO_MODEL_PATH": os.path.join(pkg_share, "models"),
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("gazebo_ros"),
                    "launch",
                    "gazebo.launch.py",
                )
            ]
        ),
        launch_arguments={
            "world": world_file,
            "verbose": "false",
            "pause": "false",
        }.items(),
    )

    # ── Spawn robot entity in Gazebo ──────────────────────────────────────────
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_quadruped",
        arguments=[
            "-topic", "robot_description",
            "-entity", "quadruped_robot",
            "-x", spawn_x,
            "-y", spawn_y,
            "-z", spawn_z,
            "-Y", spawn_yaw,
        ],
        output="screen",
    )

    # ── RViz2 (optional) ──────────────────────────────────────────────────────
    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config] if os.path.exists(rviz_config) else [],
        parameters=[{"use_sim_time": use_sim_time}],
        condition=IfCondition(use_rviz),
    )

    # ── Assemble LaunchDescription ────────────────────────────────────────────
    return LaunchDescription(
        [
            # Arguments
            use_sim_time_arg,
            rviz_arg,
            x_arg, y_arg, z_arg, yaw_arg,

            # Nodes / processes
            robot_state_publisher,
            gazebo,
            # Delay spawn until Gazebo is ready
            TimerAction(period=3.0, actions=[spawn_entity]),
            # Delay joint_state_publisher_gui
            TimerAction(period=4.0, actions=[joint_state_publisher_gui]),
            rviz2,

            LogInfo(msg="=== Quadruped Robot Launch Complete ==="),
        ]
    )
