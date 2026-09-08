# Versuch 2 – SLAM: Eine Karte des Labors erstellen

> **Lernziele:** Ihr versteht das Prinzip von SLAM (Simultaneous Localization and
> Mapping), erstellt mit dem TurtleBot 4 und der SLAM Toolbox eine Karte des
> Labors und speichert sie für die spätere Navigation (Versuch 3).
>
> **Voraussetzung:** [Versuch 1](01_ros2_grundlagen.md) abgeschlossen. Verbindung steht.

In jedem Terminal: `src_ws`. Ihr braucht für diesen Versuch **3–4 Terminals**.

---

## 2.1 Was ist SLAM?

Der Roboter weiß weder, wie das Labor aussieht, noch genau, wo er steht. **SLAM**
löst beides gleichzeitig:

- Aus den **Laserscans** (`/scan`, 2D-LiDAR) erkennt er Wände/Hindernisse.
- Aus der **Odometrie** (`/odom`, Rad-/IMU-Daten) schätzt er seine Bewegung.
- Die SLAM Toolbox fügt beides zu einer konsistenten **Karte** (`/map`) zusammen
  und korrigiert dabei die Positionsschätzung (Loop Closure).

```
/scan  ─┐
        ├──>  slam_toolbox  ──>  /map  (+ Pose des Roboters)
/odom  ─┘
```

---

## 2.2 Zuerst: vom Dock runter (Undock)

> ⚠️ **Das ist der Schritt, den fast alle vergessen.** Der TurtleBot steht nach
> dem Einschalten auf seiner Ladestation. Solange er dockt, fährt er nicht
> normal los, und die Karte beginnt mitten in der Dock-Struktur.

```bash
ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
```

Docken könnt ihr am Ende genauso wieder:

```bash
ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"
```

Dockstatus prüfen (Feld `is_docked`):

```bash
ros2 topic echo /dock_status --once
```

> Mit Namespace: `/tb01/undock`, `/tb01/dock`, `/tb01/dock_status`.

---

## 2.3 SLAM starten

**Terminal 1 – SLAM:**

```bash
ros2 launch turtlebot4_navigation slam.launch.py
```

> Falls euer Roboter einen Namespace hat:
> `ros2 launch turtlebot4_navigation slam.launch.py namespace:=/tb01`
>
> `sync:=false` schaltet auf asynchrones SLAM um – nützlich, wenn der Rechner
> nicht hinterherkommt und die Karte ruckelt.

**Terminal 2 – Visualisierung (RViz):**

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py
```

> **Nicht `view_robot.launch.py` nehmen!** Diese Konfiguration enthält kein
> `Map`-Display und kein SLAM-Toolbox-Panel – ihr würdet die entstehende Karte
> schlicht nicht sehen. `view_navigation` bringt Map, Costmaps, Nav2-Panel und
> das SLAM-Toolbox-Panel mit.

In RViz seht ihr, wie die Karte entsteht. Anzeigen prüfen: **Map**, **LaserScan**,
**RobotModel**, **TF**. Fixed Frame muss `map` sein.

---

## 2.4 Das Labor kartieren

**Terminal 3 – Teleop (Roboter manuell fahren):**

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
```

> teleop sendet standardmäßig auf `cmd_vel` – unser Roboter hört auf
> `cmd_vel_unstamped`, daher das Remapping.
> Mit Namespace: `-r cmd_vel:=/tb01/cmd_vel_unstamped`.

Steuerung (Fenster muss im Fokus sein): Tasten `i/j/k/l/,` usw.
Alternativ mit dem **Controller** fahren (siehe [Versuch 1, 1.2](01_ros2_grundlagen.md)).

**Vorgehen für eine gute Karte:**

1. **Langsam** fahren – schnelle Drehungen verschmieren die Karte.
2. Den Raum **systematisch** abfahren, an den Wänden entlang.
3. Mindestens einmal eine **Schleife** schließen (zum Ausgangspunkt zurück) –
   das verbessert die Genauigkeit (Loop Closure).
4. In RViz prüfen, dass keine „doppelten" Wände entstehen.

> ⚠️ **Sicherheit:** Freie Fläche, niemand im Fahrweg, Not-Aus (anheben) bereit.

---

## 2.5 Karte speichern

Wenn die Karte vollständig ist, in einem **neuen Terminal**. Es gibt zwei Wege –
**Weg A ist der aus dem offiziellen Handbuch und der zuverlässigere:**

**Weg A – über den SLAM-Toolbox-Service** (Handbuchweg, im Labor bewährt):

```bash
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name: {data: '/home/<euer-benutzer>/turtlebot4-praktikum/maps/labor_map'}"
```

> ⚠️ **Absoluten Pfad angeben.** Ein relativer Name landet im Arbeitsverzeichnis
> des **slam_toolbox-Knotens**, nicht in dem eures Terminals – ein `cd` vorher
> hilft also nicht, und die Karte taucht irgendwo anders auf. Auf den
> Laborrechnern ist der Benutzer `thlstudent`, der Pfad also
> `/home/thlstudent/turtlebot4-praktikum/maps/labor_map`.

**Weg B – über den map_saver:**

```bash
cd ~/turtlebot4-praktikum/maps && ros2 run nav2_map_server map_saver_cli -f labor_map --ros-args -p map_subscribe_transient_local:=true
```

> Der Parameter `map_subscribe_transient_local:=true` ist wichtig: `/map` wird
> mit QoS *transient local* publiziert. Ohne ihn wartet `map_saver_cli` gern
> ewig und meldet am Ende „Failed to save the map". Bei Namespace zusätzlich
> `-r __ns:=/tb01` anhängen.

Beide Wege erzeugen zwei Dateien:

- `labor_map.pgm` – das Bild der Karte (Graustufen: frei / belegt / unbekannt)
- `labor_map.yaml` – Metadaten (Auflösung, Ursprung, Schwellwerte)

Diese braucht ihr in **Versuch 3** für die Navigation. Kontrolle:

```bash
ls -l ~/turtlebot4-praktikum/maps/
```

> Im RViz-Panel der SLAM Toolbox gibt es zusätzlich `Serialize Map` – das
> erzeugt ein `.posegraph`, mit dem SLAM später *weiterkartieren* kann. Für
> reines Nav2 reicht das `.pgm`/`.yaml`-Paar.

Zum Schluss den Roboter wieder auf die Ladestation schicken:

```bash
ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"
```

---

## 2.6 Aufgaben & Protokoll

1. Kartiert das Labor (oder den zugewiesenen Bereich) und speichert `labor_map`.
2. Fügt einen **Screenshot der RViz-Karte** ins Protokoll ein.
3. **Frage 1:** Was passiert mit der Karte, wenn ihr zu schnell dreht? Probiert es aus.
4. **Frage 2:** Wofür ist Loop Closure gut? Beschreibt eine Stelle, an der es
   eure Karte korrigiert hat.
5. **Frage 3:** Welche Auflösung (Meter/Pixel) steht in eurer `labor_map.yaml`?

Weiter mit → [Versuch 3: Navigation](03_navigation.md)

---

### Wichtige Befehle

```bash
ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
ros2 launch turtlebot4_navigation slam.launch.py [namespace:=/tbXX] [sync:=false]
ros2 launch turtlebot4_viz view_navigation.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name: {data: '/home/<benutzer>/turtlebot4-praktikum/maps/labor_map'}"
ros2 action send_goal /dock irobot_create_msgs/action/Dock "{}"
```
