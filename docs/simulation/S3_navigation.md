# Versuch S3 – Navigation mit Nav2 in der Simulation

> **Lernziele:** Ihr navigiert den simulierten TurtleBot 4 autonom auf eurer
> Karte, testet das Ausweichverhalten mit Hindernissen, die ihr zur Laufzeit in
> die Welt legt, und fahrt eine Route aus mehreren Wegpunkten.
>
> **Voraussetzung:** [S2](S2_slam.md) abgeschlossen, Karte `sim_maze_map` gespeichert.

In jedem Terminal zuerst: `source ~/turtlebot4-praktikum/tools/sim_env.sh`

---

## S3.1 Zwei Wege, Nav2 zu starten

**Weg A – alles in einem Befehl** (schnell, benutzt aber die mitgelieferte
Standardkarte der Welt, nicht eure):

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=maze nav2:=true localization:=true rviz:=true
```

**Weg B – mit eurer eigenen Karte aus S2** (das ist der Weg, den ihr für das
Protokoll nehmt). Vier Terminals:

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=maze
```

```bash
ros2 launch turtlebot4_navigation localization.launch.py use_sim_time:=true map:=$HOME/turtlebot4-praktikum/maps/sim_maze_map.yaml
```

```bash
ros2 launch turtlebot4_navigation nav2.launch.py use_sim_time:=true
```

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py use_sim_time:=true
```

> ⚠️ **`use_sim_time:=true` nicht vergessen.** Ohne das benutzen AMCL und Nav2 die
> Systemuhr, die Simulation aber ihre eigene — die TF-Zeitstempel passen dann
> nicht zusammen, und ihr bekommt „Lookup would require extrapolation into the
> past" oder einen Roboter, der einfach stehenbleibt. Das ist der mit Abstand
> häufigste Fehler in diesem Versuch.

---

## S3.2 Lokalisieren und erstes Ziel

1. In RViz **„2D Pose Estimate"** setzen, passend zur Position in Gazebo. Die
   Laserpunkte müssen danach auf den Wänden liegen.
2. Undocken:

   ```bash
   ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
   ```

3. **„Nav2 Goal"** anklicken und ein Ziel wählen. Beobachtet **gleichzeitig**
   Gazebo (was der Roboter tut) und RViz (was er zu wissen glaubt).

**Frage 1 (Protokoll):** Beschreibt den Unterschied zwischen der Ansicht in
Gazebo und der in RViz. Was davon sieht der Roboter, was davon nur ihr?

---

## S3.3 Hindernisse zur Laufzeit

Das ist der Versuch, für den die Simulation gemacht ist. Während der Roboter
fährt, legt ihr in Gazebo mit dem Würfel-Werkzeug ein Hindernis in seinen Pfad.

**Aufgabe:**

1. Ziel setzen, Hindernis mitten auf den geplanten Pfad legen. Beobachtet die
   lokale Costmap in RViz.
2. Denselben Versuch mit einem Hindernis, das den Gang **komplett** blockiert.
3. Hindernis wieder entfernen, während der Roboter davorsteht.

**Frage 2:** Ab welcher Größe des Hindernisses plant Nav2 um, statt anzuhalten?
**Frage 3:** Was passiert im vollständig blockierten Fall? Wie lange versucht es
Nav2, und was meldet die Konsole?

---

## S3.4 Programmatisch navigieren

Ihr benutzt dieselben Nodes wie im Hardwarezweig, nur mit Simulationszeit:

```bash
ros2 run praktikum_py goto_goal --ros-args -p use_sim_time:=true
```

Die TODOs stehen in `src/praktikum_py/praktikum_py/goto_goal.py`, die Erklärung
in [Versuch 3](../03_navigation.md).

---

## S3.5 Pflichtaufgabe – Route abfahren

```bash
ros2 run praktikum_py patrol --ros-args -p use_sim_time:=true
```

Wegpunkte lest ihr in RViz ab (Mauszeiger über die Karte, x/y unten links).

**Aufgabe:** Fahrt dieselbe Route einmal mit `startFollowWaypoints` und einmal
mit `startThroughPoses`.

**Frage 4:** Worin unterscheidet sich das Fahrverhalten? Nutzt aus, dass ihr die
Fahrt in der Simulation exakt wiederholen könnt — startet für beide Varianten aus
derselben Startpose.

**Frage 5:** Legt bei der zweiten Runde ein Hindernis auf einen Wegpunkt. Wie
reagieren die beiden Varianten unterschiedlich?

---

## S3.6 Zusatz – Reproduzierbarkeit

Startet die Simulation mit einer festen Startpose:

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=maze x:=1.0 y:=0.5 yaw:=1.57
```

**Frage 6:** Fahrt dieselbe Route fünfmal aus exakt derselben Startpose. Wie
stark streuen Fahrzeit und Endpose? Warum ist das Ergebnis trotz identischer
Startbedingungen nicht exakt gleich?

Weiter mit → [Versuch S4: Mehrere Roboter](S4_mehrere_roboter.md)
