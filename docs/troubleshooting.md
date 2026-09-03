# Troubleshooting

Häufige Probleme im Praktikum und ihre Lösungen. Wenn nichts hilft: Betreuung fragen.

---

## `ros2 topic list` zeigt keine / kaum Topics des Roboters

1. **Gleiches WLAN?** PC und Roboter müssen im selben Labor-WLAN sein.
2. **Domain-ID stimmt mit dem Aufkleber überein?** (häufigster Fehler!)
   ```bash
   echo $ROS_DOMAIN_ID          # muss EXAKT der "Domain ID" vom Roboter-Aufkleber entsprechen (z.B. 10)
   ```
3. **Umgebung richtig gesetzt?**
   ```bash
   env | grep ROS               # RMW_IMPLEMENTATION=rmw_fastrtps_cpp, ROS_DISCOVERY_SERVER, ROS_SUPER_CLIENT=true
   ```
4. **DDS-Cache zurücksetzen:**
   ```bash
   ros2 daemon stop && ros2 daemon start
   ```
5. **Erreichbarkeit prüfen:** `ping <ROBOTER-IP>`
6. **IP unbekannt / geändert?** IP aus der MAC-Adresse neu ermitteln (siehe
   [00_setup.md](00_setup.md)):
   ```bash
   ip neigh | grep -i "<MAC-mit-doppelpunkten>"
   ```
7. **Roboterseite prüfen** – dabei unbedingt `ssh -t` benutzen, sonst fehlt dem
   Roboter in der Sitzung selbst die Umgebung (siehe Super-Client-Abschnitt oben):

   ```bash
   ssh -t ubuntu@<ROBOTER-IP>
   env | grep ROS && ros2 topic list
   ```

   Sieht der Roboter selbst nur `/parameter_events` und `/rosout`, läuft sein
   ROS-Stack nicht:

   ```bash
   sudo systemctl status turtlebot4.service   # Neustart: turtlebot4-service-restart
   sudo systemctl status discovery.service    # Discovery Server auf dem Roboter
   ```

## Topic-Liste unvollständig – Super Client fehlt

Die Verbindungsdaten des Laborrechners stehen in `/etc/turtlebot4_discovery/setup.bash`
(aus der `~/.bashrc` gesourct). Darin steht:

```bash
[ -t 0 ] && export ROS_SUPER_CLIENT=True || export ROS_SUPER_CLIENT=False
```

`[ -t 0 ]` prüft, ob die Shell ein Terminal ist. **Super Client gibt es also nur in
interaktiven Terminals.** In Skripten, in `ssh rechner "befehl"` und in manchen
VS-Code-Tasks steht der Wert auf `False` – und ohne Super Client seht ihr nur den
Teil des Graphen, mit dem ihr selbst gematcht seid, statt aller Topics.

```bash
echo $ROS_SUPER_CLIENT        # muss True sein
export ROS_SUPER_CLIENT=True  # für diese Shell nachziehen
ros2 daemon stop && ros2 topic list
```

## Nur ein Teil der Topics ist da (`/scan` ja, `/odom` und `/cmd_vel_unstamped` nein)

Das ist der **Create-3-Basis-Fall**: der Raspberry Pi ist oben, die Fahrbasis noch
nicht. Ein bis zwei Minuten warten, sonst Roboter aus- und wieder einschalten.
Bleibt es dabei, im Create-3-Web-Interface (`http://<ROBOTER-IP>:8080`) prüfen,
ob die Basis im Fehlerzustand ist (nur mit Betreuung).

## `command not found: ros2`

ROS 2 nicht gesourct. `source /opt/ros/jazzy/setup.bash` (oder `src_ws`).

## `Package 'praktikum_py' not found` / eigene Nodes nicht startbar

```bash
cd ~/turtlebot4-praktikum
colcon build --symlink-install
source install/setup.bash      # in genau diesem Terminal nötig!
```
Neues Terminal? → wieder `src_ws`.

## `colcon build` schlägt fehl

- Fehlermeldung ganz oben lesen – meist Syntaxfehler in einer `.py`-Datei.
- Nur das betroffene Paket bauen: `colcon build --packages-select praktikum_py`.
- Bei „setup.py / entry_point"-Fehlern: Tippfehler in `setup.py` prüfen.
- Sauberer Neustart: `rm -rf build install log && colcon build --symlink-install`.

## Roboter reagiert nicht auf `/cmd_vel_unstamped`

- **Steht er noch auf der Ladestation?** Erst undocken:
  `ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"`
- **Richtiges Topic?** Fahrbefehle aus eurem Code gehen an `/cmd_vel_unstamped`
  (Typ `Twist`). `/cmd_vel` erwartet unter Jazzy `TwistStamped` und wird von
  Nav2 benutzt. Prüfen: `ros2 topic list | grep cmd_vel`.
- **Namespace?** Vielleicht ist es `/tbXX/cmd_vel_unstamped`.
- Sendet überhaupt jemand? `ros2 topic echo /cmd_vel_unstamped` in zweitem Terminal.
- **teleop bewegt nichts?** teleop sendet auf `cmd_vel` – remappen:
  `--ros-args -r cmd_vel:=/cmd_vel_unstamped`.
- Create-3-Basis im Fehlerzustand? Kurz aus-/einschalten (mit Betreuung).
- Sicherheitsstopp aktiv (Roboter angehoben/gekippt)? Wieder absetzen.

## RViz zeigt keine Karte, obwohl SLAM läuft

Fast immer die **falsche RViz-Konfiguration**: `view_robot.launch.py` enthält
gar kein `Map`-Display und kein SLAM-Toolbox-Panel. Für Versuch 2 und 3 gilt:

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py
```

Sonst: **Fixed Frame** auf `map` setzen, Displays (Map, LaserScan, RobotModel, TF)
ergänzen, TF-Baum prüfen mit `ros2 run tf2_tools view_frames`.

## Karte speichern: `map_saver_cli` hängt oder meldet „Failed to save the map"

`/map` wird mit QoS *transient local* publiziert. Ohne den passenden Parameter
bekommt der Saver nie eine Nachricht:

```bash
ros2 run nav2_map_server map_saver_cli -f labor_map --ros-args -p map_subscribe_transient_local:=true
```

Zuverlässiger ist der Service der SLAM Toolbox (speichert ins aktuelle Verzeichnis):

```bash
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name: {data: 'labor_map'}"
```

Bei Namespace zusätzlich `-r __ns:=/tbXX` bzw. `/tbXX/slam_toolbox/save_map`.

## `nav_bringup.launch.py` nicht gefunden

Dieses Launch-File gibt es in ROS 2 Jazzy **nicht mehr**. Navigation läuft jetzt
in zwei Schritten:

```bash
ros2 launch turtlebot4_navigation localization.launch.py map:=$HOME/turtlebot4-praktikum/maps/labor_map.yaml
```

```bash
ros2 launch turtlebot4_navigation nav2.launch.py
```

## Nav2: Roboter fährt nicht los

- **Startpose gesetzt?** In RViz „2D Pose Estimate" passend zur echten Position –
  ohne Anfangsschätzung bleibt AMCL inaktiv und Nav2 nimmt keine Ziele an.
- Laserscan-Punkte liegen nicht auf den Wänden → Pose neu setzen.
- **Noch gedockt?** Undocken (siehe oben).
- Karte korrekt geladen? Pfad in `map:=...` prüfen (**absoluter** Pfad, `.yaml`).
- Nav2 wirklich aktiv? `ros2 topic echo /diagnostics_agg` bzw. Konsolenausgabe der
  beiden Launch-Files auf Fehler prüfen.
- `waitUntilNav2Active()` hängt ewig? Meist läuft Localization nicht (Terminal 1)
  oder der Namespace passt nicht zusammen.

## Zwei Gruppen stören sich gegenseitig

Jeder Roboter hat eine **eigene Domain-ID** und einen eigenen Discovery Server.
Wenn zwei Rechner dieselbe Domain-ID benutzen, sehen sie beide Roboter und die
Fahrbefehle gehen an den falschen. `echo $ROS_DOMAIN_ID` auf beiden Rechnern
vergleichen. Bei Robotern mit Namespace gehören `namespace:=/tbXX` an **alle**
Launch-Files.

## VS Code Remote-SSH verbindet nicht

- IP/Hostname korrekt? `ssh ubuntu@<IP>` zuerst im Terminal testen.
- Gleiches WLAN, Roboter gebootet.

---

### Allgemeine Diagnose-Reihenfolge

1. Stimmt das Netzwerk? (`ping`, gleiches WLAN)
2. Stimmt die Umgebung? (`env | grep ROS`)
3. Ist das Paket gebaut & gesourct?
4. Stimmt der Topic-Name (Namespace!)?
5. Steht der Roboter noch auf der Dock?
6. Logs lesen – die erste Fehlermeldung zählt.
