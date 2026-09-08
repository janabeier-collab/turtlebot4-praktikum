# Cheatsheet – ROS 2 Jazzy & TurtleBot 4

Schnellreferenz für das Praktikum. In jedem neuen Terminal zuerst: **`src_ws`**
(= `source /opt/ros/jazzy/setup.bash && source ~/turtlebot4-praktikum/install/setup.bash`).

> **Namespace beachten:** Hat euer Roboter einen (z.B. `tb01`), heißen Topics
> `/tb01/cmd_vel_unstamped` statt `/cmd_vel_unstamped`, und alle Launch-Files
> brauchen `namespace:=/tb01`. Immer `ros2 topic list` prüfen.

---

## Verbindung zum Roboter (vom Aufkleber)

```bash
source ~/.bashrc
ping <ip>                                     # zeigt ob Roboter erreichbar
# IP aus MAC-Adresse ermitteln:
ip neigh | grep -i "e4:5f:01:7d:3f:36"        # → zeigt die IP des Roboters
env | grep ROS                                # Domain-ID, Discovery Server, RMW prüfen
```

## Umgebung & Workspace

```bash
source /opt/ros/jazzy/setup.bash          # ROS 2 laden
colcon build --symlink-install            # Workspace bauen (im Repo-Root)
source install/setup.bash                 # gebautes Paket verfügbar machen
colcon build --packages-select praktikum_py   # nur ein Paket bauen
```

## Graph erkunden

```bash
ros2 node list                  ros2 node info <node>
ros2 topic list                 ros2 topic info <topic>
ros2 topic echo <topic>         ros2 topic hz <topic>
ros2 action list                ros2 interface show <typ>
rqt_graph                       ros2 run tf2_tools view_frames
```

## Topics / Nodes / Params

```bash
ros2 run <pkg> <executable>
ros2 run <pkg> <exe> --ros-args -p <name>:=<wert>     # Parameter setzen
ros2 launch <pkg> <file.launch.py> <arg>:=<wert>
ros2 topic pub --once /cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: 0.1}}"
ros2 param list | get <node> <param> | set <node> <param> <wert>
```

## TurtleBot 4 – wichtige Topics

| Topic | Typ | Bedeutung |
|-------|-----|-----------|
| `/cmd_vel_unstamped` | `geometry_msgs/Twist` | Fahrbefehl für **euren** Code (linear.x, angular.z) |
| `/cmd_vel` | `geometry_msgs/TwistStamped` | gestempelte Variante – nutzt Nav2 intern |
| `/scan` | `sensor_msgs/LaserScan` | 2D-LiDAR |
| `/odom` | `nav_msgs/Odometry` | Odometrie / geschätzte Pose |
| `/battery_state` | `sensor_msgs/BatteryState` | Akkustand |
| `/dock_status` | `irobot_create_msgs/DockStatus` | steht der Roboter auf der Ladestation? |
| `/map` | `nav_msgs/OccupancyGrid` | Karte (während SLAM/Nav) |
| `/diagnostics` | `diagnostic_msgs/DiagnosticArray` | Zustand von Sensorik & Basis |

## Fahren & Docken

```bash
ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"
ros2 action send_goal /dock   irobot_create_msgs/action/Dock "{}"
ros2 action send_goal /drive_distance irobot_create_msgs/action/DriveDistance "{distance: 0.5}"
ros2 action send_goal /rotate_angle   irobot_create_msgs/action/RotateAngle "{angle: 1.5708}"
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel_unstamped
```

## SLAM (Versuch 2)

```bash
ros2 launch turtlebot4_navigation slam.launch.py [namespace:=/tbXX] [sync:=false]
ros2 launch turtlebot4_viz view_navigation.launch.py
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "name: {data: '/home/<benutzer>/turtlebot4-praktikum/maps/labor_map'}"   # absoluter Pfad!
# Alternative:
ros2 run nav2_map_server map_saver_cli -f labor_map --ros-args -p map_subscribe_transient_local:=true
```

## Navigation (Versuch 3)

```bash
ros2 launch turtlebot4_navigation localization.launch.py map:=$HOME/turtlebot4-praktikum/maps/labor_map.yaml
ros2 launch turtlebot4_navigation nav2.launch.py
ros2 launch turtlebot4_viz view_navigation.launch.py
# In RViz: "2D Pose Estimate" → dann "Nav2 Goal"
```

> `nav_bringup.launch.py` (mit `slam:=off localization:=true`) gibt es in Jazzy
> **nicht mehr** – es sind die zwei Launch-Files oben.
> Und für Karten/Navigation immer `view_navigation.launch.py` statt
> `view_robot.launch.py` – nur ersteres hat Map-, Costmap- und Nav2-Anzeigen.

## Diagnose / Zustand des Roboters

```bash
ros2 launch turtlebot4_viz view_diagnostics.launch.py   # grafische Diagnose (auf dem PC)
ros2 topic echo /diagnostics_agg                        # aggregierte Meldungen
ros2 topic hz /scan                                     # LiDAR laeuft? (~10 Hz)
ros2 topic echo /battery_state --once                   # Akkustand
```

Das Create-3-Web-Interface (Firmware, WLAN, Logs) erreicht ihr im Browser unter
`http://<ROBOTER-IP>:8080` – **nur mit Rücksprache** etwas ändern.

---

## Offizielle Doku (Links)

- TurtleBot 4 User Manual: https://turtlebot.github.io/turtlebot4-user-manual/
  - Setup / Basic: https://turtlebot.github.io/turtlebot4-user-manual/setup/basic.html
  - Networking: https://turtlebot.github.io/turtlebot4-user-manual/setup/networking.html
  - Discovery Server: https://turtlebot.github.io/turtlebot4-user-manual/setup/discovery_server.html
  - Driving: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/driving.html
  - Generating a map: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/generate_map.html
  - Navigation: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/navigation.html
  - TurtleBot4 Navigator: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/turtlebot4_navigator.html
  - Multiple robots: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/multiple_robots.html
  - SD-Karten-Backup: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/create_sd_image.html
- ROS 2 Jazzy: https://docs.ros.org/en/jazzy/
- Nav2: https://docs.nav2.org/
- SLAM Toolbox: https://github.com/SteveMacenski/slam_toolbox
- Create 3 Doku (Actions, Web-Interface): https://iroboteducation.github.io/create3_docs/
