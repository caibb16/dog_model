# 🐕 四足机器人仿真 - 快速参考

## 🚀 一键启动

```bash
cd /home/cai/dog_model-master
source install/setup.bash
ros2 launch DOG gazebo_simple.launch.py
```

---

## 📋 常用命令

### 启动仿真
| 命令 | 说明 |
|------|------|
| `ros2 launch DOG gazebo_simple.launch.py` | Gazebo 仿真 + GUI 控制 |
| `ros2 launch DOG gazebo_harmonic.launch.py` | 完整仿真 + ros2_control |
| `ros2 launch DOG display.launch.py` | 仅 RViz2 可视化 |

### 查看状态
| 命令 | 说明 |
|------|------|
| `ros2 topic list` | 查看所有话题 |
| `ros2 topic echo /joint_states` | 查看关节状态 |
| `gz topic -l` | 查看 Gazebo 话题 |
| `gz model -l` | 查看模型列表 |

### 控制关节
```bash
# 发布关节位置（12个关节）
ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray \
  "data: [0.0, 0.0, -1.5, 0.0, 0.0, -1.5, 0.0, 0.0, -1.5, 0.0, 0.0, -1.5]"
```

---

## 🦿 关节布局

```
        前腿                      后腿
    FL          FR          RL          RR
    ↓           ↓           ↓           ↓
  ABAD        ABAD        ABAD        ABAD    ← 外展/内收
  HIP         HIP         HIP         HIP     ← 髋关节
  KNEE        KNEE        KNEE        KNEE    ← 膝关节
```

**关节顺序（数组索引 0-11）：**
```
[FL_ABAD, FL_HIP, FL_KNEE,    # 索引 0-2
 FR_ABAD, FR_HIP, FR_KNEE,    # 索引 3-5
 RR_ABAD, RR_HIP, RR_KNEE,    # 索引 6-8
 RL_ABAD, RL_HIP, RL_KNEE]    # 索引 9-11
```

---

## 🔧 维护命令

### 编译
```bash
colcon build --symlink-install
source install/setup.bash
```

### 清理
```bash
rm -rf build/ install/ log/
colcon build --symlink-install
```

### 环境检查
```bash
./check_gazebo_env.sh
```

---

## 📁 关键文件位置

```
src/DOG/
├── urdf/
│   ├── DOG.urdf              # 机器人描述
│   ├── DOG.xacro             # 主 xacro 文件
│   └── DOG.gazebo.xacro      # Gazebo 配置
├── launch/
│   ├── gazebo_simple.launch.py     # 简单启动 ⭐
│   └── gazebo_harmonic.launch.py   # 完整启动
├── config/
│   └── controller.yaml       # 控制器配置
└── meshes/                   # STL 网格文件
```

---

## ⚡ 快捷技巧

### 1. 快速重启仿真
```bash
# Ctrl+C 停止，然后：
ros2 launch DOG gazebo_simple.launch.py
```

### 2. 同时打开多个终端
```bash
# 终端 1：启动仿真
ros2 launch DOG gazebo_simple.launch.py

# 终端 2：监控状态
ros2 topic echo /joint_states

# 终端 3：发送命令
ros2 topic pub /joint_states ...
```

### 3. 保存关节配置
```bash
# 记录当前姿态
ros2 topic echo /joint_states -1 > pose_standing.yaml
```

---

## 🐛 常见错误速查

| 错误 | 解决方案 |
|------|----------|
| `Unable to find file [model://DOG/...]` | ✅ 已修复！重新启动即可 |
| `Could not find package "ros_gz_sim"` | `sudo apt install ros-${ROS_DISTRO}-ros-gz-sim` |
| Gazebo 无法启动 | `killall -9 gz` 然后重试 |
| 机器人快速掉落 | 在 GUI 中拖动关节到支撑姿态 |

详细故障排除 → [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)

---

## 📚 文档导航

- 📖 [`README.md`](README.md) - 项目概述
- 🚀 [`QUICKSTART.md`](QUICKSTART.md) - 快速入门
- 📘 [`GAZEBO_HARMONIC_GUIDE.md`](GAZEBO_HARMONIC_GUIDE.md) - 详细指南
- 🔧 [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - 故障排除
- 📂 [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) - 项目结构

---

## 🎯 姿态示例

### 站立姿态（示例值）
```python
standing_pose = [
    0.0, 0.7, -1.4,   # FL: ABAD, HIP, KNEE
    0.0, 0.7, -1.4,   # FR
    0.0, 0.7, -1.4,   # RR
    0.0, 0.7, -1.4    # RL
]
```

### 趴下姿态（示例值）
```python
lying_pose = [
    0.0, 1.5, -2.7,   # FL
    0.0, 1.5, -2.7,   # FR
    0.0, 1.5, -2.7,   # RR
    0.0, 1.5, -2.7    # RL
]
```

---

**💡 提示：** 将此文件加入书签以便快速查阅！

**最后更新：** 2025年11月14日
