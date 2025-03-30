In diesem Branch wird die Migration auf dem FloriBot durchgeführt. Die Packages in diesem Branch sind genauso bereits auf dem FloriBot angelegt. Auf dem Roboter befindet sich ROS 2 Foxy

## Nächste Schritte

Zunächst sollte eine Keyboard-Steuerung oder Joystick-Steuerung, wie auf dem Handy für ROS  1, erstellt werden, um die vollständige Ansteuerung und Umrechnung der Koordinatensysteme des FloriBot testen zu können. Als nächstes sollte dann das Auslesen der Laserscanner programmiert und das maize_navigation-Package auf einem Maisfeld getestet werden. Außerdem sollte der Branch in diesem Zuge auch auf eine ROS 2 LTS Version geupdatet werden. Hierzu können die nötigen Packages des floribot_simulation_ros2-Branch einfach kopiert werden.


# Klonen des Repository
```
git clone -b RealRobotRos2 https://github.com/Team-FloriBot/FloriBot-ROS2.git ~/floribot
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

# Ausführen und Testen des Programms
Terminal 1:
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
colcon build
```

```
. install/setup.bash
```
```
ros2 launch floribot robot.launch.py
```

zum Testen der linearen Bewegung kann in einem zweiten Terminal folgendes ausgeführt werden.
Terminal 2:
```
source /opt/ros/foxy/setup.bash
```
```
cd ~/floribot/ros2_ws
```
```
. install/local_setup.bash
```
```
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

