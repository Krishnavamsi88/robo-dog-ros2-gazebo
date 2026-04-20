#!/usr/bin/env python3
"""
TF Tree Structure for Quadruped Robot
======================================
Run this to print the expected TF tree, or use:
  ros2 run tf2_tools view_frames

Expected tree:
  world (if using /gazebo)
  └── base_link
      ├── head_joint      → head_link
      │   └── camera_joint → camera_link
      ├── tail_joint       → tail_link  (revolute)
      ├── imu_joint        → imu_link
      │
      ├── front_left_hip_joint   → front_left_hip
      │   └── front_left_thigh_joint → front_left_thigh
      │       └── front_left_knee_joint → front_left_calf
      │           └── front_left_foot_joint → front_left_foot
      │
      ├── front_right_hip_joint  → front_right_hip
      │   └── front_right_thigh_joint → front_right_thigh
      │       └── front_right_knee_joint → front_right_calf
      │           └── front_right_foot_joint → front_right_foot
      │
      ├── rear_left_hip_joint    → rear_left_hip
      │   └── rear_left_thigh_joint  → rear_left_thigh
      │       └── rear_left_knee_joint   → rear_left_calf
      │           └── rear_left_foot_joint   → rear_left_foot
      │
      └── rear_right_hip_joint   → rear_right_hip
          └── rear_right_thigh_joint → rear_right_thigh
              └── rear_right_knee_joint  → rear_right_calf
                  └── rear_right_foot_joint  → rear_right_foot

Joint types:
  hip_joint    : revolute  (axis Y → abduction/adduction)
  thigh_joint  : revolute  (axis X → forward/backward)
  knee_joint   : revolute  (axis X → bending)
  foot_joint   : fixed
  head_joint   : fixed
  tail_joint   : revolute  (axis Z → wag)
  imu_joint    : fixed
  camera_joint : fixed
"""

TF_TREE = {
    "base_link": {
        "head_link": {
            "camera_link": {}
        },
        "tail_link": {},
        "imu_link": {},
        "front_left_hip": {
            "front_left_thigh": {
                "front_left_calf": {
                    "front_left_foot": {}
                }
            }
        },
        "front_right_hip": {
            "front_right_thigh": {
                "front_right_calf": {
                    "front_right_foot": {}
                }
            }
        },
        "rear_left_hip": {
            "rear_left_thigh": {
                "rear_left_calf": {
                    "rear_left_foot": {}
                }
            }
        },
        "rear_right_hip": {
            "rear_right_thigh": {
                "rear_right_calf": {
                    "rear_right_foot": {}
                }
            }
        },
    }
}


def print_tree(tree: dict, indent: int = 0):
    for parent, children in tree.items():
        prefix = "    " * indent + ("└── " if indent > 0 else "")
        print(f"{prefix}{parent}")
        print_tree(children, indent + 1)


if __name__ == "__main__":
    print("\n=== Quadruped Robot TF Tree ===\n")
    print_tree(TF_TREE)
    print("\nTotal links: 21")
    print("Total joints: 20 (13 revolute, 7 fixed)\n")
    print("To visualize in ROS 2:")
    print("  ros2 run tf2_tools view_frames")
    print("  evince frames.pdf\n")
