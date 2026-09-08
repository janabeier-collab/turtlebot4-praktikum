# Versuch S0 – Simulation installieren und starten

> **Lernziel:** Ihr startet den TurtleBot 4 in Gazebo, findet euch in der
> Simulationsoberfläche zurecht und seht dieselben ROS-2-Topics wie beim echten
> Roboter. Am Ende fährt der simulierte Roboter auf Tastendruck.

Plattform: **ROS 2 Jazzy**, **Ubuntu 24.04**, **Gazebo Harmonic**.

---

## S0.1 Installation

```bash
sudo apt update && sudo apt install ros-jazzy-turtlebot4-simulator ros-jazzy-irobot-create-nodes
```

Das zieht `turtlebot4_gz_bringup`, die Gazebo-Welten und den simulierten Create 3
mit. Auf den Laborrechnern ist das in der Regel schon installiert — prüfen:

```bash
ros2 pkg prefix turtlebot4_gz_bringup
```

---

## S0.2 Wichtig: die Simulation von den echten Robotern trennen

> ⚠️ **Das ist die Stolperfalle Nummer eins im Labor.** Auf den Laborrechnern
> zeigt die `~/.bashrc` über `ROS_DISCOVERY_SERVER` auf einen echten TurtleBot.
> Steht diese Variable, melden sich **auch die Simulationsknoten** bei diesem
> Discovery Server an. Ist der Roboter aus, finden sich eure lokalen Knoten dann
> untereinander nicht — Gazebo läuft, aber `ros2 topic list` bleibt leer.

Deshalb die Simulation immer in einer **eigenen, sauberen Umgebung** starten.
Dafür liegt ein Skript bereit:

```bash
source ~/turtlebot4-praktikum/tools/sim_env.sh
```

Es entfernt Discovery-Server und Super-Client aus der Umgebung und stellt die
automatische Erkennung auf `LOCALHOST` — damit bleibt eure Simulation auf eurem
Rechner und stört die Nachbarplätze nicht (und die euch nicht).

**In jedem Terminal der Simulationsversuche zuerst dieses Skript sourcen**,
nicht `src_ws`. Kontrolle:

```bash
env | grep -E "ROS_DISCOVERY_SERVER|ROS_AUTOMATIC_DISCOVERY_RANGE"
```

Erwartet: kein `ROS_DISCOVERY_SERVER`, dafür `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`.

---

## S0.3 Erster Start

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py
```

Gazebo öffnet sich mit der Welt **warehouse** und einem TurtleBot 4 Standard auf
seiner Ladestation. Der erste Start dauert länger, weil Modelle geladen werden.

Die wichtigsten Startoptionen:

| Argument | Werte | Standard | Bedeutung |
|---|---|---|---|
| `world` | `warehouse`, `depot`, `maze` | `warehouse` | Simulationswelt |
| `model` | `standard`, `lite` | `standard` | Robotermodell |
| `rviz` | `true`, `false` | `false` | RViz gleich mitstarten |
| `slam` | `true`, `false` | `false` | SLAM Toolbox mitstarten |
| `localization` | `true`, `false` | `false` | AMCL mitstarten |
| `nav2` | `true`, `false` | `false` | Nav2 mitstarten |
| `namespace` | z.B. `/robot1` | leer | Namespace des Roboters |
| `x`, `y`, `z`, `yaw` | Zahl | `0.0` | Startpose des Roboters |

Beispiel — Labyrinth mit RViz, Startpose versetzt:

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=maze rviz:=true x:=1.0 y:=0.5
```

---

## S0.4 Gazebo bedienen

- **Simulation läuft?** Unten links Play/Pause. Nach dem Start ist die Uhr aktiv;
  bei pausierter Simulation passiert in ROS gar nichts (und ihr sucht den Fehler
  im Code, wo keiner ist).
- **Navigieren:** linke Maustaste = drehen, mittlere/Scrollrad = zoomen,
  Shift + linke Maustaste = schwenken.
- **Objekte einfügen:** oben die Formen-Buttons (Würfel, Kugel, Zylinder) — so
  legt ihr in Versuch S3 ein Hindernis in den Weg.
- **Roboter versetzen:** Werkzeug „Translate", dann den Roboter ziehen. In der
  Realität heißt das „hochheben und woanders hinstellen" — Odometrie und
  Lokalisierung reagieren entsprechend verwirrt.
- **Teleop-Panel:** In der rechten Seitenleiste gibt es ein Teleop-Widget, das
  auf das Gazebo-Topic `/cmd_vel` sendet. Praktisch zum schnellen Ausprobieren,
  für die Versuche nutzt ihr aber die ROS-Werkzeuge.

---

## S0.5 Der ROS-2-Graph der Simulation

Zweites Terminal (wieder `source tools/sim_env.sh`):

```bash
ros2 topic list
```

Ihr solltet dieselben Topics wie beim echten Roboter sehen: `/scan`, `/odom`,
`/cmd_vel_unstamped`, `/battery_state`, `/dock_status`, `/tf`. Genau deshalb
läuft euer Praktikumscode später unverändert auf der Hardware.

Ein Unterschied ist wichtig: die Simulation hat ihre **eigene Uhr**. Jeder Knoten,
der Zeitstempel oder TF benutzt, muss das wissen:

```bash
ros2 topic echo /clock --once
```

Eigene Nodes startet ihr in der Simulation deshalb mit:

```bash
ros2 run praktikum_py hello_node --ros-args -p use_sim_time:=true
```

Die mitgelieferten Launch-Files der Simulation setzen `use_sim_time` selbst.

---

## S0.6 Workspace bauen

Der Praktikumscode ist derselbe wie im Hardwarezweig:

```bash
cd ~/turtlebot4-praktikum && colcon build --symlink-install && source install/setup.bash
```

`tools/sim_env.sh` sourct den Workspace automatisch mit, falls er schon gebaut ist.

---

## S0.7 Checkliste vor Versuch S1

- [ ] `ros2 pkg prefix turtlebot4_gz_bringup` liefert einen Pfad
- [ ] `source tools/sim_env.sh` ausgeführt, `ROS_DISCOVERY_SERVER` ist weg
- [ ] Gazebo startet und zeigt den TurtleBot auf der Dock
- [ ] Simulation läuft (Play gedrückt), `/clock` liefert Werte
- [ ] `ros2 topic list` zeigt `/scan`, `/odom`, `/cmd_vel_unstamped`, `/dock_status`
- [ ] `colcon build` läuft fehlerfrei

Probleme? → [troubleshooting.md](../troubleshooting.md), Abschnitt Simulation.

Weiter mit → [Versuch S1: Fahren](S1_fahren.md)
