# Versuch 0 – Setup: Netzwerk, SSH und Workspace

> **Lernziel:** Ihr verbindet euren Laborrechner mit dem TurtleBot 4, versteht das
> Netzwerk-Setup (Labor-WLAN + Discovery Server) und baut den ROS-2-Workspace.
> Am Ende seht ihr die Topics des Roboters auf eurem Rechner.

Plattform: **ROS 2 Jazzy**, **Ubuntu 24.04**, **TurtleBot 4 Standard**.
Ihr arbeitet **ohne `sudo`** – alles passiert in eurem Home-Verzeichnis.

---

## 0.1 Das Setup auf einen Blick

```
┌────────────────────┐        Labor-WLAN          ┌──────────────────────────┐
│  Laborrechner (PC) │  <─────────────────────>   │  TurtleBot 4             │
│  Ubuntu 24.04      │      (gleiches Netz)       │  Raspberry Pi 4 + Create3│
│  ROS 2 Jazzy       │                            │  ROS 2 Jazzy             │
│  → euer Code       │   ROS 2 DDS / Discovery    │  → Sensoren & Antrieb    │
└────────────────────┘        Server              └──────────────────────────┘
```

- **PC und Roboter sind im selben Labor-WLAN.** Nur dann finden sich die ROS-2-Knoten.
- Ihr **programmiert auf dem PC**. Auf dem Roboter müsst ihr im Normalfall nichts
  ändern – ihr schaltet euch nur per **SSH** drauf, wenn ihr etwas prüfen/konfigurieren wollt.
- Die Knoten finden sich über einen **Discovery Server**, der auf dem TurtleBot läuft.

---

## 0.2 Verbindung herstellen (Rechner ist vorkonfiguriert)

> **Wichtig:** Die Laborrechner sind **bereits fertig eingerichtet**. Die richtige
> Domain-ID und die Discovery-Server-Adresse **eures** Roboters stehen schon in der
> `~/.bashrc`. Ihr müsst **nichts** von Hand eintragen.

Verbindung herstellen und prüfen:

```bash
source ~/.bashrc        # lädt die vorkonfigurierte Roboter-Verbindung
ros2 topic list         # sollte die Topics des Roboters zeigen
```

Seht ihr Topics wie `/battery_state`, `/scan`, `/odom`, `/cmd_vel`? **Dann steht die Verbindung.**

> In frisch geöffneten Terminals wird `~/.bashrc` meist automatisch geladen –
> das `source` ist nur nötig, wenn ihr es explizit neu laden wollt.

<details>
<summary><b>Was in der vorkonfigurierten <code>~/.bashrc</code> steht (nur zur Info)</b></summary>

Ihr braucht das nicht anzufassen – zum Verständnis, was die Verbindung ausmacht:

```bash
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_DOMAIN_ID=10                         # Domain-ID eures Roboters (Aufkleber)
export ROS_DISCOVERY_SERVER="10.0.0.42:11811"   # IP eures Roboters : Port
export ROS_SUPER_CLIENT=true                    # damit ALLE Topics sichtbar sind
```

Die **Domain-ID** trennt eure Roboter voneinander (jeder Roboter eine eigene) – so
kommen sich die Teams im selben WLAN nicht in die Quere. Der **Discovery Server**
zeigt auf genau euren Roboter. `ROS_SUPER_CLIENT` sorgt dafür, dass ihr den *ganzen*
Topic-Graphen seht und nicht nur einen Teil.
</details>

### Topics fehlen oder Liste bleibt leer?

```bash
ros2 topic list      # ruhig ein zweites Mal aufrufen – der Daemon braucht kurz
```

Wenn dann immer noch etwas fehlt, der Reihe nach:

1. **Roboter fertig gebootet?** Direkt nach dem Einschalten ist die Create-3-Basis
   noch nicht bereit → `/odom`, `/cmd_vel`, `/imu` fehlen. Kurz warten, oder den
   **Roboter aus- und wieder einschalten** und ~1–2 Min. hochfahren lassen.
   *(Genau das war im Praktikum schon der Fix, wenn Topics fehlten.)*
2. **Daemon zurücksetzen:** `ros2 daemon stop && ros2 daemon start`, dann erneut listen.
3. **Umgebung geladen?** `source ~/.bashrc` in diesem Terminal, oder neues Terminal öffnen.
4. **Roboter erreichbar?** `ping <ROBOTER-IP>`.

Mehr dazu → [troubleshooting.md](troubleshooting.md).

---

## 0.3 Per SSH auf den Roboter (optional)

Zum Programmieren bleibt ihr auf dem PC. Ihr schaltet euch nur per **SSH** auf den
Roboter, wenn ihr etwas **prüfen oder konfigurieren** wollt:

```bash
ssh ubuntu@<ROBOTER-IP>       # Passwort erfragt ihr bei der Betreuung
```

Auf dem Roboter z.B.:

```bash
turtlebot4-setup      # interaktives Konfig-Menü (Netzwerk, Discovery Server, ...)
ros2 topic list       # Topics direkt auf dem Roboter
exit                  # SSH-Sitzung verlassen
```

> ⚠️ **Ändert auf dem Roboter nichts ohne Rücksprache.** Das Setup ist für alle
> Gruppen gleich konfiguriert.

---

## 0.4 Roboter-Beschriftung verstehen (Referenz / Fehlersuche)

> Nur zur Info – im Normalfall müsst ihr hier **nichts** tun, die Verbindung ist
> ja bereits eingerichtet (0.2). Nützlich, falls doch mal die IP gesucht werden muss.

Jeder TurtleBot ist beschriftet, z.B.:

```
Domain ID: 10
E4 5F 01 7D 3F 36
```

- **Domain ID** (`10`) → die `ROS_DOMAIN_ID`. Trennt eure Roboter voneinander; steht
  bereits in der `~/.bashrc`.
- Die **Hex-Folge** ist die **MAC-Adresse** der WLAN-Karte. Kommt *nicht* in ROS –
  sie dient nur dazu, die **IP** des Roboters zu finden, falls nötig:

```bash
ip neigh | grep -i "e4:5f:01:7d:3f:36"    # → zeigt die IP des Roboters
```

Alternativ: IP in der DHCP-Tabelle des Labor-Routers nachschlagen (MAC → IP).

---

## 0.5 Workspace klonen und bauen

```bash
cd ~
git clone <REPO-URL> turtlebot4-praktikum
cd turtlebot4-praktikum

# Abhängigkeiten prüfen (nur Anzeige, kein sudo nötig wenn alles installiert ist):
# rosdep check --from-paths src --ignore-src   # optional

# Bauen:
colcon build --symlink-install
source install/setup.bash
```

`--symlink-install` bedeutet: Änderungen an Python-Dateien wirken sofort, ohne
neu zu bauen (nur bei neuen Dateien / `entry_points` erneut `colcon build`).

Tipp für jedes neue Terminal – einmal definieren, immer nutzen:

```bash
echo 'alias src_ws="source /opt/ros/jazzy/setup.bash && source ~/turtlebot4-praktikum/install/setup.bash"' >> ~/.bashrc
source ~/.bashrc
# danach reicht in jedem Terminal:  src_ws
```

Erstes eigenes Node testen:

```bash
src_ws
ros2 run praktikum_py hello_node
# Erwartung:  [hello_node]: Hallo Welt! (Tick 1) ...
```

---

## 0.6 VS Code (Remote-SSH, optional aber empfohlen)

Ihr könnt komfortabel mit **VS Code** arbeiten und euch direkt auf den Roboter
oder einen Remote-Rechner schalten:

1. Erweiterung **„Remote – SSH"** installieren.
2. Befehlspalette (`F1`) → *Remote-SSH: Connect to Host* → `ubuntu@<ROBOTER-IP>`.
3. Ordner öffnen, integriertes Terminal nutzen.

Für die meisten Aufgaben genügt aber VS Code lokal auf dem PC + Terminal.
Empfohlene Erweiterungen: **Python**, **ROS** (`ms-iot.vscode-ros`), **XML**.

---

## 0.7 Checkliste vor Versuch 1

- [ ] Roboter eingeschaltet und ~1–2 Min. hochgefahren (Create-3-Basis bereit)
- [ ] `source ~/.bashrc` ausgeführt
- [ ] `ros2 topic list` zeigt die Topics des Roboters (`/scan`, `/odom`, `/cmd_vel`, …)
- [ ] `colcon build` läuft fehlerfrei
- [ ] `ros2 run praktikum_py hello_node` gibt Ticks aus

Probleme? → [troubleshooting.md](troubleshooting.md)

---

*Quellen: TurtleBot 4 User Manual (Setup / Networking / Discovery Server), ROS 2 Jazzy Doku – siehe Linksammlung in [cheatsheet.md](cheatsheet.md).*
