# mecanum_car_ros2

## Installation 

### Setup

Create the venv
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Setup Livox SDK
```
./bash_scripts/setup_livox_sdk.bash
```

Build ROS 2 workspace
```
./bash_scripts/build_env.bash
```

Source workspace
```
source ./bash_scripts/source_deps.bash
```

### Run

Start drivers with 
```
ros2 launch launch_files drivers_bringup.launch.xml
```

Launch the Livox Lidar stuff (First add the livoxs ip address (192.168.1.5 for MID360) to your devices wired connections with network=24)
```
ros2 launch livox_ros_driver2 msg_MID360_launch.py
ros2 launch fast_lio mapping.launch.py 
```

Run individual packages with
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
<!-- note: we use FAST-LIO as a starting point, this does not include loop closure though... if drift is too large we can try LIO or some other slam method instead -->