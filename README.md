
## Aktueller Migrationsstand

Die folgende Tabelle gibt einen Überblick über den aktuellen Stand der Migration einzelner Pakete von ROS 1 zu ROS 2. Jedes Paket durchläuft mehrere Phasen, beginnend mit der Analyse der Abhängigkeiten und Schnittstellen, über die schrittweise Portierung der Codebasis bis hin zur vollständigen Integration in die ROS 2 Umgebung. Während einige Pakete bereits erfolgreich migriert wurden, befinden sich andere noch in der Bearbeitung oder sind aufgrund bestehender Abhängigkeiten noch nicht gestartet.

| Paket                 | Status         | Bemerkungen                                    |
|-----------------------|--------------------|--------------------------------------------|
| base                  | ⏳ In Arbeit       | Teilweise migriert, Tests laufen           |
| base2gazebo           | ⏳ In Arbeit |                                            |
| maize_navigation      | ❌ Nicht gestartet |                                            |
| PointCloudTransformer | ❌ Nicht gestartet |                                            |
| FieldRobotNavigator   | ❌ Nicht gestartet |                                            |
=======
| Paket                 | Status             | Bemerkungen                                   | Branch           |Wer        |
|-----------------------|--------------------|-----------------------------------------------|------------------|-----------|
| base                  | ✅Fertig           | vollständig migriert                          | base_ros2        | Aaron    |
| base2gazebo           | ✅Fertig           | vollständig migriert                          | base2gazebo_ros2 | Jannis  |
| scan2cart             | ✅Fertig      | vollständig migriert                                      | base_ros2        | Jannis & Aaron   |
| maize_navigation      | ✅Fertig        | vollständig migriert                    |                  | Aaron    |
| Floribot_simulation   | noch nicht gestartet       |                                               | base2gazebo_ros2 |          |

# Individuelle Änderungen
sick_scan_xd in CMakeLists.txt urdf in share file installieren
line 915: install(DIRECTORY urdf DESTINATION share/${PROJECT_NAME})


in generate_world.py Koordinaten der Spawnposition ändern
line 119-126 ersetzen mit:
      content = launch_file_template.render(
          x=float(self.fgen.start_loc[0][0]) + self.wd.rng.random() * 0.1 + 2.8,
          y=float(self.fgen.start_loc[0][1]) + self.wd.rng.random() * 0.1 + 0.1,
          z=0.35,
          roll=0,
          pitch=0,
          yaw=1.5707963267948966 + self.wd.rng.random() * 0.1 - 0.05,
      )
      
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
cd ~/floribot/ros1_ws
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
cd ~/floribot/ros2_ws
```
```
colcon build --symlink-install
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
source ~/floribot/ros1_ws/devel/setup.bash
```
```
source ~/floribot/ros2_ws/install/setup.bash
```
```
cd ~/floribot/bridge_ws
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
ros2 launch floribot_simulation FloriBot.launch.py
```
Terminal 3:
```
. install/local_setup.bash
```
```
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
```




