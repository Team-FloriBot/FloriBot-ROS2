cmake_minimum_required(VERSION 3.5)
project(visu)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

# Install directories
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# Install the Python executable
install(PROGRAMS
  src/rviz_visu.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_export_dependencies(
  rclpy
  geometry_msgs
  visualization_msgs
  #ros2_control
)
ament_package()
