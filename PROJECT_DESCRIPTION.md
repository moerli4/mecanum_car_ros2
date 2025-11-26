## Project Description Drive Proj 2

Beginner friendly project with the goal of creating the control software to an autonomous car kit we bought online.


Not much hardware stuff, mostly software. Good for actively getting to know the ROS2, Python, C++, Ubuntu basics.


Car includes some sensors (camera, ultrasound, infrared track sensor, infrared remote sensor), a Raspberry Pi 5 and four motors with omniwheels. And we now want to do control stuff with this. 

Possible control tasks we aim to achieve include stuff like:
- line following
- camera pose detection/face detection
- obstacle evasion
- whatever else you want to do

Whats already done:
- car assembly
- Ubuntu & ROS2 installation on the car
- basic drivers for all sensors and actuators

### Prerequisite knowledge for joining this project:
#### Ubuntu 24.04
- basic file structure
- handling of virtual environments (sourcing)
- using the command line
- ssh
#### ROS2 Jazzy
- ROS2 build tools (colcon build, source install/setup.bash, cmakelists.txt, setup.py, package.xml etc)
- publisher/subscriber communication
- server/client communication
- interfaces
- launchfiles
- command line inspection tools
- object oriented node templates in both c++ and python
- https://docs.ros.org/en/jazzy/Concepts/Basic.html
#### Git
- clone, add, commit -m, push, pull, mv ...
- branches
- best practices:
    - never push to *main* branch, instead create a new branch for each task and merge when finished
    - frequent small commits are better than rare large commits
    - use concise but meaningful commit messages
    - linting: run black and isort to keep the repo clean and structured
- https://git-scm.com/cheat-sheet
#### Python and C++
- i think this is self explanatory
