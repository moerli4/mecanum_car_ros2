cmake_minimum_required(VERSION 3.8)
project(control_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/FaceBoundingBox.msg"
  "msg/FaceBoundingBoxArray.msg"
  "msg/PoseLandmarks.msg"
  "msg/HandGesture.msg"
  "msg/HandGestureArray.msg"
)

ament_package()
