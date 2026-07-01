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

## 0.2 Roboter identifizieren

Jeder TurtleBot im Labor ist **beschriftet**. Typischerweise findet ihr auf dem
Aufkleber zwei Angaben, z.B.:

```
Domain ID: 10
E4 5F 01 7D 3F 36
```

- **Domain ID** (`10`) → die `ROS_DOMAIN_ID`. Kommt direkt in die ROS-Konfiguration
  (Abschnitt 0.4). PC und Roboter **müssen denselben Wert** haben.
- Die **Hex-Folge** (`E4 5F 01 7D 3F 36`) ist die **MAC-Adresse** der WLAN-Karte
  des Roboters. Sie kommt **nicht** in die ROS-Konfiguration – ihr braucht sie nur,
  um die aktuelle **IP-Adresse** des Roboters zu ermitteln (Abschnitt 0.2.1).

Tragt eure Werte hier ein (für euer Protokoll):

| Feld | Beispiel | Euer Wert |
|------|----------|-----------|
| Domain ID (`ROS_DOMAIN_ID`) | `10` | `__________` |
| MAC-Adresse (vom Aufkleber) | `e4:5f:01:7d:3f:36` | `__________` |
| IP-Adresse des Roboters (ermittelt) | `10.0.0.42` | `__________` |
| Discovery-Server-IP : Port | `10.0.0.42 : 11811` | `__________ : 11811` |
| TurtleBot-Name / Namespace | `tb01` | `__________` |

> **Namespace:** Wenn euer Roboter einen Namespace hat (z.B. `/tb01`), heißen die
> Topics `/tb01/cmd_vel` statt `/cmd_vel`. Prüft das immer mit `ros2 topic list`.

### 0.2.1 IP-Adresse aus der MAC ermitteln

ROS kennt keine MAC-Adressen – ihr braucht die **IP** des Roboters für SSH und für
den Discovery Server. So findet ihr sie im Labor-WLAN (MAC klein, mit Doppelpunkten:
`e4:5f:01:7d:3f:36`):

```bash
# Variante A: Netz anpingen, dann Nachbar-Tabelle durchsuchen
ping -c1 -b 10.0.0.255 2>/dev/null          # Broadcast eures Subnetzes (ggf. anpassen)
ip neigh | grep -i "e4:5f:01:7d:3f:36"
# → z.B.:  10.0.0.42 dev wlan0 lladdr e4:5f:01:7d:3f:36 REACHABLE

# Variante B: Subnetz scannen
sudo nmap -sn 10.0.0.0/24
arp -a | grep -i "e4:5f:01"
```

Alternativ: IP in der **DHCP-Tabelle des Labor-Routers** nachschlagen (MAC → IP) oder,
falls konfiguriert, per Hostname `ping <name>.local`. Was bei euch gilt, sagt die Betreuung.

> 💡 **Tipp für die Betreuung:** Eine **feste DHCP-Reservierung** auf die MAC vergeben,
> dann hat der Roboter immer dieselbe IP und die Studierenden müssen nicht jedes Mal suchen.

---

## 0.3 Per SSH auf den TurtleBot

```bash
# Standard-Login (Passwort erfragt ihr bei der Betreuung):
ssh ubuntu@<ROBOTER-IP>
```

Auf dem Roboter könnt ihr z.B. den Status prüfen:

```bash
turtlebot4-setup      # interaktives Menü (Discovery Server, Netzwerk, ...)
ros2 topic list       # zeigt die Topics direkt auf dem Roboter
exit                  # SSH-Sitzung verlassen
```

> ⚠️ **Ändert auf dem Roboter nichts ohne Rücksprache.** Das Setup ist für alle
> Gruppen gleich konfiguriert. Zum Programmieren bleibt ihr auf dem PC.

---

## 0.4 Discovery Server auf dem PC konfigurieren

Damit euer PC die Topics des Roboters sieht, müssen drei Dinge stimmen:

1. **gleiche DDS-Implementierung** (`rmw_fastrtps_cpp`),
2. **Adresse des Discovery Servers** (`ROS_DISCOVERY_SERVER`) – die IP aus 0.2.1,
3. **gleiche `ROS_DOMAIN_ID`** wie der Roboter – **der Wert vom Aufkleber** (z.B. `10`).

Tragt das ans Ende eurer `~/.bashrc` ein (einmalig, dann `source ~/.bashrc`).
Ersetzt `10` und die IP durch **eure** Werte aus der Tabelle in 0.2:

```bash
# --- ROS 2 Praktikum: Verbindung zum TurtleBot 4 ---
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_DOMAIN_ID=10                          # = "Domain ID" vom Aufkleber
export ROS_DISCOVERY_SERVER="10.0.0.42:11811"    # = ermittelte Roboter-IP : 11811
# ---------------------------------------------------
```

> ⚠️ **Häufigster Fehler:** Domain-ID stimmt nicht mit dem Aufkleber überein →
> `ros2 topic list` bleibt leer. Prüfen mit `echo $ROS_DOMAIN_ID`.

> Manche Labore nutzen statt des Discovery Servers **Simple Discovery** (reines
> Multicast im WLAN). Dann entfällt `ROS_DISCOVERY_SERVER`, und es genügen
> `RMW_IMPLEMENTATION` + identische `ROS_DOMAIN_ID`. Was bei euch gilt, sagt die Betreuung.

Verbindung testen:

```bash
source ~/.bashrc
ros2 daemon stop && ros2 daemon start   # Cache zurücksetzen
ros2 topic list                         # Topics des Roboters müssen erscheinen
ros2 topic echo /battery_state          # (ggf. mit Namespace) → Live-Daten
```

Seht ihr Topics wie `/battery_state`, `/scan`, `/odom`, `/cmd_vel`? **Dann steht die Verbindung.**

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

- [ ] PC und Roboter im selben Labor-WLAN
- [ ] Domain-ID, MAC und ermittelte IP in der Tabelle (0.2) notiert
- [ ] `echo $ROS_DOMAIN_ID` zeigt den Wert vom Aufkleber (z.B. `10`)
- [ ] `ros2 topic list` zeigt die Topics des Roboters
- [ ] `colcon build` läuft fehlerfrei
- [ ] `ros2 run praktikum_py hello_node` gibt Ticks aus

Probleme? → [troubleshooting.md](troubleshooting.md)

---

*Quellen: TurtleBot 4 User Manual (Setup / Networking / Discovery Server), ROS 2 Jazzy Doku – siehe Linksammlung in [cheatsheet.md](cheatsheet.md).*
