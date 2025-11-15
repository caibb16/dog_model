#!/bin/bash
# Gazebo Harmonic 环境检查脚本

echo "======================================"
echo "Gazebo Harmonic 环境检查"
echo "======================================"
echo

# 1. 检查 Gazebo Harmonic
echo "1. 检查 Gazebo Harmonic 安装..."
if command -v gz &> /dev/null; then
    echo "✓ Gazebo 已安装"
    gz sim --versions
else
    echo "✗ 未找到 Gazebo Harmonic"
    echo "  安装命令: sudo apt-get install gz-harmonic"
fi
echo

# 2. 检查 ROS 包
echo "2. 检查 ROS 2 Gazebo 集成包..."
packages=(
    "ros_gz_sim"
    "ros_gz_bridge"
    "joint_state_publisher_gui"
    "robot_state_publisher"
)

for pkg in "${packages[@]}"; do
    if ros2 pkg prefix "$pkg" &> /dev/null; then
        echo "✓ $pkg"
    else
        echo "✗ $pkg (未安装)"
    fi
done
echo

# 3. 检查 DOG 包
echo "3. 检查 DOG 包..."
if ros2 pkg prefix DOG &> /dev/null; then
    echo "✓ DOG 包已编译"
    DOG_PATH=$(ros2 pkg prefix DOG)
    echo "  路径: $DOG_PATH"
else
    echo "✗ DOG 包未找到"
    echo "  请运行: colcon build --symlink-install"
fi
echo

# 4. 检查启动文件
echo "4. 检查启动文件..."
if ros2 pkg prefix DOG &> /dev/null; then
    DOG_SHARE=$(ros2 pkg prefix DOG)/share/DOG
    if [ -f "$DOG_SHARE/launch/gazebo_simple.launch.py" ]; then
        echo "✓ gazebo_simple.launch.py"
    else
        echo "✗ gazebo_simple.launch.py"
    fi
    
    if [ -f "$DOG_SHARE/launch/gazebo_harmonic.launch.py" ]; then
        echo "✓ gazebo_harmonic.launch.py"
    else
        echo "✗ gazebo_harmonic.launch.py"
    fi
fi
echo

# 5. 检查 URDF 文件
echo "5. 检查 URDF 文件..."
if ros2 pkg prefix DOG &> /dev/null; then
    DOG_SHARE=$(ros2 pkg prefix DOG)/share/DOG
    if [ -f "$DOG_SHARE/urdf/DOG.urdf" ]; then
        echo "✓ DOG.urdf"
    fi
    if [ -f "$DOG_SHARE/urdf/DOG.xacro" ]; then
        echo "✓ DOG.xacro"
    fi
    if [ -f "$DOG_SHARE/urdf/DOG.gazebo.xacro" ]; then
        echo "✓ DOG.gazebo.xacro"
    fi
fi
echo

# 6. 总结和建议
echo "======================================"
echo "总结"
echo "======================================"
echo
echo "如果所有检查都通过(✓)，可以运行:"
echo "  ros2 launch DOG gazebo_simple.launch.py"
echo
echo "如果有未安装的包(✗)，请运行:"
echo "  sudo apt-get install ros-\${ROS_DISTRO}-ros-gz-sim \\"
echo "                       ros-\${ROS_DISTRO}-ros-gz-bridge \\"
echo "                       ros-\${ROS_DISTRO}-joint-state-publisher-gui \\"
echo "                       gz-harmonic"
echo
