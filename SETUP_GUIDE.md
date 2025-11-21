# ROS 2 Humble 四足机器人项目配置指南

## 系统依赖安装

如果您是首次设置，请安装以下依赖：

```bash
# 基础 ROS 2 工具
sudo apt update
sudo apt install -y \
  ros-humble-xacro \
  ros-humble-joint-state-publisher \
  ros-humble-joint-state-publisher-gui \
  ros-humble-robot-state-publisher \
  ros-humble-rviz2 \
  ros-humble-ros-gz-sim \
  ros-humble-ros-gz-bridge \
  gazebo-harmonic
```

## 项目编译

```bash
cd /home/cai/VSproject/dog_model
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## 运行机器人

### 1. TF 树可视化（推荐）
```bash
# 启动机器人状态发布和关节发布
ros2 launch DOG display.launch.py
```

此模式下：
- ✅ 机器人 TF 树正常发布
- ✅ 关节状态发布正常
- ⚠️ RViz2 默认禁用（避免库冲突）

### 2. RViz2 可视化（高级）
```bash
# 如果环境支持图形界面，启用 RViz2
ros2 launch DOG display.launch.py rviz:=true
```

**注意**：如果出现 `__libc_pthread_init` 错误，这是系统库冲突（snap），不影响功能。

### 3. Gazebo 物理仿真
```bash
# 简单仿真
ros2 launch DOG gazebo_simple.launch.py

# 完整仿真（带 GUI 和 RViz2）
ros2 launch DOG gazebo_harmonic.launch.py gui:=true rviz:=true
```

## 项目结构

```
src/DOG/
├── urdf/                  # 机器人模型
│   ├── DOG.urdf          # 完整 URDF 模型
│   ├── DOG.xacro         # Xacro 配置
│   ├── DOG.gazebo.xacro  # Gazebo 扩展
│   └── ...
├── launch/               # 启动文件
│   ├── display.launch.py       # TF 树可视化
│   ├── gazebo_simple.launch.py # Gazebo 简单仿真
│   └── gazebo_harmonic.launch.py # Gazebo 完整仿真
├── config/               # 配置文件
│   ├── controller.yaml   # 控制器配置
│   └── rviz/             # RViz2 配置
├── meshes/               # 3D 模型文件
└── worlds/               # Gazebo 世界文件
```

## 关键 ROS 2 API 改进

### display.launch.py 的重要更新

新增 `rviz` 参数来控制 RViz2 的启动：
- `rviz:=false` （默认）- 禁用 RViz2，避免库冲突
- `rviz:=true` - 启用 RViz2 可视化（仅在支持图形界面时使用）

```python
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

rviz_node = launch_ros.actions.Node(
    package='rviz2',
    executable='rviz2',
    arguments=['-d', default_rviz_config_path],
    condition=IfCondition(LaunchConfiguration('rviz'))
)
```

## 常见问题

### Q: 为什么 RViz2 默认禁用？
A: 系统中存在 snap 库冲突，导致 `libpthread.so.0` 符号查找失败。禁用 RViz2 可以避免此问题，同时保证核心功能（TF 树、关节状态发布）正常工作。

### Q: 如何验证机器人模型是否正确加载？
A: 运行以下命令：
```bash
ros2 topic list | grep -E "tf|joint"
ros2 topic echo /tf
```

### Q: Gazebo 无法启动？
A: 确保安装了 Gazebo Harmonic：
```bash
sudo apt install -y gazebo-harmonic
```

## 下一步

1. **开发控制器**：修改 `src/DOG/config/controller.yaml` 实现机器人控制
2. **自定义仿真环境**：编辑 `src/DOG/worlds/dog_world.sdf` 添加障碍物
3. **视觉反馈**：在 RViz2 中添加相机插件以实现点云可视化

## 联系与支持

项目地址：`/home/cai/VSproject/dog_model`
当前分支：`cai`
