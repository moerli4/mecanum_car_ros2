# mecanum_car_ros2

create .venv: python -m venv .venv

source venv: source .venv/bin/activate

install requirements.txt: pip install -r requirements.txt


cd: cd ros2_ws

build packages: colcon build

source: source install/setup.bash

run package *: ros2 run *
