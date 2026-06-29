"""demo.launch.py – Beispiel-Launch-File (Versuch 1).

Startet hello_node mit einem überschriebenen Parameter. Launch-Files bündeln
das Starten mehrerer Nodes inkl. Parametern, Namespaces und Remappings.

Starten:
    ros2 launch praktikum_py demo.launch.py
    ros2 launch praktikum_py demo.launch.py name:=Lübeck
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    name_arg = DeclareLaunchArgument('name', default_value='Praktikum')

    hello = Node(
        package='praktikum_py',
        executable='hello_node',
        name='hello_node',
        output='screen',
        parameters=[{'name': LaunchConfiguration('name')}],
    )

    return LaunchDescription([name_arg, hello])
