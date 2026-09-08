# Robotercheck – Abnahme aller TurtleBot 4 und Laborplätze

> Für **Betreuung**, nicht für Studierende. Ziel: jeder TurtleBot 4 (Standard-
> geräte **und** Ersatzgeräte) und jeder Laborplatz ist nachweislich lauffähig,
> und das Ergebnis ist dokumentiert.

Ergänzende Dateien: [Inventar](inventar.md) · [Protokollvorlage](protokoll_vorlage.md) ·
Skript `tools/tb4_check.sh`

---

## Ablauf in Kürze

Pro Roboter etwa **30–40 Minuten**, davon 10 Minuten automatisiert:

| Stufe | Inhalt | Dauer |
|---|---|---|
| 1 | Hardware-Sichtprüfung | 5 min |
| 2 | Boot & Netzwerk | 5 min |
| 3 | Automatischer Check (`tb4_check.sh`) | 5 min |
| 4 | Antriebstest (`--drive`) | 5 min |
| 5 | SLAM-Kurzkarte | 10 min |
| 6 | Nav2 + Route (`patrol`) | 10 min |
| 7 | Andocken & Laden, Protokoll | 5 min |

Reihenfolge nicht abkürzen: Stufe 3 findet die meisten Fehler, bevor der
Roboter überhaupt fährt.

---

## Stufe 1 – Hardware-Sichtprüfung

- [ ] **Aufkleber** lesbar: Domain ID + MAC → ins [Inventar](inventar.md) übertragen
- [ ] **Räder** frei, kein Haar/Kabel um die Achsen, Laufflächen nicht abgefahren
- [ ] **Bumper** federt zurück, keine sichtbaren Risse
- [ ] **RPLIDAR** dreht frei, Kuppel sauber (Staub verfälscht Scans)
- [ ] **OAK-D-Kamera** fest, Linse sauber
- [ ] **Dock-Kontakte** an Roboter und Ladestation sauber (oxidiert = lädt nicht)
- [ ] **Ladestation** steht frei: ca. 0,5 m seitlich und 1 m nach vorn Platz,
      keine spiegelnde Fläche direkt dahinter
- [ ] **Display** (nur Standard-Modell) zeigt Menü, Tasten reagieren
- [ ] **USB-C / Kabel** am Raspberry Pi fest

## Stufe 2 – Boot & Netzwerk

1. Roboter auf die Ladestation setzen, einschalten, **1–2 Minuten** hochfahren lassen.
2. Am Laborplatz: Display des Roboters zeigt die IP – oder IP über die MAC ermitteln:

   ```bash
   ip neigh | grep -i "<MAC-mit-doppelpunkten>"
   ```

3. Erreichbarkeit und SSH prüfen:

   ```bash
   ssh ubuntu@<ROBOTER-IP>
   ```

4. Auf dem Roboter Konfiguration und Versionen ablesen:

   ```bash
   turtlebot4-setup
   ```

   Notieren: **Domain ID**, **Discovery-Server-Rolle/IP**, **WLAN-SSID**,
   ROS-Distro und Paketversion (`ros2 pkg xml turtlebot4_bringup`).
5. Create-3-Firmware im Web-Interface ablesen: `http://<ROBOTER-IP>:8080`
   → Version ins Inventar. **Alle Roboter sollten dieselbe Firmware haben.**

## Stufe 3 – Automatischer Check

Am Laborplatz, dessen `~/.bashrc` auf genau diesen Roboter zeigt:

```bash
./tools/tb4_check.sh --robot tb01
```

Das Skript prüft ROS-Umgebung, installierte Pakete, Erreichbarkeit, alle
Pflicht-Topics, Scan-/Odom-Raten, Akku, Dockstatus und Diagnostics. Ausgabe
gleich mitschreiben:

```bash
mkdir -p ~/tb4-berichte && ./tools/tb4_check.sh --robot tb01 | tee ~/tb4-berichte/tb01.txt
```

Bei `[FEHLT]`-Zeilen zuerst [troubleshooting.md](../troubleshooting.md) abarbeiten.

## Stufe 4 – Antriebstest

Freie Fläche herstellen, dann:

```bash
./tools/tb4_check.sh --robot tb01 --drive
```

Der Roboter undockt, fährt 0,5 m, dreht 180°, fährt zurück, dreht zurück und
dockt wieder an. Dabei beobachten:

- [ ] fährt **geradeaus** (Ziehen zur Seite → Rad/Reifen/Odometrie prüfen)
- [ ] Drehung ist rund, kein Rucken
- [ ] **Andocken klappt beim ersten Versuch** (sonst: Dock-Umgebung prüfen, IR-Fenster sauber?)
- [ ] Ladeanzeige geht an, `percentage` steigt nach 2 Minuten messbar

## Stufe 5 – SLAM-Kurzkarte

Drei Terminals, wie in [Versuch 2](../02_slam.md):

```bash
ros2 launch turtlebot4_navigation slam.launch.py
```

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py
```

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
```

Einmal die Praktikumsfläche umrunden und die Schleife schließen, dann speichern:

```bash
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name: {data: '/home/thlstudent/turtlebot4-praktikum/maps/labor_map'}"
```

- [ ] Wände sind einfach, nicht doppelt
- [ ] `.pgm` und `.yaml` liegen in `maps/`

> Für die Abnahme genügt eine kleine Karte. **Eine** saubere Referenzkarte des
> Labors reicht für alle Roboter – die weiteren Geräte werden gegen diese
> Referenzkarte navigiert. Spart pro Roboter rund 10 Minuten.

## Stufe 6 – Nav2 + Route

```bash
ros2 launch turtlebot4_navigation localization.launch.py map:=$HOME/turtlebot4-praktikum/maps/labor_map.yaml
```

```bash
ros2 launch turtlebot4_navigation nav2.launch.py
```

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py
```

- [ ] „2D Pose Estimate" gesetzt, Scanpunkte liegen auf den Wänden
- [ ] „Nav2 Goal": Roboter erreicht das Ziel
- [ ] Hindernis (Karton) in den Weg: Roboter plant um, fährt nicht dagegen
- [ ] `ros2 run praktikum_py patrol` fährt die Route und dockt am Ende an

## Stufe 7 – Abschluss

- [ ] Roboter dockt, lädt, wird ausgeschaltet oder zum Laden stehen gelassen
- [ ] [Protokoll](protokoll_vorlage.md) ausgefüllt, Befund im [Inventar](inventar.md) eingetragen
- [ ] Auffälligkeiten (Rad schleift, Dock hakt, Akku schwach) direkt vermerken

---

## Laborplatz-Check (7 Plätze)

Für **jeden** Rechner, inklusive des 7. Platzes in der Ecke:

- [ ] Ubuntu 24.04 + ROS 2 Jazzy vorhanden (`ros2 --version`)
- [ ] `~/.bashrc` enthält `ROS_DOMAIN_ID`, `ROS_DISCOVERY_SERVER`,
      `RMW_IMPLEMENTATION=rmw_fastrtps_cpp`, `ROS_SUPER_CLIENT=true`
      und zeigt auf den **richtigen** Roboter
- [ ] Stufe 3 des Skripts läuft ohne `[FEHLT]`:

  ```bash
  ./tools/tb4_check.sh --robot platz7
  ```

- [ ] Repo klonbar und baubar:

  ```bash
  cd ~ && git clone https://github.com/janabeier-collab/turtlebot4-praktikum.git && cd turtlebot4-praktikum && colcon build --symlink-install
  ```

- [ ] `rviz2` startet flüssig (Grafiktreiber! Nicht nur leeres `rviz2` testen,
      sondern `view_navigation.launch.py` mit Karte)
- [ ] `ros2 run praktikum_py hello_node` läuft
- [ ] WLAN-Verbindung stabil
- [ ] Der Platz kann **live** einen TB4 fahren (Stufen 3–6 einmal komplett)

> **7. Platz besonders prüfen:** Er ist nicht Teil des Standard-Rollouts. Häufige
> Abweichungen: andere Domain-ID in der `~/.bashrc`, fehlende Pakete
> (`turtlebot4_navigation`, `teleop_twist_keyboard`), älterer Grafiktreiber,
> anderes WLAN-Profil. Die ersten drei deckt das Skript ab.

---

## Ersatzroboter

Zusätzlich zu den Stufen 1–7:

- [ ] Domain ID **eindeutig**, kollidiert mit keinem Standardroboter
- [ ] Create-3-Firmware auf demselben Stand wie die Standardgeräte
- [ ] Nach erfolgreicher Abnahme ein **SD-Karten-Image** ziehen (TurtleBot-4-Handbuch,
      *Creating a backup of your SD card*) und mit Datum + Robotername beschriften.
      Das ist die schnellste Reparatur, wenn im Praktikum ein Roboter ausfällt.
- [ ] Akku geladen einlagern, alle 2–3 Monate nachladen
