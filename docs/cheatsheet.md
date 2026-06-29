# Cheatsheet – ROS 2 Jazzy & TurtleBot 4

Schnellreferenz für das Praktikum. In jedem neuen Terminal zuerst: **`src_ws`**
(= `source /opt/ros/jazzy/setup.bash && source ~/turtlebot4-praktikum/install/setup.bash`).

> **Namespace beachten:** Hat euer Roboter einen (z.B. `tb01`), heißen Topics
> `/tb01/cmd_vel` statt `/cmd_vel`. Immer `ros2 topic list` prüfen.

---

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
ros2 interface show <typ>       rqt_graph
```

## Topics / Nodes / Params

```bash
ros2 run <pkg> <executable>
ros2 run <pkg> <exe> --ros-args -p <name>:=<wert>     # Parameter setzen
ros2 launch <pkg> <file.launch.py> <arg>:=<wert>
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}}"
ros2 param list | get <node> <param> | set <node> <param> <wert>
```

## TurtleBot 4 – wichtige Topics

| Topic | Typ | Bedeutung |
|-------|-----|-----------|
| `/cmd_vel` | `geometry_msgs/Twist` | Fahrbefehl (linear.x, angular.z) |
| `/scan` | `sensor_msgs/LaserScan` | 2D-LiDAR |
| `/odom` | `nav_msgs/Odometry` | Odometrie / geschätzte Pose |
| `/battery_state` | `sensor_msgs/BatteryState` | Akkustand |
| `/map` | `nav_msgs/OccupancyGrid` | Karte (während SLAM/Nav) |

## SLAM (Versuch 2)

```bash
ros2 launch turtlebot4_navigation slam.launch.py [namespace:=/tbXX]
ros2 launch turtlebot4_viz view_robot.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 run nav2_map_server map_saver_cli -f labor_map
```

## Navigation (Versuch 3)

```bash
ros2 launch turtlebot4_navigation nav_bringup.launch.py \
    slam:=off localization:=true map:=$HOME/turtlebot4-praktikum/maps/labor_map.yaml
ros2 launch turtlebot4_viz view_robot.launch.py
# In RViz: "2D Pose Estimate" → dann "Nav2 Goal"
```

## SSH zum Roboter

```bash
ssh ubuntu@<ROBOTER-IP>
turtlebot4-setup        # Konfig-Menü auf dem Roboter (nur mit Rücksprache ändern!)
exit
```

---

## Offizielle Doku (Links)

- TurtleBot 4 User Manual: https://turtlebot.github.io/turtlebot4-user-manual/
  - Setup / Basic: https://turtlebot.github.io/turtlebot4-user-manual/setup/basic.html
  - Networking: https://turtlebot.github.io/turtlebot4-user-manual/setup/networking.html
  - Discovery Server: https://turtlebot.github.io/turtlebot4-user-manual/setup/discovery_server.html
  - Navigation: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/navigation.html
  - TurtleBot4 Navigator: https://turtlebot.github.io/turtlebot4-user-manual/tutorials/turtlebot4_navigator.html
- ROS 2 Jazzy: https://docs.ros.org/en/jazzy/
- Nav2: https://docs.nav2.org/
- SLAM Toolbox: https://github.com/SteveMacenski/slam_toolbox
