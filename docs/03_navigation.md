# Versuch 3 – Navigation mit Nav2

> **Lernziele:** Ihr lokalisiert den TurtleBot 4 auf eurer Karte, lasst ihn mit
> **Nav2** autonom und kollisionsfrei zu Zielpunkten fahren – erst per RViz,
> dann programmatisch über die `TurtleBot4Navigator`-API.
>
> **Voraussetzung:** [Versuch 2](02_slam.md) abgeschlossen, Karte `labor_map` gespeichert.

In jedem Terminal: `src_ws`. Ihr braucht **2–3 Terminals**.

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
> die Karte fix; AMCL *lokalisiert* nur noch darin. Also `slam:=off`,
> `localization:=true`.

---

## 3.2 Navigation starten

**Terminal 1 – Nav2 + Localization mit eurer Karte:**

```bash
src_ws
ros2 launch turtlebot4_navigation nav_bringup.launch.py \
  slam:=off \
  localization:=true \
  map:=$HOME/turtlebot4-praktikum/maps/labor_map.yaml
```

> Mit Namespace zusätzlich `namespace:=/tb01` anhängen.

**Terminal 2 – RViz:**

```bash
src_ws
ros2 launch turtlebot4_viz view_robot.launch.py
```

---

## 3.3 Lokalisieren und manuell navigieren (RViz)

1. **Startpose setzen:** In RViz **„2D Pose Estimate"** anklicken und dort auf der
   Karte ziehen, wo der Roboter **wirklich** steht (Pfeil = Blickrichtung). Die
   Laserscan-Punkte sollten danach gut auf den Wänden liegen.
2. **Ziel setzen:** **„Nav2 Goal"** anklicken und ein Ziel auf der Karte wählen.
3. Der Roboter plant einen Pfad und fährt los. Beobachtet Pfad (Linie) und Costmaps.

**Frage 1 (Protokoll):** Was passiert, wenn ihr während der Fahrt ein Hindernis
(z.B. einen Karton) in den Weg stellt? Beschreibt das Verhalten.

> ⚠️ **Sicherheit:** Freie Fläche, Aufsicht, Not-Aus (anheben) bereit.

---

## 3.4 Programmatisch navigieren (`goto_goal`)

Jetzt steuert ihr die Navigation aus eigenem Code. Datei:
`src/praktikum_py/praktikum_py/goto_goal.py` – enthält **TODOs**.

Genutzt wird die `TurtleBot4Navigator`-API (Wrapper um Nav2):

```python
from turtlebot4_navigation.turtlebot4_navigator import (
    TurtleBot4Navigator, TurtleBot4Directions)

navigator = TurtleBot4Navigator()
navigator.waitUntilNav2Active()                       # wartet, bis Nav2 bereit
goal = navigator.getPoseStamped([1.0, 0.5], TurtleBot4Directions.NORTH)
navigator.startToPose(goal)                           # fährt zum Ziel
print(navigator.getResult())                          # Ergebnis (SUCCEEDED/...)
```

Aufgaben:

1. **TODO 1–4** in `goto_goal.py` umsetzen (Navigator erzeugen, auf Nav2 warten,
   Ziel anfahren, Ergebnis ausgeben).
2. Bauen & starten (Nav2 muss aus 3.2 laufen, Startpose aus 3.3 gesetzt sein):

   ```bash
   cd ~/turtlebot4-praktikum && colcon build --symlink-install && src_ws
   ros2 run praktikum_py goto_goal
   ```

**Aufgabe (Pflicht):** Erweitert `goto_goal` so, dass der Roboter **nacheinander
mehrere Zielpunkte** abfährt (eine Liste von Posen, z.B. eine Patrouille).
Tipp: Schleife über mehrere `startToPose(...)`-Aufrufe.

**Frage 2:** Wie reagiert die Wegplanung, wenn ein Ziel nicht erreichbar ist
(z.B. hinter einer Wand)? Was liefert `getResult()`?

---

## 3.5 Abgabe Versuch 3

- Ausgefüllte `goto_goal.py` inkl. Mehrziel-Erweiterung.
- Protokoll mit Antworten auf Fragen 1–2 und kurzer Beschreibung.
- Optional: kurzes Video/GIF einer autonomen Fahrt.

---

### Wichtige Befehle

```bash
# Navigation mit gespeicherter Karte:
ros2 launch turtlebot4_navigation nav_bringup.launch.py \
    slam:=off localization:=true map:=<pfad>/labor_map.yaml [namespace:=/tbXX]

# Visualisierung:
ros2 launch turtlebot4_viz view_robot.launch.py

# Eigener Navigations-Node:
ros2 run praktikum_py goto_goal
```

*Quelle: TurtleBot 4 User Manual – Navigation & TurtleBot4Navigator; Nav2 Doku.*
