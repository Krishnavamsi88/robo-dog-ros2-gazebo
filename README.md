# 🐕 Robo Dog — ROS 2 Jazzy + Gazebo Simulation

<p align="center">
  <strong>Quadruped Robot Simulation using ROS 2 Jazzy, Gazebo Sim and RViz2</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/ROS%202-Jazzy-blue?style=for-the-badge" alt="ROS 2 Jazzy">
  <img src="https://img.shields.io/badge/Gazebo-Sim-orange?style=for-the-badge" alt="Gazebo Sim">
  <img src="https://img.shields.io/badge/RViz2-Visualization-green?style=for-the-badge" alt="RViz2">
  <img src="https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python" alt="Python">
</p>

---

## 📌 Project Overview

**Robo Dog** is a simulation-based quadruped robot developed using **ROS 2 Jazzy**, **Gazebo Sim** and **RViz2**.

The project focuses on designing, simulating and controlling a four-legged robot in a custom virtual environment. The robot is modelled using **URDF/Xacro**, visualized using RViz2, and simulated in Gazebo Sim.

The project provides a safe simulation environment for experimenting with robot modelling, joint control, teleoperation, sensors, TF relationships and walking behaviour before moving toward physical hardware.

---

## 🎯 Objectives

- Design a four-legged quadruped robot using URDF/Xacro.
- Simulate the robot in Gazebo Sim.
- Visualize the robot and its coordinate frames in RViz2.
- Test robot joints and movement.
- Implement keyboard-based teleoperation.
- Develop a basic walking/gait controller.
- Explore simulated sensors.
- Understand ROS 2 nodes, topics and robot communication.
- Build a reusable simulation platform for future robotics development.

---

## 🧠 System Architecture

```text
                    ┌─────────────────┐
                    │    ROS 2 Jazzy  │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     URDF / Xacro       Controllers       Teleoperation
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                    ┌─────────────────┐
                    │   Gazebo Sim    │
                    │    gz-sim       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           Sensors       Joint States   Robot Motion
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    ┌─────────────────┐
                    │      RViz2      │
                    │ Visualization    │
                    └─────────────────┘

---

## 🤖 Robot Features

### Quadruped Structure

- Four-legged quadruped robot
- Multi-joint leg structure
- Hip, thigh and knee joints
- Head and tail structures
- Foot links
- URDF/Xacro based robot model

### Control

- 🎮 Keyboard teleoperation
- 🦿 Basic walking/gait controller
- 🧍 Joint movement testing
- 📊 Joint-state visualization
- 🌳 TF visualization

### Simulation

- Gazebo Sim environment
- RViz2 visualization
- Simulated robot sensors
- ROS 2 communication
- Custom office-style world

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **ROS 2 Jazzy** | Robot middleware and communication |
| **Gazebo Sim** | Physics and robot simulation |
| **RViz2** | Robot visualization |
| **URDF / Xacro** | Robot modelling |
| **Python** | Controllers and robotics scripts |
| **CMake** | ROS 2 package build system |
| **colcon** | Workspace build tool |
| **TF2** | Coordinate-frame management |

---

## 📂 Project Structure

```text
quadruped_robot/
├── config/
├── launch/
├── scripts/
├── urdf/
├── worlds/
├── screenshots/
├── teleop_keyboard.py
├── CMakeLists.txt
├── package.xml
└── README.md
