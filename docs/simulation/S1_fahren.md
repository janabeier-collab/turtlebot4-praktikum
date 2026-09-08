# Versuch S1 – Fahren und ROS-2-Grundlagen in der Simulation

> **Lernziele:** Ihr steuert den simulierten TurtleBot 4 über ROS-2-Topics und
> Actions, lest seine Sensordaten und lasst euren eigenen Node ein Quadrat fahren
> — denselben Node, der später auf der echten Hardware läuft.
>
> **Voraussetzung:** [S0](S0_setup.md) abgeschlossen.

In jedem Terminal zuerst: `source ~/turtlebot4-praktikum/tools/sim_env.sh`

**Terminal 1 – Simulation:**

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=warehouse
```

---

## S1.1 Den Graphen erkunden

```bash
ros2 node list
ros2 topic list
ros2 topic info /cmd_vel_unstamped
ros2 topic echo /battery_state --once
ros2 topic hz /scan
ros2 action list
```

**Frage 1 (Protokoll):** Vergleicht die Ausgabe von `ros2 topic list` mit der
Topic-Tabelle im [Cheatsheet](../cheatsheet.md). Welche Topics gibt es in der
Simulation, die es am echten Roboter nicht gibt — und umgekehrt?

---

## S1.2 Vom Dock runter

Auch der simulierte Roboter startet auf seiner Ladestation:

```bash
ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
```

Beobachtet dabei Gazebo. Zurück auf die Station:

```bash
ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"
```

**Frage 2:** Was steht in `/dock_status` vor und nach dem Undocken?

---

## S1.3 Fahren

Einzelner Fahrbefehl:

```bash
ros2 topic pub --once /cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.0}}"
```

Dauerhaft per Tastatur (Fenster muss im Fokus sein):

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
```

Geregelt über die Create-3-Actions:

```bash
ros2 action send_goal /drive_distance irobot_create_msgs/action/DriveDistance "{distance: 1.0, max_translation_speed: 0.3}"
```

```bash
ros2 action send_goal /rotate_angle irobot_create_msgs/action/RotateAngle "{angle: 1.5708, max_rotation_speed: 0.5}"
```

> **Warum funktioniert hier dasselbe Topic wie am echten Roboter?** Der simulierte
> Create 3 abonniert beides: `/cmd_vel` als `TwistStamped` und
> `/cmd_vel_unstamped` als `Twist`. Genau wie die echte Basis. Euer Code muss
> deshalb nicht angepasst werden.

---

## S1.4 Aufgabe A – Quadrat fahren

Ihr benutzt **denselben** Node wie im Hardwarepraktikum:
`src/praktikum_py/praktikum_py/square_driver.py` (TODO 1–3, siehe
[Versuch 1](../01_ros2_grundlagen.md)).

```bash
cd ~/turtlebot4-praktikum && colcon build --symlink-install && source install/setup.bash
```

```bash
ros2 run praktikum_py square_driver --ros-args -p use_sim_time:=true -p side_length:=1.0 -p linear_speed:=0.2
```

> Der Roboter muss vorher undockt sein, sonst fährt er gegen die Ladestation.

**Messen statt schätzen** — in einem zweiten Terminal die Endpose ablesen:

```bash
ros2 topic echo /odom --once | grep -A4 position
```

**Aufgabe:** Fahrt das Quadrat dreimal mit denselben Parametern und notiert jedes
Mal die Endposition.

**Frage 3:** Wie stark streuen die drei Läufe? Begründet das Ergebnis. Was
erwartet ihr am echten Roboter — mehr oder weniger Streuung, und warum?

**Frage 4:** Erhöht `linear_speed` auf 0,5 m/s. Wird das Quadrat besser oder
schlechter? Was ist die Ursache?

---

## S1.5 Aufgabe B – Akku überwachen

```bash
ros2 run praktikum_py battery_listener --ros-args -p use_sim_time:=true
```

Auch der simulierte Create 3 veröffentlicht einen Ladezustand.

**Frage 5:** Mit welcher Rate kommen die Nachrichten (`ros2 topic hz /battery_state`),
und wie verhält sich der Wert über mehrere Minuten? Vergleicht das mit eurer
Erwartung an einen echten Akku.

---

## S1.6 Zusatz – die Grenzen der Simulation sehen

Legt in Gazebo mit dem Würfel-Werkzeug ein Hindernis direkt vor den Roboter und
fahrt mit `square_driver` dagegen.

**Frage 6:** Was passiert? Welches Topic zeigt den Zusammenstoß
(`ros2 topic echo /hazard_detection`)? Und was hättet ihr am echten Roboter zusätzlich
bemerkt, das die Simulation nicht zeigt?

Weiter mit → [Versuch S2: SLAM](S2_slam.md)
