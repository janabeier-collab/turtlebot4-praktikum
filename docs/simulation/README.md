# Simulationspraktikum – TurtleBot 4 in Gazebo

Ein eigenständiger Praktikumszweig, der **ohne echten Roboter** auskommt. Alles
läuft in **Gazebo Harmonic** auf dem Laborrechner.

| Versuch | Thema | Anleitung |
|--------:|-------|-----------|
| **S0** | Setup: Simulation installieren und starten | [S0_setup.md](S0_setup.md) |
| **S1** | Fahren und ROS-2-Grundlagen in der Simulation | [S1_fahren.md](S1_fahren.md) |
| **S2** | SLAM: das Labyrinth kartieren | [S2_slam.md](S2_slam.md) |
| **S3** | Navigation mit Nav2 und eigene Routen | [S3_navigation.md](S3_navigation.md) |
| **S4** | Mehrere Roboter gleichzeitig (Namespaces) | [S4_mehrere_roboter.md](S4_mehrere_roboter.md) |

Dazu: [Unterschiede Simulation ↔ realer Roboter](unterschiede.md) — die Liste,
die ihr braucht, wenn ihr euren Code auf einen echten TurtleBot bringt.

---

## Warum ein zweiter Zweig?

Der Praktikumscode ist **derselbe**. `src/praktikum_py` läuft unverändert in der
Simulation und auf dem echten Roboter, weil der simulierte Create 3 dieselben
Topics und Actions anbietet — insbesondere `/cmd_vel_unstamped`, `/scan`,
`/odom`, `/battery_state`, `/dock_status` sowie `/dock` und `/undock`.

Was die Simulation **besser** kann:

- **Kein Zeitdruck, keine Akkus.** Ein Versuch lässt sich beliebig oft und exakt
  gleich wiederholen — gut für Vorbereitung, Fehlersuche und Nachholtermine.
- **Nichts geht kaputt.** Ein Fehler im Regler fährt hier gegen eine simulierte Wand.
- **Mehrere Roboter gleichzeitig** (Versuch S4). Am realen Aufbau kaum praktikabel,
  in der Simulation eine Zeile mehr.
- **Reproduzierbar.** Gleiche Welt, gleiche Startpose, gleiches Ergebnis.

Was die Simulation **nicht** kann: Reibung, Radschlupf, Sensorrauschen, Lichtverhältnisse,
WLAN-Aussetzer, verschmutzte Dock-Kontakte. Wer nur simuliert hat, ist am echten
Roboter überrascht — deshalb gibt es [unterschiede.md](unterschiede.md).

## Empfohlener Ablauf

- **Als Vorbereitung:** S0–S3 vor dem ersten Hardware-Termin. Die Studierenden
  kommen dann mit lauffähigem Code ins Labor und verbringen die knappe
  Robotikzeit nicht mit Tippfehlern.
- **Als eigenständiges Praktikum:** S0–S4 komplett, wenn keine Hardware frei ist
  (mehr Gruppen als Roboter, Ausfall, Nachholtermin, Homeoffice).
- **Als Fehlersuche:** Verhält sich der echte Roboter seltsam, zeigt derselbe
  Code in der Simulation, ob es am Programm oder an der Hardware liegt.

## Voraussetzungen

Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic und eine halbwegs brauchbare Grafik.
Die Installation steht in [S0_setup.md](S0_setup.md). Ein echter TurtleBot wird
**nicht** gebraucht — er darf für diese Versuche sogar ausgeschaltet bleiben.
