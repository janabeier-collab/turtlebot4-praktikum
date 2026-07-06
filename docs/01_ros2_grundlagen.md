# Versuch 1 – ROS 2 Grundlagen

> **Lernziele:** Ihr versteht den ROS-2-Graphen (Nodes, Topics, Services,
> Parameter), nutzt die Kommandozeilen-Tools und schreibt eigene Python-Nodes,
> die den TurtleBot 4 steuern und seine Sensordaten lesen.
>
> **Dauer:** ca. ein Praktikumstermin · **Voraussetzung:** [Versuch 0](00_setup.md) abgeschlossen.

In jedem Terminal zuerst die Umgebung laden: `src_ws` (siehe Versuch 0).

---

## 1.1 Konzepte (kurz)

- **Node** – ein Programm/Baustein mit einer Aufgabe (z.B. „Akku überwachen").
- **Topic** – benannter Datenstrom; **Publisher** senden, **Subscriber** empfangen
  (asynchron, viele-zu-viele). Beispiel: `/cmd_vel`, `/scan`.
- **Message** – Datentyp eines Topics, z.B. `geometry_msgs/Twist`.
- **Service** – synchroner Request/Response-Aufruf (einmalig, mit Antwort).
- **Parameter** – konfigurierbare Werte eines Nodes zur Laufzeit.
- **Launch-File** – startet mehrere Nodes mit Parametern auf einmal.

```
   /battery_state          /cmd_vel
TurtleBot ──topic──> [euer Node] ──topic──> TurtleBot (Antrieb)
 (Publisher)          (Sub + Pub)            (Subscriber)
```

---

## 1.2 Den ROS-Graphen erkunden (nur Kommandozeile)

Probiert der Reihe nach aus und notiert die Ausgaben:

```bash
ros2 node list                     # welche Nodes laufen gerade?
ros2 topic list                    # welche Topics gibt es?
ros2 topic info /cmd_vel           # Typ + Anzahl Pub/Sub
ros2 interface show geometry_msgs/msg/Twist   # Aufbau der Nachricht
ros2 topic echo /battery_state     # Live-Daten anschauen (Strg+C beendet)
ros2 topic hz /scan                # Publish-Rate des Laserscanners
```

**Frage 1 (Protokoll):** Welchen Typ hat `/cmd_vel`, und welche Felder bestimmen
Vorwärts- bzw. Drehbewegung?

### Roboter manuell bewegen (zum Gefühl bekommen)

```bash
# Vorsicht: freie Fläche! Eine einzelne Twist-Nachricht senden:
ros2 topic pub --once /cmd_vel_unstamped geometry_msgs/msg/Twist \
  "{linear: {x: 0.1}, angular: {z: 0.0}}"
```

## 1.3 Referenz-Node lesen: `hello_node`

Öffnet `src/praktikum_py/praktikum_py/hello_node.py`. Dieser Node ist vollständig
und zeigt das Grundgerüst (Klasse, `__init__`, Timer, Parameter, `main`).

```bash
ros2 run praktikum_py hello_node
ros2 run praktikum_py hello_node --ros-args -p name:=Lübeck   # Parameter setzen
```

**Frage 2:** Was passiert, wenn ihr den Parameter `name` ändert? Wie oft feuert
der Timer pro Sekunde?

---

## 1.4 Aufgabe A – Publisher: Quadrat fahren (`square_driver`)

Datei: `src/praktikum_py/praktikum_py/square_driver.py` – enthält **TODOs**.

Ziel: Der Roboter fährt ein Quadrat mit einstellbarer Seitenlänge.

1. **TODO 1:** Publisher auf `/cmd_vel_unstamped` (Typ `Twist`) anlegen.
2. **TODO 2:** Timer (z.B. 10 Hz) einrichten.
3. **TODO 3:** Zustandsautomat „geradeaus → 90° drehen", viermal, dann stoppen.

Bauen & testen (**erst aufgebockt / in freier Fläche, mit Aufsicht!**):

```bash
cd ~/turtlebot4-praktikum && colcon build --symlink-install && src_ws
ros2 run praktikum_py square_driver --ros-args -p side_length:=0.5 -p linear_speed:=0.15
```

**Sicherheit:** Hand am „Not-Aus" (Roboter anheben). Erst kleine Geschwindigkeiten.

**Frage 3:** Wie genau wird das Quadrat? Woran liegen Abweichungen (Reibung,
Timing, Odometrie)? Notiert Beobachtungen.

> **Zusatz (optional):** Statt fester Zeiten die Drehung über `/odom` (Topic
> `nav_msgs/Odometry`) regeln – also drehen, bis 90° erreicht sind.

---

## 1.5 Aufgabe B – Subscriber: Akku überwachen (`battery_listener`)

Datei: `src/praktikum_py/praktikum_py/battery_listener.py` – enthält **TODOs**.

1. **TODO 1:** Subscriber auf `/battery_state` (Typ `BatteryState`).
2. **TODO 2:** Ladezustand in % ausgeben; Warnung unter 15 %.

```bash
ros2 run praktikum_py battery_listener
```

**Frage 4:** Mit welcher Rate kommen die Akku-Nachrichten (`ros2 topic hz`)?

---

## 1.6 Aufgabe C – Launch-File

Schaut euch `src/praktikum_py/launch/demo.launch.py` an und startet es:

```bash
ros2 launch praktikum_py demo.launch.py name:=Mobile-Systeme
```

**Aufgabe:** Erweitert das Launch-File so, dass es zusätzlich euren
`battery_listener` startet. (Zweiten `Node(...)`-Eintrag ergänzen.)

---

## 1.7 Abgabe Versuch 1

- Ausgefüllte `square_driver.py` und `battery_listener.py` (TODOs gelöst).
- Erweitertes `demo.launch.py`.
- Protokoll mit Antworten auf Fragen 1–4 und kurzer Beschreibung eurer Lösung.

Weiter mit → [Versuch 2: SLAM](02_slam.md)

---

### Nützliche Befehle für diesen Versuch

```bash
ros2 run <pkg> <executable>
ros2 launch <pkg> <file.launch.py>
ros2 topic list | info | echo | hz | pub
ros2 interface show <msg-typ>
ros2 param list / get / set
ros2 node info <node>
rqt_graph        # grafische Ansicht des Node/Topic-Graphen
```
