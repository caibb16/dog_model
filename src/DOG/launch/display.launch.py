import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # 获取默认路径
    # 找到的是install/DOG/share/DOG
    urdf_tutorial_path = get_package_share_directory('DOG')

    # 锁定在CMakeLists.txt中install(DIRECTORY ...)指定的路径  share/DOG/urdf/DOG.urdf
    default_model_path = urdf_tutorial_path + '/urdf/DOG.urdf'
    default_rviz_config_path = urdf_tutorial_path + '/config/rviz/display_model.rviz'


    # 为 Launch 声明参数 // 方便更改URDF文件路径
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(default_model_path),
        description='URDF 的绝对路径')
    
    # 是否启动 RViz2 的参数（默认启动，可通过 rviz:=false 禁用）
    action_declare_arg_rviz = launch.actions.DeclareLaunchArgument(
        name='rviz', default_value='true',
        description='是否启动 RViz2（设置为 false 禁用）')
    

    # 获取文件内容生成新的参数，将xacro模型文件转换为robot_description参数，提供给robot_state_publisher节点使用
    # xacro可以简化URDF文件
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            ['xacro ', LaunchConfiguration('model')]),
        value_type=str)
    

    # 状态发布节点 启动robot_state_publisher
    # 包名和可执行文件名 参数
    # parameters 是传的字典格式
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher', 
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # 关节状态发布节点 启动joint_state_publisher
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )


    # RViz 节点    启动rviz2  等价于 ros2 run rviz2 rviz2 -d <path_to_config>
    # 使用 prefix 设置环境变量以修复 libpthread 库冲突
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path],
        condition=IfCondition(LaunchConfiguration('rviz')),
        prefix='env LD_PRELOAD=/lib/x86_64-linux-gnu/libpthread.so.0 QT_QPA_PLATFORM=xcb'
    )

    # 返回 LaunchDescription 对象 多节点启动
    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_declare_arg_rviz,
        joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node
    ])