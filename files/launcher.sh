#!/bin/bash

### THIS SCRIPT IS TRIGGERED BY A CRONJOB ON BOOT

HOME_DIR="/home/pi"
APP_DIR_NAME="aetherart"
LOG_NAME="webserver.log" 

###########

APP_DIR="$HOME_DIR/$APP_DIR_NAME"
LOG_FILE=$APP_DIR/$LOG_NAME

# Change to the directory where your Python scripts are located
cd $APP_DIR

# Run web_server.py in the background
python webserver.py >> "$LOG_FILE" 2>&1 &

# Sleep for a few seconds to give web_server.py some time to start (if needed)
sleep 5

# Run slideshower.py in the foreground
python aetherart.py

