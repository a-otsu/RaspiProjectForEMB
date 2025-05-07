#!/bin/bash
if [! -e /home/pi/log.txt ] ;then
touch /home/pi/log.txt
fi

echo "start script at $(date)" >> /home/pi/log.txt
echo "Waiting for network..." >> /home/pi/log.txt

#接続前にスクリプトが終了してしまう場合、MAX_RETRIESを増やす。
MAX_RETRIES=30
RETRY_COUNT=0

#ネットワーク接続を待機。一定回数の試行しても接続が確認できない場合スクリプトを終了。
until ping -c 1 google.com > /dev/null 2>&1; do
    sleep 10
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
        echo "Network not available after multiple attempts, exiting..." >> /home/pi/log.txt
        exit 1
    fi
done
echo "Network is ready at $(date)" >> /home/pi/log.txt

/usr/bin/python3 /home/pi/send_images.py >> /home/pi/log.txt 2>&1
sleep 10
/usr/bin/python3 /home/pi/send_data.py >> /home/pi/log.txt 2>&1

echo "script complete at $(date)" >> /home/pi/log.txt