import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import sys, termios, tty

JOINTS = [
    "front_left_hip_joint", "front_left_thigh_joint", "front_left_knee_joint",
    "front_right_hip_joint", "front_right_thigh_joint", "front_right_knee_joint",
    "rear_left_hip_joint", "rear_left_thigh_joint", "rear_left_knee_joint",
    "rear_right_hip_joint", "rear_right_thigh_joint", "rear_right_knee_joint"
]

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

class Teleop(Node):
    def __init__(self):
        super().__init__('teleop')
        self.pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

    def send_cmd(self, positions):
        msg = JointTrajectory()
        msg.joint_names = JOINTS

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = 1

        msg.points.append(point)
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = Teleop()

    print("Control with WASD:")
    print("W = forward, S = backward, A/D = turn")

    try:
        while True:
            key = get_key()

            # default standing
            pos = [0.0] * 12

            if key == 'w':
                pos = [0.2, -0.4, 0.6] * 4
            elif key == 's':
                pos = [-0.2, -0.4, 0.6] * 4
            elif key == 'a':
                pos = [0.3, -0.4, 0.6] * 2 + [-0.3, -0.4, 0.6] * 2
            elif key == 'd':
                pos = [-0.3, -0.4, 0.6] * 2 + [0.3, -0.4, 0.6] * 2
            elif key == 'q':
                break

            node.send_cmd(pos)

    except Exception as e:
        print(e)

    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
