#!/usr/bin/env python3
"""square_driver – AUFGABE (Versuch 1).

Ziel: Den TurtleBot ein Quadrat fahren lassen, indem ihr Twist-Nachrichten
auf das Geschwindigkeits-Topic des Roboters publiziert.

Hintergrund:
    Bewegung wird über geometry_msgs/Twist gesteuert:
        linear.x  = Vorwärtsgeschwindigkeit in m/s
        angular.z = Drehgeschwindigkeit in rad/s
    Das Fahrbefehl-Topic ist bei UNSEREM TurtleBot 4 '/cmd_vel_unstamped'
    (Typ geometry_msgs/Twist). Das ähnlich benannte '/cmd_vel' erwartet
    TwistStamped und wird hier NICHT verwendet.
    (prüft es mit:  ros2 topic list | grep cmd_vel).

Starten (NUR mit freier Fläche und Aufsicht!):
    ros2 run praktikum_py square_driver

SICHERHEIT: Erst in der Simulation oder mit aufgebocktem Roboter testen.
"""
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SquareDriver(Node):
    def __init__(self):
        super().__init__('square_driver')

        # Parameter, damit ihr ohne Code-Änderung experimentieren könnt:
        self.declare_parameter('side_length', 0.5)      # m
        self.declare_parameter('linear_speed', 0.15)    # m/s
        self.declare_parameter('angular_speed', 0.5)    # rad/s

        # TODO 1: Publisher auf das Topic '/cmd_vel_unstamped' (Typ: Twist, Queue-Size 10) anlegen.
        #         Tipp:  self.pub = self.create_publisher(Twist, '/cmd_vel_unstamped', 10)
        self.pub = None  # <-- ersetzen

        # TODO 2: Timer mit z.B. 10 Hz (period=0.1) anlegen, der self.control_loop aufruft.
        self.timer = None  # <-- ersetzen

        self.get_logger().info('square_driver bereit. (TODOs noch offen!)')

    def control_loop(self):
        """Wird periodisch vom Timer aufgerufen. Hier die State-Machine bauen."""
        # TODO 3: Zustandsautomat: abwechselnd "geradeaus" und "drehen".
        #   - Berechnet aus side_length/linear_speed, wie lange geradeaus gefahren wird.
        #   - Berechnet aus 90° (pi/2) und angular_speed, wie lange gedreht wird.
        #   - Baut eine Twist-Nachricht und publiziert sie mit self.pub.publish(msg).
        #   - Stoppt nach 4 Seiten (alle Felder auf 0 setzen und publishen).
        raise NotImplementedError('TODO 3: control_loop implementieren')

    def stop(self):
        """Hilfsfunktion: Roboter anhalten (Nullgeschwindigkeit)."""
        msg = Twist()
        if self.pub is not None:
            self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SquareDriver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
