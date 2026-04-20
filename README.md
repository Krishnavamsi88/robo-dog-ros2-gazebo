# 🐕 Quadruped Robot (RoboDog) — ROS 2 + Gazebo Simulation

A complete, simulation-ready quadruped robot package for ROS 2 with:
- **4 legs × 3 DOF** (hip abduction, thigh swing, knee bend)
- **Head** with camera sensor
- **Tail** with revolute joint
- **IMU** on body
- **Office world** environment in Gazebo
- **Trot gait controller**

---

## 📁 File Structure

```
quadruped_robot/
├── CMakeLists.txt
├── package.xml
├── urdf/
│   └── quadruped.urdf.xacro        ← Main robot model
├── worlds/
│   └── office_world.world          ← Gazebo environment
├── launch/
│   ├── quadruped_gazebo.launch.py  ← Full simulation launch
│   └── quadruped_rviz.launch.py    ← RViz-only launch
├── config/
│   └── quadruped.rviz              ← RViz configuration
└── scripts/
    ├── walking_controller.py       ← Trot gait controller
    └── tf_tree.py                  ← TF tree reference
```

---

## ⚙️ Prerequisites

### ROS 2 (Humble or Iron recommended)
```bash
# Ubuntu 22.04 + ROS 2 Humble
sudo apt update && sudo apt install -y \
  ros-humble-desktop \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-xacro \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-joint-state-publisher-gui \
  ros-humble-tf2-tools \
  ros-humble-rviz2
```

### Source ROS 2
```bash
source /opt/ros/humble/setup.bash
```

---

## 🔨 Build

```bash
# Create workspace (if not already)
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Copy or symlink the package
cp -r /path/to/quadruped_robot .

# Build
cd ~/ros2_ws
colcon build --packages-select quadruped_robot --symlink-install

# Source workspace
source ~/ros2_ws/install/setup.bash
```

---

## 🚀 Run

### Option 1: Full Simulation (Gazebo + RViz)
```bash
# Launch Gazebo with office world + spawn robot
ros2 launch quadruped_robot quadruped_gazebo.launch.py

# With RViz:
ros2 launch quadruped_robot quadruped_gazebo.launch.py rviz:=true

# Custom spawn position:
ros2 launch quadruped_robot quadruped_gazebo.launch.py \
  spawn_x:=0.0 spawn_y:=0.0 spawn_z:=0.35
```

### Option 2: RViz Only (no Gazebo, faster)
```bash
ros2 launch quadruped_robot quadruped_rviz.launch.py
```

---

## 🎮 Walking Controller

### Start the trot gait:
```bash
# In a new terminal (source workspace first):
ros2 run quadruped_robot walking_controller.py

# Or standing pose only:
ros2 run quadruped_robot walking_controller.py stand
```

### Direct joint command (example - send to one joint):
```bash
ros2 topic pub /quadruped/joint_commands sensor_msgs/JointState \
  "{ header: {stamp: {sec: 0}},
     name: ['front_left_thigh_joint'],
     position: [-0.3],
     velocity: [0.0],
     effort: [0.0] }" --once
```

---

## 📡 Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/robot_description` | `std_msgs/String` | URDF string |
| `/joint_states` | `sensor_msgs/JointState` | Current joint positions |
| `/quadruped/joint_commands` | `sensor_msgs/JointState` | Joint position commands |
| `/quadruped/imu/data` | `sensor_msgs/Imu` | IMU data (Gazebo) |
| `/quadruped/camera/image_raw` | `sensor_msgs/Image` | Camera feed |
| `/quadruped/camera/camera_info` | `sensor_msgs/CameraInfo` | Camera calibration |
| `/tf` | `tf2_msgs/TFMessage` | Transform tree |

---

## 🌳 TF Tree

```
base_link
├── head_link  →  camera_link
├── tail_link
├── imu_link
├── front_left_hip  →  front_left_thigh  →  front_left_calf  →  front_left_foot
├── front_right_hip → front_right_thigh  → front_right_calf  → front_right_foot
├── rear_left_hip   →  rear_left_thigh   →  rear_left_calf   →  rear_left_foot
└── rear_right_hip  →  rear_right_thigh  →  rear_right_calf  →  rear_right_foot
```

### View TF tree at runtime:
```bash
ros2 run tf2_tools view_frames
evince frames.pdf
```

---

## 🦿 Joint Reference

| Joint Name | Type | Axis | Limits | DOF |
|-----------|------|------|--------|-----|
| `{leg}_hip_joint` | revolute | Y | ±0.4 rad | Abduction/Adduction |
| `{leg}_thigh_joint` | revolute | X | ±0.785 rad | Swing fwd/back |
| `{leg}_knee_joint` | revolute | X | -1.57 to 0 rad | Knee bend |
| `tail_joint` | revolute | Z | ±0.5 rad | Tail wag |
| `head_joint` | fixed | — | — | Head |
| `camera_joint` | fixed | — | — | Camera |
| `imu_joint` | fixed | — | — | IMU |
| `{leg}_foot_joint` | fixed | — | — | Foot sphere |

Where `{leg}` ∈ {front_left, front_right, rear_left, rear_right}

---

## 🔧 Physical Parameters

| Component | Mass | Notes |
|-----------|------|-------|
| base_link | 2.5 kg | Body chassis |
| head_link | 0.15 kg | Spherical head |
| tail_link | 0.05 kg | Thin cylinder |
| hip_link (each) | 0.15 kg | Servo housing |
| thigh_link (each) | 0.20 kg | Upper leg |
| calf_link (each) | 0.12 kg | Lower leg |
| foot_link (each) | 0.04 kg | Rubber sphere |
| **Total** | **~4.0 kg** | |

---

## 🏢 Gazebo World Objects

| Object | Position | Description |
|--------|----------|-------------|
| Ground plane | (0,0,0) | Entire floor |
| Office floor | (0,0,0) | Wood texture overlay |
| Walls (N/S/E/W) | ±5m | 10m × 10m room |
| Desk | (3,1,0.75) | Table + legs + laptop |
| Red box | (-2,2,0) | Large obstacle |
| Green box | (1.5,-2,0) | Small rotated obstacle |
| Yellow pillar | (-1.5,-3,0) | Tall thin obstacle |
| Orange crate | (-3,0.5,0) | Medium obstacle |
| Purple step | (0,-2.5,0) | Low step obstacle |

---

## 🐛 Troubleshooting

### Robot falls on spawn
- Increase `spawn_z` (default 0.35 m is correct for this model)
- Check joint damping values in the URDF
- Ensure Gazebo physics step size is 0.001 (default)

### URDF parse errors
```bash
# Validate xacro expansion
ros2 run xacro xacro urdf/quadruped.urdf.xacro > /tmp/quadruped_expanded.urdf
check_urdf /tmp/quadruped_expanded.urdf
```

### Gazebo not finding world
```bash
echo $GAZEBO_RESOURCE_PATH
# Should include your package's worlds/ directory
```

### Camera image not showing in RViz
- Make sure Gazebo is running and the robot is spawned
- Check topic: `ros2 topic list | grep camera`
- Try `ros2 topic echo /quadruped/camera/image_raw --no-arr`

---

## 🎓 Extending This Package

### Adding ros2_control
1. Add `<ros2_control>` block to the URDF
2. Add `ros2_control.launch.py` with controller manager
3. Load `joint_trajectory_controller` for each leg

### Adding a LiDAR
Add to the URDF:
```xml
<gazebo reference="lidar_link">
  <sensor name="lidar" type="ray">
    <ray>...</ray>
    <plugin name="lidar_plugin" filename="libgazebo_ros_ray_sensor.so">
      ...
    </plugin>
  </sensor>
</gazebo>
```

### Connecting to nav2
- Add an odometry plugin to base_link
- Publish `/odom` → `/base_link` transform
- Configure `nav2_bringup` with appropriate costmaps

---

## 📜 License
Apache-2.0 — Free to use and modify.
