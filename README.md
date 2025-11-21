# 四足机器人仿真项目

## 项目状态

- ✅ **ROS 2 Humble 完全兼容** - 已修正依赖和配置
- ✅ **RViz2 可视化** - 已完成（库冲突已修复）
- ✅ **Gazebo Harmonic 仿真** - 已完成（2025年11月14日）

## 快速开始

### 编译项目
```bash
cd /home/cai/VSproject/dog_model
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### RViz2 可视化（无物理仿真）

**基本运行（仅显示机器人 TF 树）：**
```bash
source install/setup.bash
ros2 launch DOG display.launch.py
```

**启用 RViz2 可视化（推荐）：**
```bash
source install/setup.bash
ros2 launch DOG display.launch.py rviz:=true
```

在 RViz2 中：
- 机器人模型以 3D 形式显示
- 可视化关节树结构
- 实时显示 TF 变换
- 支持交互式调整视角

### Gazebo Harmonic 物理仿真
```bash
source install/setup.bash
ros2 launch DOG gazebo_simple.launch.py
```

或带有更多选项的版本：
```bash
ros2 launch DOG gazebo_harmonic.launch.py gui:=true rviz:=true
```


## 机器人规格

- **类型**: 四足机器人
- **关节数**: 12 个可活动关节（每条腿 3 个）
- **腿部**: FL (前左), FR (前右), RL (后左), RR (后右)
- **每条腿关节**: ABAD (外展/内收), HIP (髋关节), KNEE (膝关节)

## 环境要求

- ROS 2 Humble
- Gazebo Harmonic (8.x) - 仅用于仿真
- Python 3
- 相关 ROS 包（自动通过 colcon 解决）

### 已安装的关键依赖
- `ros-humble-xacro` - URDF 转换工具
- `ros-humble-joint-state-publisher` - 关节状态发布
- `ros-humble-robot-state-publisher` - 机器人状态发布
- `ros-humble-rviz2` - 3D 可视化工具
- `ros-humble-ros-gz-sim` - Gazebo 集成
- `ros-humble-ros-gz-bridge` - ROS/Gazebo 通信桥接

## 编译

```bash
colcon build --symlink-install
source install/setup.bash
```

## 环境检查

```bash
./check_gazebo_env.sh
```

## 故障排除

### RViz2 库冲突
如果遇到错误：
```
symbol lookup error: /snap/core20/current/lib/x86_64-linux-gnu/libpthread.so.0: undefined symbol: __libc_pthread_init
```

**解决方案**：
1. 禁用 RViz2（默认状态）：`ros2 launch DOG display.launch.py`
2. 或设置环境变量：`export DISPLAY=:0` 后尝试启动

### Gazebo 启动失败
确保已安装 Gazebo Harmonic：
```bash
sudo apt install -y gazebo-harmonic
```

### 机器人模型不显示
1. 验证 URDF 文件存在：`ls install/DOG/share/DOG/urdf/`
2. 检查关节发布：`ros2 topic list | grep joint`
