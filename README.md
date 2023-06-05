# dpp2023

Структура для проекта

* mkdir /catkin_ws/src/main_package
* mkdir /catkin_ws/src/main_package/include
* mkdir /catkin_ws/src/main_package/launch
* mkdir /catkin_ws/src/main_package/src
* mkdir /catkin_ws/src/main_package/srv
*
* nano /catkin_ws/src/main_package/CMakeLists.txt
* nano /catkin_ws/src/main_package/package.xml
* 
* nano /catkin_ws/src/main_package/launch/main.launch
* nano mkdir /catkin_ws/src/main_package/srv/GetCommands.srv

* Прописать запуск rosserial_arduino в /etc/ros/turtlebro.d/turtlebro.launch 
* Прописать запуск main.launch в /etc/ros/turtlebro.d/turtlebro.launch 



* Настроить ros_master_uri
* nano ./.ros_params

*machine_ip=$(hostname  -I | cut -f1 -d' ')
*export ROS_HOSTNAME=localhost
*export ROS_IP=localhost
*export ROS_MASTER_URI=http://localhost:11311
*export ROVER_MODEL=brover
*export ROVER_WHEEL_PARAM=12280
