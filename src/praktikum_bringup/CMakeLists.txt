cmake_minimum_required(VERSION 3.8)
project(praktikum_bringup)

find_package(ament_cmake REQUIRED)

# Launch- und Config-Dateien installieren, damit sie per `ros2 launch` auffindbar sind:
install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
