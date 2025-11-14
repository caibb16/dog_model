# 🐕 四足机器人 Gazebo Harmonic 仿真快速入门

## ✅ 已完成的配置

所有文件已成功配置并编译！环境检查全部通过。

## 🚀 立即开始仿真

### 1️⃣ 简单启动（推荐首次使用）

```bash
cd /home/cai/dog_model-master
source install/setup.bash
ros2 launch DOG gazebo_simple.launch.py
```

**这将启动：**
- ✅ Gazebo Harmonic 仿真环境
- ✅ 四足机器人模型（悬浮在 0.5m 高度）
- ✅ Joint State Publisher GUI（关节控制滑块）
- ✅ Robot State Publisher（TF 变换）
- ✅ 时钟同步

**操作提示：**
- 在 Joint State Publisher GUI 窗口中拖动滑块来控制关节
- 在 Gazebo 窗口中点击播放按钮 ▶️ 开始物理仿真

---

### 2️⃣ 完整启动（带 RViz2 可视化）

```bash
source install/setup.bash
ros2 launch DOG gazebo_harmonic.launch.py rviz:=true
```

---

### 3️⃣ 仅在 RViz2 中可视化（无物理仿真）

```bash
source install/setup.bash
ros2 launch DOG display.launch.py
```

---

## 📁 新增的关键文件

### 配置文件：
- ✅ `urdf/DOG.xacro` - 主机器人描述（整合原始 URDF 和 Gazebo）
- ✅ `urdf/DOG.gazebo.xacro` - Gazebo 物理属性和控制器
- ✅ `config/controller.yaml` - ros2_control 控制器配置

### 启动文件：
- ✅ `launch/gazebo_simple.launch.py` - 简化版（推荐）
- ✅ `launch/gazebo_harmonic.launch.py` - 完整版（带 ros2_control）

### 依赖更新：
- ✅ `package.xml` - 添加了 Gazebo 和 ROS 2 控制相关依赖
- ✅ `CMakeLists.txt` - 更新了依赖查找

### 文档：
- ✅ `GAZEBO_HARMONIC_GUIDE.md` - 详细使用指南
- ✅ `check_gazebo_env.sh` - 环境检查脚本

---

## 🎮 控制机器人

### 方法 1: 使用 GUI 滑块（最简单）
启动 `gazebo_simple.launch.py` 后自动打开 Joint State Publisher GUI，
直接拖动滑块控制 12 个关节。

### 方法 2: 命令行发布关节位置

```bash
# 查看关节状态
ros2 topic echo /joint_states

# 发布关节命令（示例：所有膝关节弯曲）
ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray \
  "data: [0.0, 0.0, -1.5, 0.0, 0.0, -1.5, 0.0, 0.0, -1.5, 0.0, 0.0, -1.5]"
```

**关节顺序（12个）：**
```
FL_ABAD, FL_HIP, FL_KNEE,   # 前左腿
FR_ABAD, FR_HIP, FR_KNEE,   # 前右腿
RR_ABAD, RR_HIP, RR_KNEE,   # 后右腿
RL_ABAD, RL_HIP, RL_KNEE    # 后左腿
```

---

## 🔍 验证和调试

### 检查 Gazebo 是否运行
```bash
gz topic -l
gz model -l
```

### 检查 ROS 话题
```bash
ros2 topic list
ros2 topic hz /joint_states
```

### 查看 TF 变换树
```bash
ros2 run tf2_tools view_frames
evince frames.pdf
```

### 重新运行环境检查
```bash
./check_gazebo_env.sh
```

---

## 🎯 下一步开发建议

1. **步态控制** - 编写节点发布协调的关节轨迹
2. **传感器添加** - 在 URDF 中添加 IMU、相机
3. **地形测试** - 加载不同的 Gazebo 世界文件
4. **物理参数调优** - 调整摩擦系数、质量分布
5. **强化学习** - 使用 Gazebo 作为训练环境

---

## 📚 参考资源

- [Gazebo Harmonic 官方文档](https://gazebosim.org/docs/harmonic)
- [ros_gz 仓库](https://github.com/gazebosim/ros_gz)
- [ROS 2 Control](https://control.ros.org/)
- 详细指南：查看 `GAZEBO_HARMONIC_GUIDE.md`

---

## ⚠️ 常见问题

### Q: 机器人在仿真中掉落
A: 调整生成高度或添加初始关节位置配置

### Q: 关节不响应命令
A: 确保 ros2_control 控制器已正确加载

### Q: Gazebo 窗口无法打开
A: 检查 `gz sim --version` 是否正常，可能需要重启终端

### Q: 网格文件加载错误
A: ✅ 已解决！启动文件会自动转换路径格式

📖 **更多问题？** 查看 [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) 获取详细的故障排除指南。

---

**🎉 配置完成！现在就可以开始仿真了！**

```bash
ros2 launch DOG gazebo_simple.launch.py
```
