#!/bin/bash


HOME_DIR="/home/pi"
APP_DIR_NAME="aetherart"
FRAMES_DIR_NAME="frames"
IMAGES_DIR_NAME="images"
LOGS_DIR_NAME="logs"
WEBSERVER_DIR_NAME="webserver"
LAUNCHER_NAME="launcher.sh"
LOGFILE_NAME="cron.log"

################

APP_DIR="$HOME_DIR/$APP_DIR_NAME"
FRAMES_DIR="$APP_DIR/$FRAMES_DIR_NAME"
IMAGES_DIR="$APP_DIR/$IMAGES_DIR_NAME"
WEBSERVER_DIR="$APP_DIR/$WEBSERVER_DIR_NAME"
LAUNCHER_PATH="$APP_DIR/$LAUNCHER_NAME"
LOGS_DIR="$APP_DIR/$LOGS_DIR_NAME"
LOGFILE_PATH="$LOGS_DIR/$LOGFILE_NAME"

### CREATE DIRECTORIES
# APP DIR
if [ -d "$APP_DIR" ]; then
  echo "App Directory already exists"
else
  mkdir -p "$APP_DIR"
  echo "App Directory created"
fi

# FRAMES DIR
if [ -d "$FRAMES_DIR" ]; then
  echo "Frames Directory already exists"
else
  mkdir -p "$FRAMES_DIR"
  echo "Frames Directory created"
fi

# IMAGES DIR
if [ -d "$IMAGES_DIR" ]; then
  echo "Images Directory already exists"
else
  mkdir -p "$IMAGES_DIR"
  echo "Images Directory created"
fi

# WEBSERVER DIR
if [ -d "$WEBSERVER_DIR" ]; then
  echo "Webserver Directory already exists"
else
  mkdir -p "$WEBSERVER_DIR"
  echo "Webserver Directory created"
fi

# LOGS DIR
if [ -d "$LOGS_DIR" ]; then
  echo "Logs Directory already exists"
else
  mkdir -p "$LOGS_DIR"
  echo "Logs Directory created"
fi

