#!/bin/bash


HOME_DIR="/home/pi"
APP_DIR_NAME="aetherart"
FRAMES_DIR_NAME="frames"
IMAGES_DIR_NAME="images"
TEMP_DIR_NAME="temp"
LOGS_DIR_NAME="logs"
WEBSERVER_DIR_NAME="webserver"
LAUNCHER_NAME="launcher.sh"
LOGFILE_NAME="cron.log"
APPFILES_NAME="files.zip"
APPFILES_URL="https://github.com/jazzbiddy/aetherart/archive/refs/heads/main.zip"


################


APP_DIR="$HOME_DIR/$APP_DIR_NAME"
FRAMES_DIR="$APP_DIR/$FRAMES_DIR_NAME"
IMAGES_DIR="$APP_DIR/$IMAGES_DIR_NAME"
TEMP_DIR="$APP_DIR/$TEMP_DIR_NAME"
WEBSERVER_DIR="$APP_DIR/$WEBSERVER_DIR_NAME"
LAUNCHER_PATH="$APP_DIR/$LAUNCHER_NAME"
LOGS_DIR="$APP_DIR/$LOGS_DIR_NAME"
LOGFILE_PATH="$LOGS_DIR/$LOGFILE_NAME"
APPFILES_PATH="$TEMP_DIR/$APPFILES_NAME"

### CREATE DIRECTORIES

#APP_DIR
if [ -d "$APP_DIR" ]; then
  echo "App Directory already exists"
else
  mkdir -p "$APP_DIR"
  echo "App Directory created"
fi

#FRAMES_DIR
if [ -d "$FRAMES_DIR" ]; then
  echo "Frames Directory already exists"
else
  mkdir -p "$FRAMES_DIR"
  echo "Frames Directory created"
fi

#IMAGES_DIR
if [ -d "$IMAGES_DIR" ]; then
  echo "Images Directory already exists"
else
  mkdir -p "$IMAGES_DIR"
  echo "Images Directory created"
fi

#WEBSERVER_DIR
if [ -d "$WEBSERVER_DIR" ]; then
  echo "Webserver Directory already exists"
else
  mkdir -p "$WEBSERVER_DIR"
  echo "Webserver Directory created"
fi

#LOGS
if [ -d "$LOGS_DIR" ]; then
  echo "Logs Directory already exists"
else
  mkdir -p "$LOGS_DIR"
  echo "Logs Directory created"
fi

# TEMP DIR
if [ -d "$TEMP_DIR" ]; then
  echo "Temp Directory already exists"
else
  mkdir -p "$TEMP_DIR"
  echo "Temp Directory created"
fi


### Add Crontab setting
### TODO - CHECK TO MAKE SURE THIS DOESN'T OVERWRITE ANY EXISTING JOBS

# line to add to the crontab
cron_line="@reboot sh $LAUNCHER_PATH >$LOGFILE_PATH 2>&1"

# Check if the line is already in the crontab
if ! (sudo crontab -l | grep -Fxq "$cron_line"); then
    # If it's not present, add the line
    (sudo crontab -l ; echo "$cron_line") | sudo crontab -
    echo "Crontab entry added."
else
    echo "Crontab entry already exists."
fi


### INSTALL PYTHON REQUIREMENTS
pip install requests pillow pygame


### DOWNLOAD APP FILES 
curl -o $APPFILES_PATH $APPFILES_URL

### UNZIP APPFILES


### PUT APP FILES INTO THE RIGHT PLACES


### DELETE TEMPORARY APP FILES






