# mecanum_car_ros2

## Setup

### 1. Create a Python virtual environment
python -m venv .venv

### 2. Activate the virtual environment
source .venv/bin/activate

### 3. Install Python dependencies
pip install -r requirements.txt

## Build ROS 2 packages

### 4. Build with colcon
colcon build

### 5. Source the install setup
source install/setup.bash

## Run nodes / executables

### 6. Run nodes with ros2
ros2 run <package_name> <executable_name>
