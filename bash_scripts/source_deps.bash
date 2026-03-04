#!/usr/bin/env bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="$ROOT_DIR/install"

# source ROS
if [ -f "/opt/ros/jazzy/setup.bash" ]; then
    source /opt/ros/jazzy/setup.bash
fi

# Livox SDK
export CMAKE_PREFIX_PATH="$INSTALL_DIR/livox_sdk:${CMAKE_PREFIX_PATH:-}"
export LD_LIBRARY_PATH="$INSTALL_DIR/livox_sdk/lib:${LD_LIBRARY_PATH:-}"

# ROS workspace
if [ -f "$ROOT_DIR/install/setup.bash" ]; then
    source "$ROOT_DIR/install/setup.bash"
fi

echo "Dependencies sourced."