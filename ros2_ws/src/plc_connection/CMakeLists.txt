cmake_minimum_required(VERSION 3.5)
project(plc_connection)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find ament packages and dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(base REQUIRED)

# Add service files
rosidl_generate_interfaces(plc_connection
  "srv/GetCount.srv"
  DEPENDENCIES std_msgs
)


include_directories(
  include
  ${rclcpp_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
  ${geometry_msgs_INCLUDE_DIRS}
  ${tf2_INCLUDE_DIRS}
  ${tf2_ros_INCLUDE_DIRS}
  ${base_INCLUDE_DIRS}
  ${rosidl_default_generators_INCLUDE_DIRS}
  ${CMAKE_BINARY_DIR}/rosidl_generator_cpp/${PROJECT_NAME}
)


ament_export_dependencies(rosidl_default_runtime)
ament_export_include_directories(${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp)
ament_export_include_directories(include)

add_library(plc_connection_lib
  src/plc_connection_lib.cpp
)
add_library(udp_socket
  src/network/udp/udp_socket.cpp
)
add_library(socket
  src/network/socket/socket.cpp
)

add_executable(${PROJECT_NAME}_node src/${PROJECT_NAME}_node.cpp)


# Link dependencies


target_link_libraries(socket
  rclcpp::rclcpp
)

target_link_libraries(udp_socket
  rclcpp::rclcpp
  socket
)

target_link_libraries(plc_connection_lib
  rclcpp::rclcpp
  socket
  udp_socket
)

target_link_libraries(${PROJECT_NAME}_node
  rclcpp::rclcpp
  udp_socket
  socket
  plc_connection_lib
)

ament_target_dependencies(${PROJECT_NAME}_node rclcpp base tf2 tf2_ros std_msgs geometry_msgs)


rosidl_target_interfaces(plc_connection_lib
  plc_connection "rosidl_typesupport_cpp"
)

rosidl_target_interfaces(${PROJECT_NAME}_node
  ${PROJECT_NAME} "rosidl_typesupport_cpp"
)

rosidl_target_interfaces(socket
  plc_connection "rosidl_typesupport_cpp"
)

rosidl_target_interfaces(udp_socket
  plc_connection "rosidl_typesupport_cpp"
)

#

# Add install targets
install(TARGETS
  ${PROJECT_NAME}_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include
)

# Ament export
ament_package()