
## Aktueller Migrationsstand

Die folgende Tabelle gibt einen Überblick über den aktuellen Stand der Migration einzelner Pakete von ROS 1 zu ROS 2. Jedes Paket durchläuft mehrere Phasen, beginnend mit der Analyse der Abhängigkeiten und Schnittstellen, über die schrittweise Portierung der Codebasis bis hin zur vollständigen Integration in die ROS 2 Umgebung. Während einige Pakete bereits erfolgreich migriert wurden, befinden sich andere noch in der Bearbeitung oder sind aufgrund bestehender Abhängigkeiten noch nicht gestartet.

=======
| Paket                 | Status          |ROS Version   | Bemerkungen                                   | Branch           |Wer      |
|-----------------------|-----------------|---------------|-----------------------------------------------|------------------|---------|
| base                  | ✅Fertig       | Foxy           | vollständig migriert                          | base_ros2        | Aaron   |
| base2gazebo           | ✅Fertig        | Foxy           | vollständig migriert                          | base2gazebo_ros2 | Jannis  |
| scan2cart             | ✅Fertig       | Foxy            | vollständig migriert                          | scan_tool        | Jannis & Aaron   |
| maize_navigation      | ✅Fertig       | Foxy            | vollständig migriert                          | maize_navigation_ros2| Aaron   |
| plc_communication     | ✅Fertig       | Foxy            | vollständig migriert                          | plc_communication_ros2 | Jannis  |
| Floribot_simulation   | ⌛in Arbeit    | Humble            |                                               | Floribot_simulation_ros2 | Aaron   |
# Individuelle Änderungen
in sick_scan_xd in CMakeLists.txt urdf in share file installieren
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
```
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
```
roslaunch floribot_simulation FloriBot.launch
```
Terminal 2:
```
. install/setup.bash
```
```

ros2 launch floribot_simulation FloriBot.launch.py
```
Terminal 3:
```
. install/local_setup.bash
```
```
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
```

# Requirements
Folgende Bibliotheken müssen vor Nutzung installiert werden:
```
sudo apt install ros-noetic-velocity-controllers
```
```
sudo apt install ros-noetic-ddynamic-reconfigure
```
```
curl -sSL http://get.gazebosim.org | sh
```
```
sudo apt install python-is-python3
```
```
sudo apt install ros-noetic-xacro
```
```
sudo apt-get install ros-noetic-can-msgs
```
```
sudo apt install ros-noetic-tf2-sensor-msgs
```
Bitte der Installationsanleitung folgen: https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md
Hierbei müssen die Pakete librealsense2-dkms, librealsense2-utils und librealsense2-dev installiert werden.
```
sudo apt-get install python3-colcon-common-extensions
```
```
sudo apt-get install ros-foxy-gazebo-ros-pkgs
```
```
sudo apt install ros-foxy-ros2-control ros-foxy-ros2-control
```
```
sudo apt remove ros-foxy-controller-manager-msgs
```
```
sudo apt install ros-foxy-laser-geometry
```
```
sudo apt-get install ros-foxy-sensor-msgs-py
```
```
sudo apt install python3-pip
```
```
sudo apt install ros-foxy-xacro
```
```
sudo apt install ros-foxy-can-msgs
```
```
sudo apt install python3-sensor-msgs
```
```
pip3 install jinja2
```
```
pip3 install shapely
```
```
pip3 install xacro
```
```
sudo apt install python3-rosdep2
```
```
rosdep update
```
in allen ws:
```
rosdep install --from-paths src --ignore-src -r -y
```
```
sudo apt update
```
```
sudo apt upgrade
```
# Bekannte Fehler:
/usr/bin/ld: libros1_bridge.so: undefined reference to `ros1_bridge::Factory<controller_manager_msgs::ControllerState_<std::allocator<void> >, controller_manager_msgs::msg::ControllerState_<std::allocator<void> > >::convert_1_to_2(controller_manager_msgs::ControllerState_<std::allocator<void> > const&, controller_manager_msgs::msg::ControllerState_<std::allocator<void> >&)'

--> im Terminal folgendes ausführen:
```
sudo apt remove ros-foxy-controller-manager-msgs
```
