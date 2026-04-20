import sys
import termios
import tty
import subprocess

def get_key():
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def move_joint(joint, value):
    cmd = f'gz topic -t {joint} -m gz.msgs.Double -p "data: {value}"'
    subprocess.call(cmd, shell=True)

print("W/S/A/D to move, Q to quit")

while True:
    key = get_key()

    if key == 'w':
        print("Forward")
        move_joint("/model/quadruped_robot/joint/front_left_thigh_joint/0/cmd_pos", -0.3)
        move_joint("/model/quadruped_robot/joint/front_right_thigh_joint/0/cmd_pos", -0.3)

    elif key == 's':
        print("Backward")
        move_joint("/model/quadruped_robot/joint/rear_left_thigh_joint/0/cmd_pos", -0.3)
        move_joint("/model/quadruped_robot/joint/rear_right_thigh_joint/0/cmd_pos", -0.3)

    elif key == 'a':
        print("Left")
        move_joint("/model/quadruped_robot/joint/front_left_hip_joint/0/cmd_pos", 0.3)

    elif key == 'd':
        print("Right")
        move_joint("/model/quadruped_robot/joint/front_right_hip_joint/0/cmd_pos", -0.3)

    elif key == 'q':
        print("Exit")
        break
