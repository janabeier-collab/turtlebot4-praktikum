# Versuch S4 – Mehrere Roboter gleichzeitig

> **Lernziele:** Ihr startet mehrere TurtleBots in einer Welt, versteht
> **Namespaces** als Trennung im ROS-2-Graphen und lasst zwei Roboter gleichzeitig
> navigieren.
>
> **Voraussetzung:** [S3](S3_navigation.md) abgeschlossen.

In jedem Terminal zuerst: `source ~/turtlebot4-praktikum/tools/sim_env.sh`

> Dieser Versuch ist das simulierte Gegenstück zum Handbuchkapitel *Multiple
> robots*. Am realen Aufbau wäre er teuer und unfallträchtig — hier kostet der
> zweite Roboter eine Zeile.

---

## S4.1 Warum Namespaces?

Ein zweiter Roboter im selben Graphen bringt alle Topics doppelt mit. Zwei Knoten
namens `/robot_state_publisher`, zwei Mal `/scan`, zwei Mal `/cmd_vel_unstamped` —
das kann nicht funktionieren. Ein **Namespace** stellt jedem Namen ein Präfix voran:

```
ohne Namespace          mit namespace:=/robot1
/scan                   /robot1/scan
/cmd_vel_unstamped      /robot1/cmd_vel_unstamped
/odom                   /robot1/odom
```

Jeder Roboter bekommt so seinen eigenen Ast im Graphen. Genau dieselbe Technik
benutzt das Labor, wenn mehrere echte TurtleBots gleichzeitig laufen sollen.

---

## S4.2 Zwei Roboter starten

Anders als in S0–S3 startet ihr Welt und Roboter **getrennt**.

**Terminal 1 – nur die Welt:**

```bash
ros2 launch turtlebot4_gz_bringup sim.launch.py world:=warehouse
```

**Terminal 2 – erster Roboter:**

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_spawn.launch.py namespace:=/robot1 x:=0.0 y:=0.0
```

**Terminal 3 – zweiter Roboter, versetzt:**

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_spawn.launch.py namespace:=/robot2 x:=0.0 y:=2.0
```

> Die Startposen **müssen** sich unterscheiden, sonst spawnen beide Roboter
> ineinander und Gazebo schleudert sie auseinander.

Kontrolle:

```bash
ros2 topic list | grep -E "robot1|robot2"
```

---

## S4.3 Beide getrennt fahren

**Roboter 1:**

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/robot1/cmd_vel_unstamped
```

**Roboter 2 – in einem weiteren Terminal:**

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/robot2/cmd_vel_unstamped
```

**Frage 1 (Protokoll):** Lasst versehentlich das Remapping weg und startet teleop
ohne Namespace. Was passiert, und warum? Prüft mit `ros2 topic info /cmd_vel_unstamped`.

**Frage 2:** Zeichnet den Graphen mit `rqt_graph` und fügt ihn ins Protokoll ein.
Markiert, welche Knoten zu welchem Roboter gehören.

---

## S4.4 Beide gleichzeitig navigieren

Nav2 muss pro Roboter einmal laufen — jeweils mit dessen Namespace:

```bash
ros2 launch turtlebot4_navigation localization.launch.py namespace:=/robot1 use_sim_time:=true map:=$HOME/turtlebot4-praktikum/maps/sim_maze_map.yaml
```

```bash
ros2 launch turtlebot4_navigation nav2.launch.py namespace:=/robot1 use_sim_time:=true
```

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py namespace:=/robot1 use_sim_time:=true
```

Dasselbe noch einmal mit `namespace:=/robot2`. Ihr braucht dann **zwei**
RViz-Fenster — je eines pro Roboter.

Aus eigenem Code sprecht ihr den Roboter über den Navigator-Konstruktor an:

```python
navigator = TurtleBot4Navigator(namespace='/robot1')
```

**Aufgabe:** Erweitert `patrol.py` um einen Parameter `namespace`, sodass ihr
denselben Node zweimal starten könnt:

```bash
ros2 run praktikum_py patrol --ros-args -p use_sim_time:=true -p namespace:=/robot1
```

**Frage 3:** Lasst beide Roboter Routen fahren, die sich kreuzen. Weichen sie
einander aus? Erklärt das Ergebnis: Was weiß Nav2 von Roboter 1 über Roboter 2?

**Frage 4:** Was müsste man ergänzen, damit sich die beiden zuverlässig
koordinieren? (Stichwort: gemeinsame Costmap oder eine übergeordnete Instanz.)

---

## S4.5 Übertrag auf das Labor

**Frage 5:** Im Labor hat jeder TurtleBot eine eigene **Domain-ID** statt eines
Namespaces. Was ist der Unterschied zwischen beiden Trennungen, und welche
Nachteile hätte es, die sechs Laborroboter stattdessen über Namespaces in einer
gemeinsamen Domain zu betreiben?

Zurück zur → [Übersicht](README.md) · Vergleich mit der Hardware →
[Unterschiede](unterschiede.md)
