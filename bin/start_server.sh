#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APP_PATH="$SCRIPT_DIR/../src/app.py"

if [ ! -f "$APP_PATH" ]; then
    echo "Error: $APP_PATH does not exist."
    exit 1
fi

python "$APP_PATH"