# 四足机器人仿真项目

## 项目状态

- ✅ **ROS 2 Humble 完全兼容** - 已修正依赖和配置
- ✅ **RViz2 可视化** - 已完成（库冲突已修复）
- ✅ **Gazebo Classic 11.10.2 仿真** - 已完成（2025年11月21日）

## 快速开始

### 编译项目
```bash
cd /home/cai/VSproject/dog_model
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### RViz2 可视化（无物理仿真）

**启动 RViz2 可视化（推荐）：**
```bash
source install/setup.bash
ros2 launch DOG display.launch.py
```

**如果需要禁用 RViz2（仅显示 TF 树）：**
```bash
source install/setup.bash
ros2 launch DOG display.launch.py rviz:=false
```

在 RViz2 中：
- 机器人模型以 3D 形式显示
- 可视化关节树结构
- 实时显示 TF 变换
- 支持交互式调整视角

### Gazebo Classic 11 物理仿真
```bash
source install/setup.bash
ros2 launch DOG gazebo_simple.launch.py
```

这将启动：
- **Gazebo 服务器（gzserver）** - 物理仿真引擎
- **Gazebo 客户端（gzclient）** - 3D 可视化界面
- **机器人状态发布器** - 发布 TF 变换
- **关节状态发布器** - 发布关节状态
- **机器人生成器** - 将机器人加载到 Gazebo


## 机器人规格

- **类型**: 四足机器人
- **关节数**: 12 个可活动关节（每条腿 3 个）
- **腿部**: FL (前左), FR (前右), RL (后左), RR (后右)
- **每条腿关节**: ABAD (外展/内收), HIP (髋关节), KNEE (膝关节)

## 环境要求

- **ROS 2 Humble** - 机器人操作系统
- **Gazebo Classic 11.10.2** - 物理仿真引擎（官方推荐用于ROS 2 Humble）
- **Python 3** - 启动脚本支持
- 相关 ROS 包（自动通过 colcon 解决）

### 已安装的关键依赖
- `gazebo` (11.10.2) - 经典 Gazebo 仿真器
- `ros-humble-gazebo-ros` - ROS 与 Gazebo 的接口
- `ros-humble-gazebo-ros-pkgs` - Gazebo ROS 包集合
- `ros-humble-gazebo-plugins` - 传感器和执行器插件
- `ros-humble-joint-state-publisher` - 关节状态发布
- `ros-humble-robot-state-publisher` - 机器人状态和 TF 发布
- `ros-humble-rviz2` - 3D 可视化工具

### 版本对应关系
| ROS 2 版本 | 推荐 Gazebo 版本 | 备注 |
|-----------|-----------------|------|
| Humble | Classic 11.x | 官方稳定版本 |
| Humble | Gazebo Fortress | 新版本，功能更强 |

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

### 问题 1: Gazebo 启动但没有显示机器人模型

**症状**：Gazebo 界面打开，但看不到机器人

**解决方案**：
1. 检查 ros2 话题（在新终端运行）：
   ```bash
   ros2 topic list
   ```
   应该看到 `/robot_description` 和 `/joint_states`

2. 检查生成日志（查看启动终端输出）：
   - 确保有 `spawn_entity.py` 的成功输出
   - 检查是否有 mesh 文件路径错误

3. 重新启动Gazebo和ROS:
   ```bash
   pkill -f gzserver
   pkill -f gzclient
   source install/setup.bash
   ros2 launch DOG gazebo_simple.launch.py
   ```

### 问题 2: SDF 版本错误

**错误信息**：
```
Error [Converter.cc:113] Unable to convert from SDF version 1.9 to 1.7
```

**原因**：World 文件使用了 Gazebo Sim（新版本）的 SDF 1.9 格式

**解决方案**：World 文件已更新为 SDF 1.6（Gazebo Classic 11 兼容格式）

### 问题 3: 物理引擎错误

**错误信息**：
```
[Err] [World.cc:345] EXCEPTION: Unable to create physics engine
```

**原因**：物理引擎类型不支持

**解决方案**：World 文件中已配置为 `type="ode"`（ODE 是 Gazebo Classic 11 的标准引擎）

### 问题 4: RViz2 库冲突

**错误信息**：
```
symbol lookup error: /snap/core20/current/lib/x86_64-linux-gnu/libpthread.so.0
```

**解决方案**：
```bash
# 使用 RViz2（如果库兼容）
ros2 launch DOG display.launch.py

# 如果 RViz2 有问题，禁用它
ros2 launch DOG display.launch.py rviz:=false
```

### 问题 5: 检查 mesh 文件

```bash
# 验证 mesh 文件是否存在
ls -la install/DOG/share/DOG/meshes/

# 验证 URDF 是否正确安装
ls -la install/DOG/share/DOG/urdf/
```

### 问题 6: 查看完整的 ROS 拓扑

```bash
# 查看所有节点
ros2 node list

# 查看所有话题
ros2 topic list

# 查看 TF 树
ros2 run tf2_tools view_frames
```
