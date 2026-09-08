# Simulation ↔ echter TurtleBot 4

> Die Liste, die ihr braucht, wenn ihr Code aus dem Simulationspraktikum auf
> einen echten Roboter bringt — oder umgekehrt.

---

## Was identisch ist

Das ist der Grund, warum sich der Aufwand lohnt: **euer Code muss nicht angepasst
werden.** Der simulierte Create 3 bietet dieselbe Schnittstelle wie die echte Basis.

| | Simulation | Realer Roboter |
|---|---|---|
| Fahrbefehl | `/cmd_vel_unstamped` (`Twist`) | `/cmd_vel_unstamped` (`Twist`) |
| Laserscan | `/scan` | `/scan` |
| Odometrie | `/odom` | `/odom` |
| Akku | `/battery_state` | `/battery_state` |
| Dockstatus | `/dock_status` | `/dock_status` |
| Actions | `/undock`, `/dock`, `/drive_distance`, `/rotate_angle` | dieselben |
| SLAM / Nav2 | `turtlebot4_navigation` | dasselbe Paket |
| RViz | `turtlebot4_viz` | dasselbe Paket |

Der simulierte Create 3 abonniert `/cmd_vel` als `TwistStamped` **und**
`/cmd_vel_unstamped` als `Twist` — genau wie die echte Basis über ihren
Republisher. Deshalb laufen `square_driver`, `battery_listener`, `goto_goal` und
`patrol` in beiden Welten unverändert.

---

## Was ihr umstellen müsst

| Thema | Simulation | Realer Roboter |
|---|---|---|
| **Umgebung** | `source tools/sim_env.sh` (ohne Discovery Server, `LOCALHOST`) | `source ~/.bashrc` (Domain-ID + Discovery Server + Super Client) |
| **Zeit** | `use_sim_time:=true` **überall** | `use_sim_time` bleibt `false` |
| **Start** | `turtlebot4_gz_bringup turtlebot4_gz.launch.py` | Roboter einschalten, `turtlebot4.service` läuft von selbst |
| **Trennung mehrerer Roboter** | Namespaces | eigene Domain-ID je Roboter |
| **Karte** | Karte der Gazebo-Welt | Karte des echten Labors |
| **Not-Aus** | Simulation pausieren | Roboter anheben |

> ⚠️ **Die häufigsten zwei Fehler beim Wechsel:**
> 1. In der Simulation `use_sim_time` vergessen → Nav2 steht, TF meckert über
>    Extrapolation.
> 2. Auf der Hardware `use_sim_time:=true` stehen lassen → der Roboter wartet auf
>    eine `/clock`, die niemand veröffentlicht, und tut gar nichts.

---

## Was die Simulation nicht abbildet

Hier wird es für die Interpretation eurer Messwerte wichtig:

- **Reibung und Radschlupf.** Auf Teppich, Fugen oder Kabeln driftet der echte
  Roboter deutlich stärker. Ein Quadrat, das in Gazebo sauber schließt, tut das
  in der Realität selten.
- **Sensorrauschen und Reflexionen.** Der simulierte LiDAR ist sauber. Der echte
  hat Probleme mit Glas, Spiegeln, dunklen Sockelleisten und Stuhlbeinen.
- **Beleuchtung.** Für die Kamera und die Dock-Erkennung real relevant, simuliert irrelevant.
- **Akku.** Der simulierte Ladezustand ist ein Modell. Ein echter Roboter wird
  gegen Ende langsamer und dockt schlechter.
- **Netzwerk.** WLAN-Aussetzer, Discovery-Server, halbe Topic-Listen — es gibt
  in der Simulation keine Entsprechung. Genau das ist im Labor die häufigste
  Fehlerquelle.
- **Rechenlast.** In der Simulation teilen sich Gazebo, Nav2 und RViz eine CPU.
  Läuft es zäh, ist das kein Fehler eures Codes.
- **Mechanik.** Verschmutzte Dock-Kontakte, klemmende Bumper, Haare in den
  Achsen — die häufigsten realen Ausfälle haben gar keinen Software-Anteil.

---

## Praktische Empfehlung

1. **Entwickeln und Debuggen in der Simulation.** Syntaxfehler, falsche
   Topic-Namen, kaputte Zustandsautomaten fallen dort in Sekunden auf.
2. **Parameter in der Simulation grob einstellen**, auf der Hardware nachziehen —
   besonders Geschwindigkeiten und Drehzeiten.
3. **Auf der Hardware bewusst langsamer anfangen.** Was in Gazebo mit 0,5 m/s
   funktioniert, gehört real erst mit 0,15 m/s ausprobiert.
4. **Bleibt ein Fehler unklar**, denselben Code in der Simulation laufen lassen.
   Läuft er dort sauber, liegt es an Hardware, Netzwerk oder Umgebung — nicht am
   Programm.
