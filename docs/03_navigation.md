# Versuch 3 – Navigation mit Nav2

> **Lernziele:** Ihr lokalisiert den TurtleBot 4 auf eurer Karte, lasst ihn mit
> **Nav2** autonom und kollisionsfrei zu Zielpunkten fahren – erst per RViz,
> dann programmatisch über die `TurtleBot4Navigator`-API, und am Ende eine
> ganze **Route** aus mehreren Wegpunkten.
>
> **Voraussetzung:** [Versuch 2](02_slam.md) abgeschlossen, Karte `labor_map` gespeichert.

In jedem Terminal: `src_ws`. Ihr braucht **3–4 Terminals**.

---

## 3.1 Was macht Nav2?

Nav2 ist der ROS-2-Navigations-Stack. Bei bekannter Karte:

- **Localization (AMCL)** schätzt fortlaufend die Pose des Roboters auf der Karte.
- **Global Planner** plant einen Pfad vom Start zum Ziel.
- **Controller** (bei Jazzy standardmäßig **MPPI**) folgt dem Pfad und weicht
  dynamischen Hindernissen aus.
- **Costmaps** kombinieren Karte + Live-Laserscan zu „befahrbar / gefährlich".

```
Karte (labor_map) ─┐
/scan ─────────────┼──> Nav2 ──> /cmd_vel ──> Roboter fährt zum Ziel
Zielpose ──────────┘
```

> **SLAM vs. Localization:** In Versuch 2 hat SLAM die Karte *gebaut*. Jetzt ist
> die Karte fix; AMCL *lokalisiert* nur noch darin.
>
> **Randnotiz zu `cmd_vel`:** Nav2 unter Jazzy publiziert `TwistStamped` auf
> `/cmd_vel` (`enable_stamped_cmd_vel: true` in der Nav2-Config). Euer eigener
> Code aus Versuch 1 nutzt dagegen weiterhin `/cmd_vel_unstamped` mit `Twist` –
> beides landet über den Republisher beim gleichen Antrieb.

---

## 3.2 Navigation starten

Die Navigation besteht aus **zwei** Launch-Files: Localization (Karte + AMCL)
und Nav2 (Planner + Controller). Sie werden nacheinander gestartet.

> Ein früher übliches `nav_bringup.launch.py` mit `slam:=off localization:=true`
> gibt es in ROS 2 Jazzy **nicht mehr**. Wer das noch in alten Anleitungen
> findet, bekommt „file not found".

**Terminal 1 – Localization mit eurer Karte:**

```bash
ros2 launch turtlebot4_navigation localization.launch.py map:=$HOME/turtlebot4-praktikum/maps/labor_map.yaml
```

**Terminal 2 – Nav2:**

```bash
ros2 launch turtlebot4_navigation nav2.launch.py
```

**Terminal 3 – RViz:**

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py
```

> Mit Namespace bei **allen dreien** zusätzlich `namespace:=/tb01` anhängen.
> Den Kartenpfad immer **absolut** angeben (`$HOME/...`), sonst findet der
> map_server die Datei nicht.

---

## 3.3 Lokalisieren und manuell navigieren (RViz)

1. **Startpose setzen:** In RViz **„2D Pose Estimate"** anklicken und dort auf der
   Karte ziehen, wo der Roboter **wirklich** steht (Pfeil = Blickrichtung). Die
   Laserscan-Punkte sollten danach gut auf den Wänden liegen. Ohne diesen Schritt
   startet Nav2 nicht – AMCL braucht eine Anfangsschätzung.
2. **Undocken** (falls der Roboter noch auf der Ladestation steht):

   ```bash
   ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
   ```

3. **Ziel setzen:** **„Nav2 Goal"** anklicken und ein Ziel auf der Karte wählen.
4. Der Roboter plant einen Pfad und fährt los. Beobachtet Pfad (Linie) und Costmaps.

**Frage 1 (Protokoll):** Was passiert, wenn ihr während der Fahrt ein Hindernis
(z.B. einen Karton) in den Weg stellt? Beschreibt das Verhalten.

---

## 3.4 Programmatisch navigieren (`goto_goal`)

Jetzt steuert ihr die Navigation aus eigenem Code. Datei:
`src/praktikum_py/praktikum_py/goto_goal.py` – enthält **TODOs**.

Genutzt wird die `TurtleBot4Navigator`-API (Wrapper um Nav2). Der offizielle
Ablauf aus dem TurtleBot-4-Handbuch ist immer der gleiche:

```python
from turtlebot4_navigation.turtlebot4_navigator import (
    TurtleBot4Directions, TurtleBot4Navigator)

navigator = TurtleBot4Navigator()

# 1. Startpose setzen – nur nötig, wenn nicht schon in RViz geschehen.
#    Steht der Roboter auf der Dock, ist die Dock-Pose der übliche Ursprung:
if not navigator.getDockedStatus():
    navigator.info('Roboter nicht gedockt – bitte auf die Dock stellen.')
navigator.setInitialPose(navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH))

# 2. Warten, bis Nav2 vollständig hochgefahren ist
navigator.waitUntilNav2Active()

# 3. Vom Dock runterfahren
navigator.undock()

# 4. Ziel anfahren (blockiert, bis das Ziel erreicht oder abgebrochen ist)
goal = navigator.getPoseStamped([1.0, 0.5], TurtleBot4Directions.NORTH)
navigator.startToPose(goal)

# 5. Zurück auf die Ladestation
navigator.dock()
```

> `startToPose()` **blockiert** bis zum Ende und gibt das Ergebnis selbst auf der
> Konsole aus. Wollt ihr das Ergebnis auswerten, fragt danach `navigator.getResult()`
> ab und vergleicht mit `TaskResult.SUCCEEDED`
> (`from nav2_simple_commander.robot_navigator import TaskResult`).

Aufgaben:

1. **TODO 1–5** in `goto_goal.py` umsetzen.
2. Bauen & starten (Localization + Nav2 aus 3.2 müssen laufen):

   ```bash
   cd ~/turtlebot4-praktikum && colcon build --symlink-install && src_ws && ros2 run praktikum_py goto_goal
   ```

**Frage 2:** Wie reagiert die Wegplanung, wenn ein Ziel nicht erreichbar ist
(z.B. hinter einer Wand)? Was liefert `getResult()`?

---

## 3.5 Pflichtaufgabe – eine Route abfahren (`patrol`)

Datei: `src/praktikum_py/praktikum_py/patrol.py` – enthält **TODOs**.

Der Roboter soll **mehrere Wegpunkte nacheinander** abfahren (Patrouille durch
das Labor) und danach wieder andocken. Die API bietet dafür drei Varianten:

| Methode | Verhalten |
|---|---|
| `startToPose(pose)` | Ein Ziel, blockiert bis fertig. Route = Schleife über mehrere Aufrufe. |
| `startThroughPoses(poses)` | **Ein** durchgehender Plan über alle Posen; Zwischenposen werden nur „gestreift". |
| `startFollowWaypoints(poses)` | Jeder Wegpunkt wird **einzeln angefahren** und erreicht. |

Aufgabe:

1. Definiert eine Liste von mindestens **vier** Wegpunkten in eurer Karte
   (Koordinaten in RViz ablesen: Mauszeiger über die Karte bewegen, unten links
   werden x/y angezeigt).
2. Fahrt die Route einmal mit `startFollowWaypoints(...)` und einmal mit
   `startThroughPoses(...)`.
3. Startet:

   ```bash
   ros2 run praktikum_py patrol
   ```

**Frage 3:** Worin unterscheidet sich das Fahrverhalten der beiden Varianten?
Welche würdet ihr für eine Inspektionsfahrt mit Halt an jeder Station wählen?

**Frage 4:** Fügt einen Screenshot der geplanten Route (RViz, Display `Path`)
ins Protokoll ein.

> **Tipp:** `navigator.createPath()` erzeugt eine Posenliste interaktiv – ihr
> klickt die Wegpunkte in RViz mit „Nav2 Goal" und schließt mit Enter ab.

---

### Wichtige Befehle

```bash
ros2 launch turtlebot4_navigation localization.launch.py map:=$HOME/turtlebot4-praktikum/maps/labor_map.yaml [namespace:=/tbXX]
ros2 launch turtlebot4_navigation nav2.launch.py [namespace:=/tbXX]
ros2 launch turtlebot4_viz view_navigation.launch.py [namespace:=/tbXX]
ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
ros2 run praktikum_py goto_goal
ros2 run praktikum_py patrol
```

*Quelle: TurtleBot 4 User Manual – Navigation & TurtleBot4Navigator; Nav2 Doku.*
