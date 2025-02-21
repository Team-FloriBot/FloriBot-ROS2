
## Floribot Simulation

Dieser Branch stellt den Versuch dar, die komplette Simulation in ROS2 zu migrieren. Dazu wurde in ROS 2 Humble gearbeitet.
Jedoch treten zurzeit noch einige Fehler auf die noch behebt werden müssen.

# Requirements
``
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-velocity-controllers
sudo apt install ros-humble-xacro

sudo apt install ros-humble-ros-gz-sim
sudo apt install ros-humble-ros-gz-bridge
sudo apt install ros-humble-joint-state-publisher
sudo apt install ros-humble-controller-manager
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
``
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
```bash
git clone -b floribot_simulation_ros2 https://github.com/Team-FloriBot/FloriBot-ROS2.git ~/floribot
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

# Bauen der Packages
```
cd ~/floribot/ros2_ws
```
``
colcon build --packages-select sick_scan_xd --cmake-args " -DROS_VERSION=2" " -DLDMRS=0" " -DSCANSEGMENT_XD=0" --event-handlers console_direct+
```
```
colcon build --symlink-install --packages-ignore sick_scan_xd
```

# Starten der Simulation
```
cd ~/floribot/ros2_ws
```
```
. install/setup.bash
```
```
ros2 launch floribot_simulation floribot_simulation.launch.py
```



