#!/usr/bin/env python3
"""hello_node – Minimaler ROS-2-Node als Referenzbeispiel.

Dieser Node ist KOMPLETT und dient als Vorlage. Lest ihn Zeile für Zeile,
bevor ihr die Aufgaben-Stubs (square_driver, battery_listener) bearbeitet.

Starten:
    ros2 run praktikum_py hello_node
"""
import rclpy
from rclpy.node import Node


class HelloNode(Node):
    def __init__(self):
        # Jeder Node braucht einen eindeutigen Namen im ROS-Graphen:
        super().__init__('hello_node')

        # Ein Parameter mit Default-Wert (von außen überschreibbar):
        self.declare_parameter('name', 'Welt')

        # Ein Timer ruft self.tick() periodisch auf (hier alle 1.0 s):
        self.timer = self.create_timer(1.0, self.tick)
        self.counter = 0
        self.get_logger().info('hello_node gestartet.')

    def tick(self):
        name = self.get_parameter('name').get_parameter_value().string_value
        self.counter += 1
        self.get_logger().info(f'Hallo {name}! (Tick {self.counter})')


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    try:
        rclpy.spin(node)          # Node am Leben halten, Callbacks abarbeiten
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
