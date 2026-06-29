#!/usr/bin/env python3
"""goto_goal – AUFGABE (Versuch 3, Navigation).

Ziel: Mit der TurtleBot4Navigator-API ein Navigationsziel anfahren.
Voraussetzung: Nav2 + Localization laufen bereits (siehe docs/03_navigation.md)
und der Roboter hat eine gültige Pose auf der Karte.

Doku: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/turtlebot4_navigator.html

Starten:
    ros2 run praktikum_py goto_goal
"""
import rclpy
from rclpy.node import Node

# Die Navigator-Klasse kommt aus dem TurtleBot-4-Paket:
#   from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Navigator
# Sie ist auf dem Laborrechner installiert. Falls der Import fehlschlägt,
# zuerst die ROS-Umgebung sourcen (siehe docs/00_setup.md).


def main(args=None):
    rclpy.init(args=args)

    # TODO 1: Navigator-Objekt erzeugen:
    #   from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Navigator
    #   navigator = TurtleBot4Navigator()

    # TODO 2: Startpose setzen (nur falls noch nicht lokalisiert) und auf Nav2 warten:
    #   navigator.waitUntilNav2Active()

    # TODO 3: Zielpose definieren und anfahren. Beispiel:
    #   from geometry_msgs.msg import PoseStamped
    #   goal = navigator.getPoseStamped([1.0, 0.5], TurtleBot4Directions.NORTH)
    #   navigator.startToPose(goal)

    # TODO 4: Ergebnis auswerten (navigator.getResult()) und ausgeben.

    raise NotImplementedError('TODOs in goto_goal.py umsetzen (siehe docs/03_navigation.md)')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
