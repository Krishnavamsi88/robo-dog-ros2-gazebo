from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
import os

def generate_launch_description():

    world_path = os.path.join(
        os.getenv('HOME'),
        'ros2_ws/src/quadruped_robot/worlds/office_world.world'
    )

    urdf_path = os.path.join(
        os.getenv('HOME'),
        'ros2_ws/src/quadruped_robot/urdf/quadruped.urdf'
    )

    return LaunchDescription([

        # 1️⃣ Start Gazebo
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_path],
            output='screen'
        ),

        # 2️⃣ Spawn robot AFTER delay (IMPORTANT)
        TimerAction(
            period=3.0,   # wait 3 seconds
            actions=[
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    arguments=[
                        '-name', 'quadruped',
                        '-file', urdf_path,
                        '-z', '0.3'
                    ],
                    output='screen'
                )
            ]
        )
    ])
