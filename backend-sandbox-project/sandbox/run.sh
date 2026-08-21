#!/bin/bash
set -e

SOURCE_FILE="/tmp/main.cpp"
EXECUTABLE="/tmp/app"

cat > "$SOURCE_FILE"

g++ "$SOURCE_FILE" -std=c++17 -O2 -o "$EXECUTABLE"
"$EXECUTABLE"
