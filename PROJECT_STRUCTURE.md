# 项目文件结构说明

## 📂 完整目录结构

```
dog_model-master/
├── README.md                      # 项目主文档（已更新）
├── QUICKSTART.md                  # 快速入门指南（新增）
├── GAZEBO_HARMONIC_GUIDE.md       # Gazebo 详细指南（新增）
├── check_gazebo_env.sh            # 环境检查脚本（新增）
├── ros笔记.wps                    # 原有笔记
│
├── src/DOG/                       # ROS 2 包源码
│   ├── package.xml                # 包依赖配置（已更新）
│   ├── CMakeLists.txt             # 编译配置（已更新）
│   ├── LICENSE                    
│   │
│   ├── config/                    # 配置文件目录
│   │   ├── joint_names_DOG.yaml  # 关节名称定义
│   │   └── controller.yaml       # ros2_control 控制器配置（新增）
│   │
│   ├── urdf/                      # 机器人描述文件
│   │   ├── DOG.urdf              # 原始 URDF（从 SolidWorks 导出）
│   │   ├── DOG.xacro             # 主 xacro 文件（新增）
│   │   ├── DOG.gazebo.xacro      # Gazebo 配置（新增）
│   │   └── DOG.gv                # 图形可视化
│   │
│   ├── meshes/                    # 3D 网格文件（STL）
│   │   ├── BASE_LINK.STL
│   │   ├── FL_ABAD_LINK.STL
│   │   ├── FL_HIP_LINK.STL
│   │   ├── FL_KNEE_LINK.STL
│   │   ├── FL_FOOT_LINK.STL
│   │   └── ... (其他腿部网格)
│   │
│   └── launch/                    # 启动文件目录
│       ├── display.launch         # ROS 1 格式（已弃用）
│       ├── display.launch.py      # RViz2 启动（ROS 2）
│       ├── gazebo.launch          # ROS 1 格式（已弃用）
│       ├── gazebo_simple.launch.py       # Gazebo 简化版（新增）★
│       └── gazebo_harmonic.launch.py     # Gazebo 完整版（新增）★
│
├── build/                         # 编译中间文件
├── install/                       # 安装文件
└── log/                          # 日志文件
```

---

## 🔑 关键文件说明

### 1️⃣ 机器人描述文件

#### `urdf/DOG.urdf`
- **来源**: SolidWorks URDF Exporter 自动生成
- **内容**: 完整的机器人几何、惯性、关节定义
- **状态**: 原始文件，未修改
- **用途**: RViz2 可视化、Gazebo 仿真基础

#### `urdf/DOG.xacro` ⭐ 新增
- **格式**: Xacro (XML Macros)
- **作用**: 整合原始 URDF 和 Gazebo 配置
- **内容**:
  ```xml
  <xacro:include filename="DOG.urdf"/>
  <xacro:include filename="DOG.gazebo.xacro"/>
  ```

#### `urdf/DOG.gazebo.xacro` ⭐ 新增
- **作用**: Gazebo 专用配置
- **内容**:
  - 物理属性（摩擦系数 μ₁, μ₂）
  - 碰撞参数（刚度 kp, 阻尼 kd）
  - ros2_control 接口定义
  - 12 个关节的控制接口

---

### 2️⃣ 启动文件

#### `launch/display.launch.py`
- **功能**: RViz2 可视化（无物理仿真）
- **启动内容**:
  - `robot_state_publisher` - 发布机器人描述和 TF
  - `joint_state_publisher` - 发布关节状态
  - `rviz2` - 3D 可视化

#### `launch/gazebo_simple.launch.py` ⭐ 新增（推荐）
- **功能**: Gazebo Harmonic 简化仿真
- **启动内容**:
  - `gz sim` - Gazebo 仿真器
  - `robot_state_publisher` - 机器人状态
  - `ros_gz_sim create` - 在仿真中生成机器人
  - `ros_gz_bridge` - ROS-Gazebo 通信桥
  - `joint_state_publisher_gui` - 关节控制 GUI
- **特点**: 简单易用，适合快速测试

#### `launch/gazebo_harmonic.launch.py` ⭐ 新增
- **功能**: Gazebo Harmonic 完整仿真（带 ros2_control）
- **额外功能**:
  - ros2_control 控制器加载
  - 支持自定义世界文件
  - 可选 RViz2 集成
- **特点**: 功能完整，适合开发

---

### 3️⃣ 配置文件

#### `config/controller.yaml` ⭐ 新增
- **作用**: ros2_control 控制器配置
- **内容**:
  ```yaml
  controller_manager:
    update_rate: 100  # Hz
    joint_state_broadcaster: ...
    position_controller: ...
  ```
- **控制器类型**:
  - `joint_state_broadcaster` - 发布关节状态到 `/joint_states`
  - `position_controller` - 位置控制（接收 12 个关节目标位置）

---

### 4️⃣ 包配置文件

#### `package.xml` ✏️ 已更新
**新增依赖**:
```xml
<depend>ros_gz_sim</depend>        <!-- Gazebo 仿真 -->
<depend>ros_gz_bridge</depend>     <!-- ROS-Gazebo 桥接 -->
<depend>gz_ros2_control</depend>   <!-- Gazebo 控制插件 -->
<depend>ros2_control</depend>      <!-- ROS 2 控制框架 -->
<depend>ros2_controllers</depend>  <!-- 标准控制器 -->
```

#### `CMakeLists.txt` ✏️ 已更新
**关键更新**:
- 添加了 `urdf`, `xacro`, `robot_state_publisher` 依赖
- 保持安装配置：`config`, `launch`, `meshes`, `urdf`

---

## 🔄 文件使用流程

### RViz2 可视化流程:
```
DOG.urdf 
  → display.launch.py 
  → robot_state_publisher 
  → rviz2
```

### Gazebo 仿真流程:
```
DOG.urdf + DOG.gazebo.xacro 
  → gazebo_simple.launch.py 
  → gz sim + ros_gz_sim 
  → 物理仿真
```

### 控制流程:
```
joint_state_publisher_gui (用户输入)
  → /joint_states 话题
  → robot_state_publisher
  → /tf, /tf_static
  → Gazebo + RViz2 可视化
```

---

## 📊 关节定义

### 12 个可活动关节:

| 腿部 | ABAD 关节 | HIP 关节 | KNEE 关节 |
|------|-----------|----------|-----------|
| 前左 (FL) | FL_ABAD_JOINT | FL_HIP_JOINT | FL_KNEE_JOINT |
| 前右 (FR) | FR_ABAD_JOINT | FR_HIP_JOINT | FR_KNEE_JOINT |
| 后右 (RR) | RR_ABAD_JOINT | RR_HIP_JOINT | RR_KNEE_JOINT |
| 后左 (RL) | RL_ABAD_JOINT | RL_HIP_JOINT | RL_KNEE_JOINT |

### 4 个固定关节:
- FL_FOOT_JOINT, FR_FOOT_JOINT, RR_FOOT_JOINT, RL_FOOT_JOINT

---

## 🛠️ 开发建议

### 如果要修改机器人模型:
1. 编辑 `DOG.urdf` (几何、惯性)
2. 编辑 `DOG.gazebo.xacro` (物理属性)
3. 重新编译: `colcon build --symlink-install`

### 如果要添加传感器:
1. 在 `DOG.gazebo.xacro` 中添加 Gazebo 传感器插件
2. 在启动文件中添加话题桥接

### 如果要更改控制器:
1. 编辑 `config/controller.yaml`
2. 在启动文件中加载新控制器

---

## 📦 编译产物

### `install/DOG/` 目录:
```
install/DOG/
├── lib/DOG/                  # 可执行文件（如有）
└── share/DOG/                # 资源文件
    ├── config/               # 配置文件
    ├── launch/               # 启动文件
    ├── meshes/               # 网格文件
    └── urdf/                 # URDF 文件
```

所有启动文件都从 `install/DOG/share/DOG/` 读取资源！

---

## 🎯 使用建议

**新手**: 使用 `gazebo_simple.launch.py` + GUI 滑块控制
**开发**: 使用 `gazebo_harmonic.launch.py` + 自定义控制节点
**调试**: 使用 `display.launch.py` 快速验证 URDF 正确性
