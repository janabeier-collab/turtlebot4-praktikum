#!/usr/bin/env python3
"""goto_goal – AUFGABE (Versuch 3, Navigation).

Ziel: Mit der TurtleBot4Navigator-API ein einzelnes Navigationsziel anfahren.

Voraussetzung: Localization und Nav2 laufen bereits (siehe docs/03_navigation.md):
    ros2 launch turtlebot4_navigation localization.launch.py map:=<...>/labor_map.yaml
    ros2 launch turtlebot4_navigation nav2.launch.py

Doku: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/turtlebot4_navigator.html

Starten:
    ros2 run praktikum_py goto_goal

SICHERHEIT: freie Fläche, niemand im Fahrweg, Hand am "Not-Aus" (Roboter anheben).
"""
import rclpy

from turtlebot4_navigation.turtlebot4_navigator import (
    TurtleBot4Directions,
    TurtleBot4Navigator,
)


def main(args=None):
    rclpy.init(args=args)

    # TODO 1: Navigator-Objekt erzeugen.
    #   navigator = TurtleBot4Navigator()
    #   (mit Namespace:  TurtleBot4Navigator(namespace='/tb01') )
    navigator = None  # <-- ersetzen

    # TODO 2: Startpose setzen, falls ihr sie nicht schon in RViz per
    #         "2D Pose Estimate" gesetzt habt. Steht der Roboter auf der
    #         Ladestation, ist deren Position der übliche Kartenursprung:
    #   if not navigator.getDockedStatus():
    #       navigator.info('Roboter steht nicht auf der Dock!')
    #   navigator.setInitialPose(
    #       navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH))

    # TODO 3: Warten, bis Nav2 vollstaendig hochgefahren ist:
    #   navigator.waitUntilNav2Active()

    # TODO 4: Vom Dock runterfahren (sonst dreht der Roboter in der Ladestation):
    #   navigator.undock()

    # TODO 5: Zielpose definieren, anfahren und danach wieder andocken:
    #   goal = navigator.getPoseStamped([1.0, 0.5], TurtleBot4Directions.NORTH)
    #   navigator.startToPose(goal)      # blockiert bis zum Ergebnis
    #   navigator.info(f'Ergebnis: {navigator.getResult()}')
    #   navigator.dock()

    raise NotImplementedError('TODOs in goto_goal.py umsetzen (siehe docs/03_navigation.md)')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
