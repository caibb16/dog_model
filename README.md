# 四足机器人仿真项目

## 项目状态

- ✅ **RViz2 可视化** - 已完成
- ✅ **Gazebo Harmonic 仿真** - 已完成（2025年11月14日）

## 快速开始

### RViz2 可视化（无物理仿真）
```bash
source install/setup.bash
ros2 launch DOG display.launch.py
```

### Gazebo Harmonic 物理仿真
```bash
source install/setup.bash
ros2 launch DOG gazebo_simple.launch.py
```


## 机器人规格

- **类型**: 四足机器人
- **关节数**: 12 个可活动关节（每条腿 3 个）
- **腿部**: FL (前左), FR (前右), RL (后左), RR (后右)
- **每条腿关节**: ABAD (外展/内收), HIP (髋关节), KNEE (膝关节)

## 环境要求

- ROS 2 (Humble/Jazzy)
- Gazebo Harmonic (8.x)
- Python 3
- 相关 ROS 包（见 `package.xml`）

## 编译

```bash
colcon build --symlink-install
source install/setup.bash
```

## 环境检查

```bash
./check_gazebo_env.sh
```
