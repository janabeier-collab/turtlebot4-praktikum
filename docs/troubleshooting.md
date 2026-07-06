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
   echo $RMW_IMPLEMENTATION     # rmw_fastrtps_cpp
   echo $ROS_DISCOVERY_SERVER   # <ROBOTER-IP>:11811 (falls Discovery Server genutzt)
   ```
4. **DDS-Cache zurücksetzen:**
   ```bash
   ros2 daemon stop && ros2 daemon start
   ```
5. **Erreichbarkeit prüfen:** `ping <ROBOTER-IP>`
6. **IP unbekannt / geändert?** IP aus der MAC-Adresse neu ermitteln (siehe
   [00_setup.md](00_setup.md#021-ip-adresse-aus-der-mac-ermitteln)):
   ```bash
   ip neigh | grep -i "<MAC-mit-doppelpunkten>"
   ```
7. Roboter eingeschaltet und gebootet? (Akku/Display prüfen, ggf. per SSH `ros2 topic list` auf dem Roboter.)

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

- **Richtiges Topic?** Fahrbefehle gehen an `/cmd_vel_unstamped` (Typ `Twist`), **nicht**
  an `/cmd_vel` (das erwartet `TwistStamped`). Prüfen: `ros2 topic list | grep cmd_vel`.
- **Namespace?** Vielleicht ist es `/tbXX/cmd_vel_unstamped`.
- Sendet überhaupt jemand? `ros2 topic echo /cmd_vel_unstamped` in zweitem Terminal.
- **teleop bewegt nichts?** teleop sendet auf `cmd_vel` – remappen:
  `--ros-args -r cmd_vel:=/cmd_vel_unstamped`.
- Create-3-Basis im Fehlerzustand? Kurz aus-/einschalten (mit Betreuung).
- Sicherheitsstopp aktiv (Roboter angehoben/gekippt)? Wieder absetzen.

## SLAM-Karte ist verschmiert / doppelte Wände

- Langsamer fahren, besonders bei Drehungen.
- Eine Schleife schließen (zum Start zurück) für Loop Closure.
- Prüfen, dass `/scan` mit stabiler Rate kommt: `ros2 topic hz /scan`.

## Nav2: Roboter fährt nicht los

- **Startpose gesetzt?** In RViz „2D Pose Estimate" passend zur echten Position.
- Laserscan-Punkte liegen nicht auf den Wänden → Pose neu setzen.
- Karte korrekt geladen? Pfad in `map:=...` prüfen (absoluter Pfad, `.yaml`).
- Nav2 wirklich aktiv? Konsole von `nav_bringup` auf Fehler prüfen.

## RViz zeigt nichts / „Global Status: Error"

- **Fixed Frame** auf `map` (Nav) bzw. `odom` setzen.
- Fehlende Displays (Map, LaserScan, RobotModel, TF) hinzufügen.
- TF-Baum prüfen: `ros2 run tf2_tools view_frames`.

## VS Code Remote-SSH verbindet nicht

- IP/Hostname korrekt? `ssh ubuntu@<IP>` zuerst im Terminal testen.
- Gleiches WLAN, Roboter gebootet.

---

### Allgemeine Diagnose-Reihenfolge

1. Stimmt das Netzwerk? (`ping`, gleiches WLAN)
2. Stimmt die Umgebung? (`env | grep ROS`)
3. Ist das Paket gebaut & gesourct?
4. Stimmt der Topic-Name (Namespace!)?
5. Logs lesen – die erste Fehlermeldung zählt.
