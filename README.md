# FloriBot-ROS2
Dieser Branch wird dazu genutzt den Floribot auf ROS2 umzuschreiben.
Der erste Commit stellt ist eine clone des main Branches des Advanced_Navigation Repositorys vom 20.01.2025 dar.
Dieser ist noch auf ROS 1 basierend.
Mit jedem Commit wird das Repository stückweise auf ROS 2 umgeschrieben.

# Klonen des Repository
```bash
git clone https://github.com/Team-FloriBot/FloriBot-ROS2.git ~/floribot
```
```
cd ~/floribot
```
```
git submodule init
```
```
git submodule update
```

# Bauen der Bridge und Packages
Terminal 1:
```
cd ~
```
```
source /opt/ros/noetic/setup.bash
```
```
cd floribot/ros1_ws
```
```
catkin_make
```
Terminal 2:
```
cd ~
```
```
source /opt/ros/foxy/setup.bash
```
```
cd floribot/ros2_ws
```
```
colcon build
```
Terminal 3:
```
cd ~
```
```
source /opt/ros/noetic/setup.bash
```
```
source /opt/ros/foxy/setup.bash
```
```
source /floribot/ros1_ws/devel/setup.bash
```
```
source /floribot/ros2_ws/install/setup.bash
```
```
cd floribot/bridge_ws
```
```
colcon build --packages-select ros1_bridge --cmake-force-configure
```
# Starten der Simulation
Terminal 1:
```
. devel/setup.bash
```
```
rosrun virtual_maize_field generate_world.py fre22_task_navigation_mini
```
```
rosrun virtual_maize_field generate_world.py fre22_task_navigation_mini
```
```
roslaunch floribot_simulation FloriBot.launch
```
Terminal 2:
```
. install/setup.bash
```
```
ros2 launch base base_node.launch.py
```
Terminal 3:
```
. <workspace-parent-path>/bridge_ws/install/local_setup.bash
```
```
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
```




