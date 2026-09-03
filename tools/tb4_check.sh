#!/usr/bin/env bash
# tb4_check.sh – Schnelltest eines TurtleBot 4 vom Laborrechner aus.
#
# Prüft in dieser Reihenfolge:
#   A) Laborrechner (ROS-Umgebung, benötigte Pakete)
#   B) Netzwerk (Erreichbarkeit des Roboters)
#   C) ROS-Graph (Topics, Raten, Akku, Dockstatus, Diagnostics)
#   D) optional: Antriebstest (undock -> fahren -> drehen -> dock)
#
# Aufruf:
#   ./tools/tb4_check.sh                 # nur prüfen, Roboter bewegt sich NICHT
#   ./tools/tb4_check.sh --drive         # zusätzlich Antriebstest (freie Fläche!)
#   ./tools/tb4_check.sh --ns /tb01      # mit Namespace
#   ./tools/tb4_check.sh --robot tb03 --drive > berichte/tb03.txt
#
# Rückgabewert: 0 = alles bestanden, 1 = mindestens ein Test fehlgeschlagen.

set -uo pipefail

NS=""
DRIVE=0
ROBOT_LABEL="unbenannt"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --drive) DRIVE=1; shift ;;
    --ns)    NS="${2%/}"; shift 2 ;;
    --robot) ROBOT_LABEL="$2"; shift 2 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "Unbekannte Option: $1"; exit 2 ;;
  esac
done

PASS=0; FAIL=0; WARN=0
ok()   { printf '  [ OK ]   %s\n' "$*"; PASS=$((PASS+1)); }
bad()  { printf '  [FEHLT]  %s\n' "$*"; FAIL=$((FAIL+1)); }
warn() { printf '  [ ?  ]   %s\n' "$*"; WARN=$((WARN+1)); }
head1() { printf '\n== %s ==\n' "$*"; }

echo "TurtleBot-4-Check – Roboter: ${ROBOT_LABEL}${NS:+ (Namespace ${NS})}"
echo "Datum: $(date '+%Y-%m-%d %H:%M')   Rechner: $(hostname)   Nutzer: $USER"

# ---------------------------------------------------------------- A) Rechner
head1 "A) Laborrechner"

if command -v ros2 >/dev/null 2>&1; then
  ok "ros2 gefunden (ROS_DISTRO=${ROS_DISTRO:-unbekannt})"
else
  bad "ros2 nicht im PATH – 'source /opt/ros/jazzy/setup.bash' fehlt"
  echo; echo "Abbruch: ohne ROS 2 keine weiteren Tests."; exit 1
fi

[[ -n "${ROS_DOMAIN_ID:-}" ]]        && ok "ROS_DOMAIN_ID=$ROS_DOMAIN_ID"        || bad "ROS_DOMAIN_ID nicht gesetzt"
[[ -n "${ROS_DISCOVERY_SERVER:-}" ]] && ok "ROS_DISCOVERY_SERVER=$ROS_DISCOVERY_SERVER" || warn "ROS_DISCOVERY_SERVER nicht gesetzt (nur ok, wenn ohne Discovery Server gearbeitet wird)"
[[ "${RMW_IMPLEMENTATION:-}" == "rmw_fastrtps_cpp" ]] && ok "RMW_IMPLEMENTATION=rmw_fastrtps_cpp" || warn "RMW_IMPLEMENTATION=${RMW_IMPLEMENTATION:-<leer>} (erwartet: rmw_fastrtps_cpp)"
case "$(printf '%s' "${ROS_SUPER_CLIENT:-}" | tr 'A-Z' 'a-z')" in
  true|1) ok "ROS_SUPER_CLIENT=${ROS_SUPER_CLIENT}" ;;
  *) warn "ROS_SUPER_CLIENT=${ROS_SUPER_CLIENT:-<leer>} – ohne Super Client ist der Topic-Graph unvollstaendig.
           /etc/turtlebot4_discovery/setup.bash setzt den Wert nur in interaktiven Terminals
           ([ -t 0 ]); in Skripten und 'ssh host befehl' steht er auf False. Fuer diesen Lauf:
           export ROS_SUPER_CLIENT=True" ;;
esac

# Fuer die folgenden Abfragen selbst erzwingen, sonst ist der Topic-Graph unvollstaendig:
export ROS_SUPER_CLIENT=True

PKGS_OK=1
for p in turtlebot4_navigation turtlebot4_viz turtlebot4_msgs nav2_bringup nav2_map_server slam_toolbox teleop_twist_keyboard irobot_create_msgs nav2_simple_commander; do
  if ros2 pkg prefix "$p" >/dev/null 2>&1; then
    ok "Paket installiert: $p"
  else
    bad "Paket fehlt: $p   (sudo apt install ros-${ROS_DISTRO:-jazzy}-$(echo "$p" | tr '_' '-'))"
    PKGS_OK=0
  fi
done

if command -v rviz2 >/dev/null 2>&1; then ok "rviz2 vorhanden"; else bad "rviz2 fehlt"; fi
if command -v colcon >/dev/null 2>&1; then ok "colcon vorhanden"; else bad "colcon fehlt"; fi

# --------------------------------------------------------------- B) Netzwerk
head1 "B) Netzwerk"

# ROS_DISCOVERY_SERVER kann mehrere Server enthalten ("ip:port;ip:port") und mit
# Semikolons beginnen, wenn Server-ID 0 uebersprungen wird -> erste IP herausziehen.
ROBOT_IP="$(printf '%s' "${ROS_DISCOVERY_SERVER:-}" | grep -oE '[0-9]{1,3}(\.[0-9]{1,3}){3}' | head -1)"
if [[ -n "$ROBOT_IP" ]]; then
  if ping -c 2 -W 2 "$ROBOT_IP" >/dev/null 2>&1; then
    ok "Roboter erreichbar: ping $ROBOT_IP"
  else
    bad "Roboter NICHT erreichbar: ping $ROBOT_IP  (WLAN? eingeschaltet? IP geändert?)"
  fi
  if command -v nc >/dev/null 2>&1; then
    nc -z -w2 "$ROBOT_IP" 22 >/dev/null 2>&1 && ok "SSH-Port 22 offen" || warn "SSH-Port 22 nicht erreichbar"
  fi
else
  warn "Keine Roboter-IP aus ROS_DISCOVERY_SERVER ableitbar – Netzwerktest übersprungen"
fi

# -------------------------------------------------------------- C) ROS-Graph
head1 "C) ROS-Graph"

ros2 daemon stop >/dev/null 2>&1; ros2 daemon start >/dev/null 2>&1
TOPICS="$(timeout 15 ros2 topic list 2>/dev/null)"
if [[ -z "$TOPICS" ]]; then
  bad "'ros2 topic list' liefert nichts – Verbindung zum Roboter steht nicht"
else
  ok "$(echo "$TOPICS" | wc -l) Topics sichtbar"
fi

for t in scan odom cmd_vel_unstamped battery_state dock_status imu; do
  if echo "$TOPICS" | grep -qx "${NS}/${t}"; then ok "Topic vorhanden: ${NS}/${t}"; else bad "Topic fehlt: ${NS}/${t}"; fi
done

rate_of() {  # $1 = topic, $2 = Mindestrate
  local r
  r="$(timeout 8 ros2 topic hz "$1" 2>/dev/null | grep -m1 -oE 'average rate: [0-9.]+' | grep -oE '[0-9.]+')"
  if [[ -z "$r" ]]; then bad "keine Daten auf $1"; return; fi
  if awk "BEGIN{exit !($r >= $2)}"; then ok "$1 läuft mit ${r} Hz (>= $2)"; else warn "$1 nur ${r} Hz (erwartet >= $2)"; fi
}
rate_of "${NS}/scan" 5
rate_of "${NS}/odom" 10

BATT="$(timeout 10 ros2 topic echo "${NS}/battery_state" --once 2>/dev/null | grep -m1 'percentage:' | awk '{print $2}')"
if [[ -n "$BATT" ]]; then
  PCT="$(awk "BEGIN{printf \"%.0f\", $BATT*100}")"
  if [[ "$PCT" -ge 30 ]]; then ok "Akku: ${PCT}%"; else warn "Akku nur ${PCT}% – vor dem Fahrtest laden"; fi
else
  bad "Akkustand nicht lesbar (${NS}/battery_state)"
fi

DOCKED="$(timeout 10 ros2 topic echo "${NS}/dock_status" --once 2>/dev/null | grep -m1 'is_docked:' | awk '{print $2}')"
case "$DOCKED" in
  true)  ok "Roboter steht auf der Ladestation" ;;
  false) warn "Roboter steht NICHT auf der Ladestation" ;;
  *)     bad "Dockstatus nicht lesbar (${NS}/dock_status)" ;;
esac

DIAG="$(timeout 12 ros2 topic echo "${NS}/diagnostics_agg" --once 2>/dev/null)"
if [[ -z "$DIAG" ]]; then
  warn "keine Diagnostics empfangen (${NS}/diagnostics_agg)"
elif echo "$DIAG" | grep -qE "level: .{0,3}(x02|x03)|level: [23]$"; then
  bad "Diagnostics meldet ERROR/STALE – Details: ros2 launch turtlebot4_viz view_diagnostics.launch.py"
else
  ok "Diagnostics ohne ERROR"
fi

# ------------------------------------------------------------- D) Antriebstest
if [[ "$DRIVE" -eq 1 ]]; then
  head1 "D) Antriebstest (Roboter bewegt sich!)"
  echo "  Freie Fläche? Niemand im Fahrweg? Weiter mit ENTER, Abbruch mit Strg+C."
  read -r _

  send() {  # $1 = action, $2 = typ, $3 = goal
    if timeout 90 ros2 action send_goal "${NS}/$1" "$2" "$3" 2>&1 | grep -q "Goal finished with status: SUCCEEDED"; then
      ok "$1 erfolgreich"
    else
      bad "$1 fehlgeschlagen"
    fi
  }
  send undock         irobot_create_msgs/action/Undock        "{}"
  send drive_distance irobot_create_msgs/action/DriveDistance "{distance: 0.5, max_translation_speed: 0.15}"
  send rotate_angle   irobot_create_msgs/action/RotateAngle   "{angle: 3.1416, max_rotation_speed: 0.5}"
  send drive_distance irobot_create_msgs/action/DriveDistance "{distance: 0.5, max_translation_speed: 0.15}"
  send rotate_angle   irobot_create_msgs/action/RotateAngle   "{angle: 3.1416, max_rotation_speed: 0.5}"
  send dock           irobot_create_msgs/action/Dock          "{}"
else
  head1 "D) Antriebstest"
  echo "  übersprungen (mit --drive aktivieren)"
fi

# ------------------------------------------------------------------ Ergebnis
head1 "Ergebnis ${ROBOT_LABEL}"
printf '  bestanden: %d   fehlgeschlagen: %d   zu prüfen: %d\n' "$PASS" "$FAIL" "$WARN"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  => Roboter/Platz einsatzbereit."; exit 0
else
  echo "  => NICHT einsatzbereit, siehe [FEHLT]-Zeilen und docs/troubleshooting.md"; exit 1
fi
