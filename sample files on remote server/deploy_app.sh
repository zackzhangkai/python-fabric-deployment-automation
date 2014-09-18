#!/bin/bash

# Default values
ARCHIVE_URL=""
INSTANCE=""

# Other variables
APP_SERVER_DIR="/${INSTANCE}/</path/to/app/server>"
TMP_FILE="/tmp/deploy_app_tmp.$$"

# Clean up on failures
trap "rm -f $TMP_FILE >/dev/null 2>&1" 0 1 2 15

# Process command-line arguments
while getopts ":f:i:" opt
do
        case $opt in
        
        f)      ARCHIVE_URL="$OPTARG"      ;;
        i)      INSTANCE="$OPTARG"      ;;

        *)      echo "Invalid option: -$OPTARG" ; exit 1 ;;

        esac

done

# Parameter validation
[ $OPTIND -gt $# ]      || { echo "Invalid option: $@" ; exit 1; }
[ -n "$ARCHIVE_URL" ]      || { echo "ARCHIVE_URL not set - use option -f" ; exit 1; }
[ -n "$INSTANCE" ]      || { echo "INSTANCE not set - use option -i" ; exit 1; }

# Sanity checks
[ -d "$APP_SERVER_DIR" ] || { echo "$APP_SERVER_DIR does not exist - wrong path?"; exit 1; }
[ -f "/etc/init.d/$INSTANCE" ] || { echo "/etc/init.d/$INSTANCE does not exist - wrong instance name?"; exit 1; }


echo "Downloading archive file"
/path/to/wget --progress=bar:force --no-check-certificate -O $TMP_FILE "$ARCHIVE_URL" 2>&1
if [ $? != 0 ]; then
        echo "Download failed"
        exit 1
fi


echo "Stopping tomcat instance"
/etc/init.d/$INSTANCE stop
if [ $? != 0 ]; then
        echo "Stop tomcat failed"
        exit 1
fi

echo "Waiting for tomcat to stop"
for i in 1 2 3 4 5 6
do
        sleep 5
        pgrep -f "java -Dinstance=${INSTANCE}" >/dev/null 2>&1
        if [ $? = 1 ]; then break; fi
        echo ... wait $i
done
pkill -9 -f "java -Dinstance=${INSTANCE}" >/dev/null 2>&1

echo "Removing old files"
rm -rf $APP_SERVER_DIR/tmp/*
rm -rf $APP_SERVER_DIR/work/*
rm -rf $APP_SERVER_DIR/webapps/<archive>


echo "Copying archive file"
cp -f $TMP_FILE "$APP_SERVER_DIR/deploy/<archive>"
if [ $? != 0 ]; then
        echo "Copy archive failed"
        exit 1
fi
chown tomcat:tomcat "$APP_SERVER_DIR/deploy/<archive>"


echo "Starting tomcat instance"
/etc/init.d/$INSTANCE start
if [ $? != 0 ]; then
        echo "Start tomcat failed"
        exit 1
fi


echo "Successfull completion"
exit 0
