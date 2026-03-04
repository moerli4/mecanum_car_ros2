#!/usr/bin/env bash
set -eo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THIRDPARTY_DIR="$ROOT_DIR/thirdparty"
INSTALL_DIR="$ROOT_DIR/install"

log_ok() { echo "[OK] $1"; }
log_fail() { echo "[FAIL] $1"; }

mkdir -p "$INSTALL_DIR"

(
set -e

cd "$THIRDPARTY_DIR/livox_sdk"

mkdir -p build
cd build

cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR/livox_sdk"

make -j$(nproc)
make install

) && log_ok "Livox SDK build" || log_fail "Livox SDK build"

echo
echo "SDK setup complete."