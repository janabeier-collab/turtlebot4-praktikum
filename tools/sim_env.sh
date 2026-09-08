# sim_env.sh – Umgebung fuer die Gazebo-Simulation.
#
# Muss GESOURCT werden, nicht ausgefuehrt:
#     source ~/turtlebot4-praktikum/tools/sim_env.sh
#
# Warum: auf den Laborrechnern zeigt die ~/.bashrc ueber ROS_DISCOVERY_SERVER
# auf einen echten TurtleBot. Steht diese Variable, melden sich auch die
# Simulationsknoten dort an und finden sich untereinander nicht, wenn der
# Roboter aus ist. Dieses Skript trennt die Simulation davon.

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  echo "Bitte sourcen statt ausfuehren:  source tools/sim_env.sh" >&2
  exit 1
fi

# 1. Verbindung zum echten Roboter aus der Umgebung nehmen
unset ROS_DISCOVERY_SERVER
unset ROS_SUPER_CLIENT
unset FASTRTPS_DEFAULT_PROFILES_FILE

# 2. Simulation auf diesen Rechner begrenzen: kein Uebersprechen zwischen den
#    Laborplaetzen, keine Domain-ID-Absprachen noetig.
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# 3. ROS 2 und den Praktikums-Workspace laden
source /opt/ros/jazzy/setup.bash
_ws="${TB4_PRAKTIKUM_WS:-$HOME/turtlebot4-praktikum}"
if [ -f "$_ws/install/setup.bash" ]; then
  source "$_ws/install/setup.bash"
else
  echo "Hinweis: $_ws/install/setup.bash fehlt – Workspace noch nicht gebaut."
  echo "         cd $_ws && colcon build --symlink-install"
fi
unset _ws

# 4. Alten Daemon wegwerfen, damit er nicht die alte Umgebung weiterbenutzt
ros2 daemon stop >/dev/null 2>&1

echo "Simulationsumgebung aktiv:"
echo "  ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}  ROS_AUTOMATIC_DISCOVERY_RANGE=$ROS_AUTOMATIC_DISCOVERY_RANGE"
echo "  ROS_DISCOVERY_SERVER ist nicht gesetzt (Verbindung zum echten Roboter getrennt)."
echo "  Start:  ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=maze rviz:=true"
