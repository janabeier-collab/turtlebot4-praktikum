"""bringup.launch.py – Sammel-Launch für das Praktikum.

Startet mehrere Nodes aus praktikum_py gemeinsam und lädt ihre Parameter aus
config/params.yaml. Beispiel dafür, wie man in echten Projekten ein System
mit einem einzigen Befehl hochfährt.

Starten:
    ros2 launch praktikum_bringup bringup.launch.py
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(
        get_package_share_directory('praktikum_bringup'),
        'config', 'params.yaml',
    )

    hello = Node(
        package='praktikum_py',
        executable='hello_node',
        name='hello_node',
        output='screen',
        parameters=[params],
    )

    battery = Node(
        package='praktikum_py',
        executable='battery_listener',
        name='battery_listener',
        output='screen',
    )

    return LaunchDescription([hello, battery])
