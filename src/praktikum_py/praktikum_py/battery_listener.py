#!/usr/bin/env python3
"""battery_listener – AUFGABE (Versuch 1).

Ziel: Den Ladezustand des TurtleBot abonnieren und ausgeben.
Lernziel: einen Subscriber schreiben und mit echten Sensordaten arbeiten.

Der TurtleBot 4 publiziert den Akkustand auf '/battery_state'
(Typ: sensor_msgs/BatteryState). Prüfen mit:
    ros2 topic info /battery_state
    ros2 interface show sensor_msgs/msg/BatteryState

Starten:
    ros2 run praktikum_py battery_listener
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState


class BatteryListener(Node):
    def __init__(self):
        super().__init__('battery_listener')

        # TODO 1: Subscriber auf '/battery_state' (Typ BatteryState) anlegen,
        #         Callback = self.on_battery, Queue-Size 10.
        #         self.sub = self.create_subscription(BatteryState, '/battery_state',
        #                                             self.on_battery, 10)
        self.sub = None  # <-- ersetzen

        self.get_logger().info('battery_listener bereit. (TODOs noch offen!)')

    def on_battery(self, msg: BatteryState):
        # TODO 2: Ladezustand in Prozent ausgeben (msg.percentage liegt zwischen 0.0 und 1.0).
        #         Zusatz: warnen, wenn unter 15 %.
        raise NotImplementedError('TODO 2: on_battery implementieren')


def main(args=None):
    rclpy.init(args=args)
    node = BatteryListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
