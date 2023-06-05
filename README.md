# dpp2023

Структура для проекта

* mkdir /catkin_ws/src/main_package
* mkdir /catkin_ws/src/main_package/include
* mkdir /catkin_ws/src/main_package/launch
* mkdir /catkin_ws/src/main_package/src
* mkdir /catkin_ws/src/main_package/srv

* nano /catkin_ws/src/main_package/CMakeLists.txt
* nano /catkin_ws/src/main_package/package.xml

* nano /catkin_ws/src/main_package/launch/main.launch
* nano mkdir /catkin_ws/src/main_package/srv/GetCommands.srv

<h5> Прописать запуск rosserial_arduino в /etc/ros/turtlebro.d/turtlebro.launch </h5>
<h5> Прописать запуск main.launch в /etc/ros/turtlebro.d/turtlebro.launch </h5>



<h2> Настроить ros_master_uri </h2>

* nano ./.ros_params

<h5> machine_ip=$(hostname  -I | cut -f1 -d' ') </h5>
<h5> export ROS_HOSTNAME=localhost </h5>
<h5> export ROS_IP=localhost </h5>
<h5> export ROS_MASTER_URI=http://localhost:11311 </h5>
<h5> export ROVER_MODEL=brover </h5>
<h5> export ROVER_WHEEL_PARAM=12280 </h5>

<h5>После настройки ровера требуется запустить файлы read_file.py (для получения фото с ровера) и send_from_pot.py (для управления ровером)</h5>
<h5>При запуске ровера запускаются скрипты из файла main.launch (main.py и radio.py)</h5>

Ровер готов к работе!

За подробностями обращайтесь ко мне в тг @llIlIIlllIIl
(+7 977 425 12 79)
