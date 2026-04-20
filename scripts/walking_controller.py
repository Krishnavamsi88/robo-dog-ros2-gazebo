#!/usr/bin/env python3
"""
Quadruped Robot - Simple Trot Gait Controller
==============================================
Publishes joint positions to drive the robot in a trot gait.

TROT GAIT: Diagonal pairs move together:
  Phase A: Front-Left + Rear-Right swing
  Phase B: Front-Right + Rear-Left swing

Topics published:
  /quadruped/joint_commands (sensor_msgs/JointState)
  OR individual joint effort topics (for ros2_control)

Usage (standalone test, no ros2_control):
  ros2 run quadruped_robot walking_controller.py

You can tune the gait parameters at the top of this file.
"""

import rclpy
from rclpy.node import Node
import math
import time
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


# ── Gait Parameters ────────────────────────────────────────────────────────────
GAIT_PERIOD     = 1.2    # seconds per full gait cycle
STEP_HEIGHT     = 0.04   # metres, foot lift height
STEP_LENGTH     = 0.06   # metres, step forward length
BODY_HEIGHT     = -0.18  # thigh angle offset to hold body up (radians)
PUBLISH_RATE    = 50     # Hz

# Default standing joint angles (radians)
# hip=0, thigh ~ -0.3 (body weight), knee ~ 0.9 (bent)
STAND_HIP       =  0.00
STAND_THIGH     = -0.30
STAND_KNEE      =  0.90


class TrotGaitController(Node):
    """
    Generates sinusoidal trot gait and publishes joint states.
    """

    def __init__(self):
        super().__init__("trot_gait_controller")

        # Joint names in order (must match URDF)
        self.joint_names = [
            "front_left_hip_joint",   "front_left_thigh_joint",   "front_left_knee_joint",
            "front_right_hip_joint",  "front_right_thigh_joint",  "front_right_knee_joint",
            "rear_left_hip_joint",    "rear_left_thigh_joint",    "rear_left_knee_joint",
            "rear_right_hip_joint",   "rear_right_thigh_joint",   "rear_right_knee_joint",
            "tail_joint",
        ]

        # Publisher for joint states
        self.pub = self.create_publisher(JointState, "/quadruped/joint_commands", 10)

        # Timer for gait loop
        self.timer = self.create_timer(1.0 / PUBLISH_RATE, self.gait_callback)

        self.t0 = time.time()
        self.get_logger().info("Trot gait controller started.")
        self.get_logger().info(f"  Period:      {GAIT_PERIOD}s")
        self.get_logger().info(f"  Step height: {STEP_HEIGHT}m")
        self.get_logger().info(f"  Step length: {STEP_LENGTH}m")

    # ── Helper: swing-phase profile ───────────────────────────────────────────

    def swing_profile(self, phase: float, amplitude: float) -> float:
        """
        Returns a sinusoidal position offset for a leg in swing.
        phase: 0.0 → 1.0 (fraction of gait cycle)
        """
        return amplitude * math.sin(math.pi * phase)

    # ── Main gait callback ────────────────────────────────────────────────────

    def gait_callback(self):
        t   = time.time() - self.t0
        phi = (t % GAIT_PERIOD) / GAIT_PERIOD  # 0 → 1

        # Trot: FL+RR are in phase A, FR+RL are in phase B (180° offset)
        phase_A = phi               # front_left, rear_right
        phase_B = (phi + 0.5) % 1  # front_right, rear_left

        # ── Thigh (forward/back swing) + knee (lift) ─────────────────────────

        def leg_angles(phase):
            """Return (thigh_delta, knee_delta) for a given gait phase."""
            # Thigh: forward during first half, back during second half
            thigh_delta = STEP_LENGTH * 3.0 * math.sin(2 * math.pi * phase)
            # Knee: lift during swing (first half), plant during stance (second half)
            if phase < 0.5:
                knee_delta = STEP_HEIGHT * 8.0 * math.sin(math.pi * (phase / 0.5))
            else:
                knee_delta = 0.0
            return thigh_delta, knee_delta

        th_A, kn_A = leg_angles(phase_A)
        th_B, kn_B = leg_angles(phase_B)

        # ── Assemble position vector ─────────────────────────────────────────
        #  Order: FL hip/thigh/knee, FR hip/thigh/knee, RL hip/thigh/knee, RR hip/thigh/knee, tail

        positions = [
            # Front Left (phase A)
            STAND_HIP,
            STAND_THIGH + th_A,
            STAND_KNEE  - kn_A,

            # Front Right (phase B)
            STAND_HIP,
            STAND_THIGH + th_B,
            STAND_KNEE  - kn_B,

            # Rear Left (phase B)
            STAND_HIP,
            STAND_THIGH + th_B,
            STAND_KNEE  - kn_B,

            # Rear Right (phase A)
            STAND_HIP,
            STAND_THIGH + th_A,
            STAND_KNEE  - kn_A,

            # Tail: gentle wag
            0.25 * math.sin(2 * math.pi * phi * 2),
        ]

        # ── Publish ───────────────────────────────────────────────────────────
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name         = self.joint_names
        msg.position     = positions
        msg.velocity     = [0.0] * len(self.joint_names)
        msg.effort       = [0.0] * len(self.joint_names)

        self.pub.publish(msg)


# ── Standing pose publisher (one-shot) ────────────────────────────────────────

class StandController(Node):
    """
    Publishes a static standing pose once, then keeps republishing.
    Useful to verify the robot stands correctly before walking.
    """

    def __init__(self):
        super().__init__("stand_controller")

        self.joint_names = [
            "front_left_hip_joint",   "front_left_thigh_joint",   "front_left_knee_joint",
            "front_right_hip_joint",  "front_right_thigh_joint",  "front_right_knee_joint",
            "rear_left_hip_joint",    "rear_left_thigh_joint",    "rear_left_knee_joint",
            "rear_right_hip_joint",   "rear_right_thigh_joint",   "rear_right_knee_joint",
            "tail_joint",
        ]

        self.positions = [
            STAND_HIP, STAND_THIGH, STAND_KNEE,  # FL
            STAND_HIP, STAND_THIGH, STAND_KNEE,  # FR
            STAND_HIP, STAND_THIGH, STAND_KNEE,  # RL
            STAND_HIP, STAND_THIGH, STAND_KNEE,  # RR
            0.0,                                  # tail
        ]

        self.pub   = self.create_publisher(JointState, "/quadruped/joint_commands", 10)
        self.timer = self.create_timer(0.05, self.publish_stand)
        self.get_logger().info("Standing controller started — publishing stand pose.")

    def publish_stand(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name         = self.joint_names
        msg.position     = self.positions
        msg.velocity     = [0.0] * len(self.joint_names)
        msg.effort       = [0.0] * len(self.joint_names)
        self.pub.publish(msg)


# ── Entry point ───────────────────────────────────────────────────────────────

def main(args=None):
    rclpy.init(args=args)

    import sys
    mode = "trot"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode == "stand":
        node = StandController()
    else:
        node = TrotGaitController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
