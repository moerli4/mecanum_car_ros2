#!/usr/bin/env bash
set -eo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Sourcing dependencies..."
source "$ROOT_DIR/bash_scripts/source_deps.bash"

echo "Building ROS workspace..."

cd "$ROOT_DIR"

colcon build \
  --symlink-install \
  --cmake-args -DCMAKE_BUILD_TYPE=Release -Wno-dev

echo "Build finished."