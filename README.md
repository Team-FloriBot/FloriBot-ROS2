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
