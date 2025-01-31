## Aktueller Migrationsstand

Die folgende Tabelle gibt einen Überblick über den aktuellen Stand der Migration einzelner Pakete von ROS 1 zu ROS 2. Jedes Paket durchläuft mehrere Phasen, beginnend mit der Analyse der Abhängigkeiten und Schnittstellen, über die schrittweise Portierung der Codebasis bis hin zur vollständigen Integration in die ROS 2 Umgebung. Während einige Pakete bereits erfolgreich migriert wurden, befinden sich andere noch in der Bearbeitung oder sind aufgrund bestehender Abhängigkeiten noch nicht gestartet.

| Paket                 | Status             | Bemerkungen                                   | Branch           |Wer        |
|-----------------------|--------------------|-----------------------------------------------|------------------|-----------|
| base                  | ⏳ In Arbeit       | vollständig migriert, funktioniert teilweise  | base_ros2         | Aaron    |
| base2gazebo           | ⏳ In Arbeit       |                                               | base2gazebo_ros2  | Jannis   |
| maize_navigation      | ❌ Nicht gestartet |                                               |                   |          |
| PointCloudTransformer | ⏳ In Arbeit       |                                               | base_ros2         | Aaron    |
| FieldRobotNavigator   | ❌ Nicht gestartet |                                               |                   |          |

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




