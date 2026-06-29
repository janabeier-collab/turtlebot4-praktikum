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
├── maps/                     ← hier speichert ihr eure SLAM-Karten
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

---

## Abgabe

Pro Gruppe ein **Fork dieses Repos** mit ausgefüllten TODO-Stellen und einem kurzen
Protokoll je Versuch (`docs/protokoll_gruppeXX.md`). Details gibt die Betreuung bekannt.
