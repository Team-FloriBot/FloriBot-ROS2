cmake_minimum_required(VERSION 3.5)
project(base2gazebo)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate interfaces (message files)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Wheels.msg"
  DEPENDENCIES std_msgs
)

# Install the Python script (keine C++-Kompilierung nötig!)
install(PROGRAMS
  src/PublishWheelSpeed.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
