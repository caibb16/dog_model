# 故障排除指南

## 已解决的问题

### ✅ 问题 1: Gazebo 无法加载网格文件

**错误信息：**
```
[gz-2] [GUI] [Err] [MeshManager.cc:211] Unable to find file[model://DOG/meshes/FR_ABAD_LINK.STL]
[gz-2] [GUI] [Err] [SceneManager.cc:426] Failed to load geometry for visual: FR_ABAD_LINK_visual
[gz-2] [GUI] [Err] [SystemPaths.cc:425] Unable to find file with URI [model://DOG/meshes/FR_HIP_LINK.STL]
```

**原因：**
Gazebo Harmonic 无法直接解析 ROS 的 `package://` URI 路径。URDF 中使用的是：
```xml
<mesh filename="package://DOG/meshes/BASE_LINK.STL" />
```

**解决方案：**
在启动文件中将 `package://` 路径替换为 `file://` 绝对路径：

```python
# 读取 URDF 并替换路径
with open(urdf_file, 'r') as f:
    robot_description_content = f.read()

robot_description_content = robot_description_content.replace(
    'package://DOG', 'file://' + pkg_dog
)
```

**状态：** ✅ 已在 `gazebo_simple.launch.py` 和 `gazebo_harmonic.launch.py` 中修复

---

### ⚠️ 警告 1: KDL Parser 根链接惯性警告

**警告信息：**
```
[WARN] [kdl_parser]: The root link BASE_LINK has an inertia specified in the URDF, 
but KDL does not support a root link with an inertia. As a workaround, you can add 
an extra dummy link to your URDF.
```

**影响：**
- 不影响 Gazebo 仿真
- 不影响可视化
- 仅影响某些使用 KDL 运动学库的功能

**是否需要修复：**
- ❌ 不需要立即修复
- ✅ 如果需要使用 KDL 运动学，可以添加虚拟根链接

**可选解决方案（高级）：**
在 URDF 中添加虚拟根链接：
```xml
<link name="world"/>
<joint name="world_to_base" type="fixed">
  <parent link="world"/>
  <child link="BASE_LINK"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
</joint>
```

---

## 常见问题

### 问题：Gazebo 窗口无法打开

**可能原因：**
1. Gazebo Harmonic 未安装
2. 图形驱动问题
3. 其他 Gazebo 进程占用

**排查步骤：**
```bash
# 1. 检查 Gazebo 安装
gz sim --version

# 2. 测试单独启动 Gazebo
gz sim empty.sdf

# 3. 杀死所有 Gazebo 进程
killall -9 gz

# 4. 检查日志
cat ~/.ros/log/latest/launch.log
```

---

### 问题：机器人在仿真中快速掉落

**原因：**
重力作用，机器人悬浮在空中但关节没有支撑姿态

**解决方案：**
1. **增加生成高度** - 在 `gazebo_simple.launch.py` 中修改：
   ```python
   '-z', '1.0',  # 从 0.5 增加到 1.0
   ```

2. **设置初始关节位置** - 在启动前发布关节状态：
   ```bash
   ros2 topic pub /joint_states sensor_msgs/msg/JointState '{...}'
   ```

3. **暂停物理** - 启动 Gazebo 时暂停：
   ```python
   gz_args = ['-r', 'empty.sdf']  # 移除 -r 参数
   ```

---

### 问题：Joint State Publisher GUI 窗口关闭后仿真停止

**原因：**
GUI 进程终止导致整个启动文件退出

**解决方案：**
在终端保持运行状态，或在后台运行：
```bash
ros2 launch DOG gazebo_simple.launch.py &
```

---

### 问题：关节不响应 GUI 滑块

**可能原因：**
1. `joint_state_publisher_gui` 和 ros2_control 冲突
2. 话题名称不匹配

**排查：**
```bash
# 查看活动话题
ros2 topic list

# 查看关节状态是否发布
ros2 topic echo /joint_states

# 查看 TF 树
ros2 run tf2_tools view_frames
```

**解决方案：**
- 简化版（`gazebo_simple.launch.py`）使用 GUI 控制
- 完整版（`gazebo_harmonic.launch.py`）使用 ros2_control

不要同时运行两者！

---

### 问题：编译错误 - 找不到依赖包

**错误示例：**
```
CMake Error: Could not find a package configuration file provided by "ros_gz_sim"
```

**解决方案：**
```bash
# 安装缺失的包
sudo apt update
sudo apt install ros-${ROS_DISTRO}-ros-gz-sim \
                 ros-${ROS_DISTRO}-ros-gz-bridge \
                 ros-${ROS_DISTRO}-joint-state-publisher-gui

# 重新编译
colcon build --symlink-install
```

---

### 问题：网格文件显示为灰色/黑色

**原因：**
STL 文件没有颜色信息，使用默认材质

**解决方案：**
在 `DOG.gazebo.xacro` 中已设置：
```xml
<gazebo reference="BASE_LINK">
  <material>Gazebo/Grey</material>
</gazebo>
```

如需更改颜色，修改材质名称：
- `Gazebo/Grey`
- `Gazebo/Red`
- `Gazebo/Blue`
- `Gazebo/Green`
- `Gazebo/Black`
- `Gazebo/White`

---

## 性能优化

### 如果仿真卡顿：

1. **降低实时系数**
   ```python
   gz_args = ['-r', '--render-engine', 'ogre2', 'empty.sdf']
   ```

2. **减少可视化质量**
   - 在 Gazebo GUI 中：View → Quality → Low

3. **使用简化碰撞几何**
   - 将 STL 网格替换为简单形状（box, sphere）

4. **关闭不必要的传感器**
   - 注释掉 URDF 中的传感器插件

---

## 调试技巧

### 1. 查看机器人描述
```bash
# 查看发布的 URDF
ros2 topic echo /robot_description

# 保存到文件
ros2 topic echo /robot_description > robot_desc.txt
```

### 2. 检查 Gazebo 话题
```bash
# 列出 Gazebo 话题
gz topic -l

# 查看模型列表
gz model -l

# 查看世界信息
gz world -l
```

### 3. 实时监控关节状态
```bash
# 监控关节位置
ros2 topic echo /joint_states

# 监控频率
ros2 topic hz /joint_states
```

### 4. TF 树可视化
```bash
# 生成 TF 树 PDF
ros2 run tf2_tools view_frames

# 查看
evince frames.pdf
```

---

## 获取帮助

如果遇到未解决的问题：

1. **查看日志**
   ```bash
   cat ~/.ros/log/latest/launch.log
   ```

2. **运行环境检查**
   ```bash
   ./check_gazebo_env.sh
   ```

3. **查看文档**
   - `README.md` - 项目概述
   - `QUICKSTART.md` - 快速入门
   - `GAZEBO_HARMONIC_GUIDE.md` - 详细指南

4. **参考资源**
   - [Gazebo Harmonic 文档](https://gazebosim.org/docs/harmonic)
   - [ros_gz 问题追踪](https://github.com/gazebosim/ros_gz/issues)
   - [ROS 2 Control 文档](https://control.ros.org/)

---

**最后更新：** 2025年11月14日
