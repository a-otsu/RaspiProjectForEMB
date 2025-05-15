#!/bin/bash

LOG_FILE="/home/pi/RaspiProjectForEMB/log.txt"

if [ ! -e "$LOG_FILE" ]; then
    touch "$LOG_FILE"
fi

echo "start script at $(date)" >> "$LOG_FILE"
echo "Waiting for network..." >> "$LOG_FILE"

MAX_RETRIES=30
RETRY_COUNT=0

# ネットワーク接続確認
until ping -c 1 google.com > /dev/null 2>&1; do
    sleep 10
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
        echo "Network not available after multiple attempts, exiting..." >> "$LOG_FILE"
        exit 1
    fi
done

echo "Network is ready at $(date)" >> "$LOG_FILE"

cd /home/pi/RaspiProjectForEMB

/usr/bin/python3 send_data.py >> "$LOG_FILE" 2>&1 || exit 1
echo "Data sent at $(date) wait camera" >> "$LOG_FILE"
sleep 5
/usr/bin/python3 send_images.py >> "$LOG_FILE" 2>&1
echo "images.py exit" >> "$LOG_FILE"
sleep 5
/usr/bin/python3 get_board_conf.py >> "$LOG_FILE" 2>&1 || exit 1

echo "script complete at $(date)" >> "$LOG_FILE"