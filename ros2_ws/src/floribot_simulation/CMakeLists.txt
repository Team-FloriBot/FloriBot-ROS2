cmake_minimum_required(VERSION 3.5)
project(floribot_simulation)

# Set standard for C++
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  set(CMAKE_CXX_EXTENSIONS OFF)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(control_msgs REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
#find_package(ros2_control REQUIRED)
find_package(ign_ros2_control REQUIRED)
foreach(Dependency IN ITEMS ${THIS_PACKAGE_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()

# Install directories
install(DIRECTORY config launch urdf meshes
  DESTINATION share/${PROJECT_NAME}
)


# Include directories
include_directories(
  include
  ${gazebo_ros_INCLUDE_DIRS}
  ${rclcpp_INCLUDE_DIRS}
)

# If you need executables
# add_executable(floribot_simulation_node src/simulation_node.cpp)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  find_package(ament_lint_auto REQUIRED)

  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(
  rclcpp
  gazebo_ros
  std_msgs
  #ros2_control
  ign_ros2_control
)

ament_package()
