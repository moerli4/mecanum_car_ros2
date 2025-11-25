# mecanum_car_ros2

## Installation 

### Setup

Create the venv
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Build ROS 2 workspace
```
colcon build
source install/setup.bash
```

Start drivers with 
```
ros2 launch launch_files drivers_bringup.launch.xml
```

and run individual packages with
```
ros2 run <package_name> <executable_name>
```

## Development & Contributing
Please apply black and isort before committing
```
black .
isort . 
```
Run tests with
```
pytest <directory_path>
```
to run hardware tests use the flag `-m hardware`.
