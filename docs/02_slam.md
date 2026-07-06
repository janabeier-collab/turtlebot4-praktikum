# Versuch 2 – SLAM: Eine Karte des Labors erstellen

> **Lernziele:** Ihr versteht das Prinzip von SLAM (Simultaneous Localization and
> Mapping), erstellt mit dem TurtleBot 4 und der SLAM Toolbox eine Karte des
> Labors und speichert sie für die spätere Navigation (Versuch 3).
>
> **Voraussetzung:** [Versuch 1](01_ros2_grundlagen.md) abgeschlossen. Verbindung steht.

In jedem Terminal: `src_ws`. Ihr braucht für diesen Versuch **3 Terminals**.

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

## 2.2 SLAM starten

**Terminal 1 – SLAM:**

```bash
src_ws
ros2 launch turtlebot4_navigation slam.launch.py
```

> Falls euer Roboter einen Namespace hat:
> `ros2 launch turtlebot4_navigation slam.launch.py namespace:=/tb01`

**Terminal 2 – Visualisierung (RViz):**

```bash
src_ws
ros2 launch turtlebot4_viz view_robot.launch.py
```

In RViz seht ihr, wie die Karte entsteht. Anzeigen prüfen: **Map**, **LaserScan**,
**RobotModel**, **TF**. Fixed Frame muss `map` sein.

---

## 2.3 Das Labor kartieren

**Terminal 3 – Teleop (Roboter manuell fahren):**

```bash
src_ws
# teleop sendet standardmäßig auf 'cmd_vel' – unser Roboter hört auf
# 'cmd_vel_unstamped', daher umbiegen (remap):
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
# Falls Namespace nötig:
# ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/tb01/cmd_vel_unstamped
```

Steuerung (Fenster muss im Fokus sein): Tasten `i/j/k/l/,` usw.

**Vorgehen für eine gute Karte:**

1. **Langsam** fahren – schnelle Drehungen verschmieren die Karte.
2. Den Raum **systematisch** abfahren, an den Wänden entlang.
3. Mindestens einmal eine **Schleife** schließen (zum Ausgangspunkt zurück) –
   das verbessert die Genauigkeit (Loop Closure).
4. In RViz prüfen, dass keine „doppelten" Wände entstehen.

> ⚠️ **Sicherheit:** Freie Fläche, niemand im Fahrweg, Not-Aus (anheben) bereit.

---

## 2.4 Karte speichern

Wenn die Karte vollständig ist, in einem **neuen Terminal**:

```bash
src_ws
cd ~/turtlebot4-praktikum/maps
ros2 run nav2_map_server map_saver_cli -f labor_map
```

Das erzeugt zwei Dateien:

- `labor_map.pgm` – das Bild der Karte (Graustufen: frei / belegt / unbekannt)
- `labor_map.yaml` – Metadaten (Auflösung, Ursprung, Schwellwerte)

Diese braucht ihr in **Versuch 3** für die Navigation.

> Alternativ kann die SLAM Toolbox eine *serialisierte* Karte speichern
> (`Serialize Map` im SLAM-Toolbox-RViz-Panel) – für reines Nav2 reicht das
> `.pgm/.yaml`-Paar aus `map_saver_cli`.

---

## 2.5 Aufgaben & Protokoll

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
ros2 launch turtlebot4_navigation slam.launch.py [namespace:=/tbXX]
ros2 launch turtlebot4_viz view_robot.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 run nav2_map_server map_saver_cli -f <name>
```
