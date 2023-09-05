#!/bin/bash

### THIS SCRIPT IS TRIGGERED BY A CRONJOB ON BOOT
### To Modify Startup, use this command
### sudo crontab -e

APP_DIR="/home/pi/aetherart"
LOGFILE="/home/pi/aetherart/logs"
WEBLOG_FILE="/home/pi/aetherart/logs/webserver.log" 
APPLOG_FILE="/home/pi/aetherart/logs/aetherart.log" 

# Change to the directory where your Python scripts are located
cd $APP_DIR

# Run web_server.py in the background
sudo python webserver.py >> "$WEBLOG_FILE" 2>&1 &

# Sleep for a few seconds to give web_server.py some time to start (if needed)
sleep 5

# Run slideshower.py in the foreground
sudo python aetherart.py >> "$APPLOG_FILE" 2>&1 &

