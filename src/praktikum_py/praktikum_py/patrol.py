#!/usr/bin/env python3
"""patrol – PFLICHTAUFGABE (Versuch 3, Navigation).

Ziel: Eine Route aus mehreren Wegpunkten autonom abfahren und danach andocken.

Voraussetzung: Localization und Nav2 laufen (siehe docs/03_navigation.md),
die Startpose ist gesetzt.

Drei Varianten der TurtleBot4Navigator-API:
    startToPose(pose)          ein Ziel, blockiert bis fertig
    startThroughPoses(poses)   EIN durchgehender Plan, Zwischenposen werden gestreift
    startFollowWaypoints(pose) jeder Wegpunkt wird einzeln angefahren und erreicht

Starten:
    ros2 run praktikum_py patrol

SICHERHEIT: freie Fläche, niemand im Fahrweg, Hand am "Not-Aus" (Roboter anheben).
"""
import rclpy

from turtlebot4_navigation.turtlebot4_navigator import (
    TurtleBot4Directions,
    TurtleBot4Navigator,
)


def main(args=None):
    rclpy.init(args=args)

    navigator = TurtleBot4Navigator()

    # TODO 1: Wegpunkte eurer Route definieren (mind. 4).
    #         Koordinaten lest ihr in RViz ab: Mauszeiger ueber die Karte
    #         bewegen, unten links werden x/y angezeigt.
    #   waypoints = [
    #       navigator.getPoseStamped([1.0,  0.0], TurtleBot4Directions.NORTH),
    #       navigator.getPoseStamped([1.0,  1.5], TurtleBot4Directions.WEST),
    #       navigator.getPoseStamped([-0.5, 1.5], TurtleBot4Directions.SOUTH),
    #       navigator.getPoseStamped([0.0,  0.0], TurtleBot4Directions.EAST),
    #   ]
    waypoints = []  # <-- ersetzen

    # TODO 2: Startpose setzen (falls noch nicht in RViz geschehen) und
    #         auf Nav2 warten:
    #   navigator.setInitialPose(
    #       navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH))
    #   navigator.waitUntilNav2Active()

    # TODO 3: Undocken, falls der Roboter auf der Ladestation steht:
    #   if navigator.getDockedStatus():
    #       navigator.undock()

    # TODO 4: Route abfahren. Probiert BEIDE Varianten aus und vergleicht
    #         das Fahrverhalten (Frage 3 im Protokoll):
    #   navigator.startFollowWaypoints(waypoints)
    #   navigator.startThroughPoses(waypoints)

    # TODO 5: Ergebnis ausgeben und wieder andocken:
    #   navigator.info(f'Ergebnis: {navigator.getResult()}')
    #   navigator.dock()

    raise NotImplementedError('TODOs in patrol.py umsetzen (siehe docs/03_navigation.md)')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
