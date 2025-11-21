#!/bin/bash
# RViz2 wrapper script to fix libpthread symbol conflict
# This script sets LD_PRELOAD to force loading the system libpthread instead of the snap version

export LD_PRELOAD=/lib/x86_64-linux-gnu/libpthread.so.0
export QT_QPA_PLATFORM=xcb

exec /opt/ros/humble/bin/rviz2 "$@"
