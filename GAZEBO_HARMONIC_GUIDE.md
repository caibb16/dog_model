# Gazebo Harmonic 仿真使用指南

## 概述
本项目已配置支持 Gazebo Harmonic 进行四足机器人仿真。

## 前置要求

### 1. 安装 Gazebo Harmonic
```bash
# Ubuntu 22.04/24.04
sudo apt-get update
sudo apt-get install gz-harmonic
```

### 2. 安装 ROS 2 Gazebo 集成包
```bash
sudo apt-get install ros-${ROS_DISTRO}-ros-gz-sim \
                     ros-${ROS_DISTRO}-ros-gz-bridge \
                     ros-${ROS_DISTRO}-gz-ros2-control \
                     ros-${ROS_DISTRO}-ros2-control \
                     ros-${ROS_DISTRO}-ros2-controllers \
                     ros-${ROS_DISTRO}-joint-state-publisher-gui
```

## 编译项目

```bash
cd /home/cai/dog_model-master
colcon build --symlink-install
source install/setup.bash
```

## 启动仿真

### 方法 1: 简单启动（推荐用于初次测试）
```bash
ros2 launch DOG gazebo_simple.launch.py
```

这将启动：
- Gazebo Harmonic 空世界
- 四足机器人模型（在 z=0.5m 高度生成）
- Joint State Publisher GUI（用于手动控制关节）
- Robot State Publisher（发布TF变换）
- 时钟桥接

### 方法 2: 完整启动（带 ros2_control）
```bash
ros2 launch DOG gazebo_harmonic.launch.py
```

可选参数：
- `rviz:=true` - 同时启动 RViz2
- `gui:=false` - 无头模式运行
- `world:=/path/to/world.sdf` - 加载自定义世界

### 方法 3: 同时启动 RViz2
```bash
ros2 launch DOG gazebo_harmonic.launch.py rviz:=true
```

## 控制机器人

### 手动控制关节（使用 GUI）
启动简单版本后会自动打开 Joint State Publisher GUI，可以通过滑块控制各个关节。

### 通过命令行发布关节位置
```bash
# 查看可用话题
ros2 topic list

# 发布单个关节命令（示例）
ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray \
  "data: [0.0, 0.0, -1.5, 0.0, 0.0, -1.5, 0.0, 0.0, -1.5, 0.0, 0.0, -1.5]"
```

关节顺序（共12个）：
1. FL_ABAD_JOINT, FL_HIP_JOINT, FL_KNEE_JOINT
2. FR_ABAD_JOINT, FR_HIP_JOINT, FR_KNEE_JOINT
3. RR_ABAD_JOINT, RR_HIP_JOINT, RR_KNEE_JOINT
4. RL_ABAD_JOINT, RL_HIP_JOINT, RL_KNEE_JOINT

### 查看关节状态
```bash
ros2 topic echo /joint_states
```

## 验证仿真

### 检查 Gazebo 是否正常运行
```bash
gz sim --version
gz topic -l
```

### 检查 ROS 话题
```bash
ros2 topic list
ros2 topic echo /robot_description
```

### 检查 TF 树
```bash
ros2 run tf2_tools view_frames
```

## 文件说明

### 新增/修改的文件：
- `urdf/DOG.xacro` - 主 xacro 文件（整合原始 URDF 和 Gazebo 配置）
- `urdf/DOG.gazebo.xacro` - Gazebo 特定配置（物理属性、ros2_control）
- `config/controller.yaml` - ros2_control 控制器配置
- `launch/gazebo_harmonic.launch.py` - 完整版启动文件
- `launch/gazebo_simple.launch.py` - 简化版启动文件
- `package.xml` - 添加了 Gazebo 相关依赖
- `CMakeLists.txt` - 添加了依赖查找

### 原有文件：
- `urdf/DOG.urdf` - 原始机器人描述文件（未修改）
- `launch/display.launch.py` - RViz2 可视化启动文件（保持不变）

## 故障排除

### 问题 1: 找不到 gz 命令
```bash
# 检查 Gazebo 安装
which gz
# 如果没有，重新安装
sudo apt-get install gz-harmonic
```

### 问题 2: 机器人掉落或不稳定
- 调整生成高度：修改 `gazebo_simple.launch.py` 中的 `-z` 参数
- 检查 URDF 中的惯性参数是否合理

### 问题 3: 控制器加载失败
```bash
# 手动加载控制器
ros2 control load_controller --set-state active joint_state_broadcaster
ros2 control load_controller --set-state active position_controller
```

### 问题 4: 网格文件加载失败
确保 `meshes/` 目录中的 STL 文件存在且路径正确。

## 下一步开发

1. **添加传感器**：IMU、相机、激光雷达等
2. **实现运动控制**：编写步态控制节点
3. **地形导航**：加载复杂地形世界文件
4. **物理参数优化**：调整摩擦系数、阻尼等参数

## 参考资源

- [Gazebo Harmonic 文档](https://gazebosim.org/docs/harmonic)
- [ros_gz 文档](https://github.com/gazebosim/ros_gz)
- [ros2_control 文档](https://control.ros.org/)
