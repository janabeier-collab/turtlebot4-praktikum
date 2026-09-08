# Versuch S2 – SLAM in der Simulation

> **Lernziele:** Ihr kartiert eine Gazebo-Welt mit der SLAM Toolbox, versteht den
> Einfluss von Fahrweise und Loop Closure auf die Kartenqualität und speichert
> eine Karte für Versuch S3.
>
> **Voraussetzung:** [S1](S1_fahren.md) abgeschlossen.

In jedem Terminal zuerst: `source ~/turtlebot4-praktikum/tools/sim_env.sh`

---

## S2.1 Warum das Labyrinth?

Für SLAM ist die Welt **maze** die dankbarste: enge Gänge, klare Wände, eine
geschlossene Runde. `warehouse` ist groß und offen — dort verliert die
Odometrie schneller den Faden, was für Versuch S2.5 interessant ist.

**Terminal 1 – Simulation mit SLAM und RViz:**

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=maze slam:=true rviz:=true
```

Damit laufen Gazebo, SLAM Toolbox und RViz in einem Rutsch, alle mit
`use_sim_time`. In RViz seht ihr die Karte entstehen; Fixed Frame ist `map`.

---

## S2.2 Kartieren

**Terminal 2 – Undocken und fahren:**

```bash
ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
```

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
```

Vorgehen wie am echten Roboter:

1. Langsam fahren, besonders bei Drehungen.
2. Systematisch an den Wänden entlang.
3. Mindestens einmal zum Ausgangspunkt zurück (**Loop Closure**).
4. In RViz auf doppelte Wände achten.

> **Vorteil der Simulation:** Ihr könnt die Simulation pausieren (Play/Pause in
> Gazebo), in Ruhe die Karte anschauen und weiterfahren. Und wenn die Karte
> misslingt, startet ihr einfach neu — der Roboter braucht keine Ladepause.

---

## S2.3 Karte speichern

```bash
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name: {data: '$HOME/turtlebot4-praktikum/maps/sim_maze_map'}"
```

Kontrolle:

```bash
ls -l ~/turtlebot4-praktikum/maps/sim_maze_map.*
```

Es müssen `sim_maze_map.pgm` und `sim_maze_map.yaml` entstehen. Beide braucht ihr
in Versuch S3.

---

## S2.4 Aufgaben & Protokoll

1. Kartiert `maze` vollständig und speichert `sim_maze_map`.
2. Screenshot der RViz-Karte ins Protokoll.
3. **Frage 1:** Öffnet `sim_maze_map.yaml`. Was bedeuten `resolution`, `origin`,
   `occupied_thresh` und `free_thresh`?
4. **Frage 2:** Vergleicht eure Karte mit der Gazebo-Ansicht. Wo weicht sie ab,
   und warum? (Tipp: der LiDAR sitzt in einer bestimmten Höhe.)

---

## S2.5 Das Experiment, das nur in der Simulation geht

Fahrt dieselbe Runde **zweimal**: einmal betont langsam, einmal mit schnellen
Drehungen. Speichert beide Karten unter verschiedenen Namen.

```bash
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name: {data: '$HOME/turtlebot4-praktikum/maps/sim_maze_schnell'}"
```

**Frage 3:** Legt beide `.pgm`-Dateien nebeneinander ins Protokoll. Wo genau
entstehen die Fehler bei der schnellen Fahrt?

**Frage 4:** Startet die Simulation neu und kartiert `warehouse` statt `maze`.
Wo ist SLAM dort unsicherer als im Labyrinth? Was sagt euch das über die
Anforderungen an einen Raum, der gut kartierbar sein soll?

> Genau dieser Vergleich ist am echten Roboter kaum machbar — ihr könnt die
> Fahrt nicht identisch wiederholen und den Raum nicht austauschen.

Weiter mit → [Versuch S3: Navigation](S3_navigation.md)
