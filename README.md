# Praktikum Mobile Robotik – TurtleBot 4

Begleitmaterial zum **Mobile Robotik Praktikum** (Vorlesung *Mobile Systeme*)
am Institut für Regelungstechnik und Mobile Systeme, TH Lübeck.

Plattform: **TurtleBot 4 Standard** · **ROS 2 Jazzy Jalisco** (Ubuntu 24.04) ·
Arbeitsweise: Linux-Laborrechner → **SSH** auf den TurtleBot im Labor-WLAN.

---

## Worum geht es?

Ihr lernt in drei aufeinander aufbauenden Versuchen, einen realen mobilen Roboter
mit ROS 2 zu programmieren und autonom fahren zu lassen:

| Versuch | Thema | Anleitung |
|--------:|-------|-----------|
| **0** | Setup: Netzwerk, SSH, Workspace | [docs/00_setup.md](docs/00_setup.md) |
| **1** | ROS 2 Grundlagen: Nodes, Topics, Services, Launch | [docs/01_ros2_grundlagen.md](docs/01_ros2_grundlagen.md) |
| **2** | SLAM: eine Karte des Labors erstellen | [docs/02_slam.md](docs/02_slam.md) |
| **3** | Navigation: autonom zum Ziel fahren (Nav2) | [docs/03_navigation.md](docs/03_navigation.md) |

Hilfreich nebenbei: [Cheatsheet](docs/cheatsheet.md) · [Troubleshooting](docs/troubleshooting.md)

### Ohne Roboter: das Simulationspraktikum

Ein eigenständiger Zweig, der komplett in **Gazebo** läuft — zur Vorbereitung,
als Ersatztermin oder zur Fehlersuche. Derselbe Code, kein Roboter nötig.

| Versuch | Thema | Anleitung |
|--------:|-------|-----------|
| **S0** | Simulation installieren und starten | [docs/simulation/S0_setup.md](docs/simulation/S0_setup.md) |
| **S1** | Fahren und ROS-2-Grundlagen | [docs/simulation/S1_fahren.md](docs/simulation/S1_fahren.md) |
| **S2** | SLAM im Labyrinth | [docs/simulation/S2_slam.md](docs/simulation/S2_slam.md) |
| **S3** | Navigation und Routen | [docs/simulation/S3_navigation.md](docs/simulation/S3_navigation.md) |
| **S4** | Mehrere Roboter gleichzeitig | [docs/simulation/S4_mehrere_roboter.md](docs/simulation/S4_mehrere_roboter.md) |

Übersicht und Vergleich: [docs/simulation/README.md](docs/simulation/README.md) ·
[Simulation ↔ echter Roboter](docs/simulation/unterschiede.md)

Für die **Betreuung**: [Robotercheck & Abnahme](docs/betreuung/robotercheck.md) ·
[Inventar](docs/betreuung/inventar.md) · [Protokollvorlage](docs/betreuung/protokoll_vorlage.md)

---

## Schnellstart (für ungeduldige)

```bash
# 1. Repo in euren Home-Ordner klonen
cd ~
git clone <REPO-URL> turtlebot4-praktikum
cd turtlebot4-praktikum

# 2. ROS 2 Umgebung laden (in JEDEM neuen Terminal nötig)
source /opt/ros/jazzy/setup.bash

# 3. Workspace bauen
colcon build --symlink-install
source install/setup.bash

# 4. Verbindung zum Roboter prüfen
ros2 topic list      # sollte Topics des TurtleBot zeigen (z.B. /battery_state)
```

> Komplettes, schrittweises Setup inkl. Labor-WLAN und Discovery Server:
> **[docs/00_setup.md](docs/00_setup.md)** – bitte zuerst lesen.

---

## Repo-Struktur

```
turtlebot4-praktikum/
├── README.md                 ← diese Datei
├── docs/                     ← alle Praktikumsanleitungen
│   ├── simulation/           ← Simulationspraktikum (Gazebo, ohne Roboter)
│   └── betreuung/            ← Abnahme & Inventar (nicht für Studierende)
├── maps/                     ← hier speichert ihr eure SLAM-Karten
├── tools/
│   ├── tb4_check.sh          ← Schnelltest eines Roboters/Laborplatzes
│   └── sim_env.sh            ← Umgebung für die Simulation (source!)
└── src/
    ├── praktikum_py/         ← euer Python-Paket (hier schreibt ihr Code, TODOs!)
    └── praktikum_bringup/    ← Launch-Files, die mehrere Nodes starten
```

`build/`, `install/`, `log/` entstehen beim Bauen und werden **nicht** eingecheckt
(siehe `.gitignore`).

---

## Wichtige Konventionen

- **Kein `sudo` nötig.** Alle Praktikumsschritte laufen im eigenen Home-Verzeichnis.
  Falls ein Schritt nach Root-Rechten verlangt, ist etwas falsch – fragt die Betreuung.
- **Ein Terminal = eine Aufgabe.** ROS 2 braucht oft mehrere Terminals parallel
  (Roboter, Visualisierung, eigener Node). Nutzt `tmux` oder mehrere VS-Code-Terminals.
- **Sicherheit zuerst.** Vor jedem Fahrversuch: freie Fläche, Not-Aus (Roboter
  hochheben) bereithalten, niemand steht im Fahrweg.
- **Erst undocken, dann fahren.** Der Roboter startet auf seiner Ladestation:
  `ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"`.


