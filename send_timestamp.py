import serial
import yaml
import os
import time
import datetime

def load_config(config_name="config.yaml"):
    """設定ファイルを読み込む"""
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    config_path = os.path.join(current_dir, config_name)
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def open_serial(config):
    """シリアルポートを開いて返す"""
    return serial.Serial(
        config["data_config"]["serial_port"],
        baudrate=config["data_config"]["baudrate"],
        timeout=config["data_config"]["timeout"]
    )

def send_command_and_wait_response(ser, command, label=""):
    """Arduinoにコマンドを送り、応答を待って表示"""
    try:
        print(f"[{label}] Sending: {command}")
        ser.write((command + "\n").encode())  # 改行付き
        response = ser.readline().decode().strip()
        print(f"[{label}] Received: {response}")
        return response
    except Exception as e:
        print(f"Error during send/receive: {e}")
        return ""

def make_timestamp_date():
    dt_now = datetime.datetime.now()
    timestamp_date = dt_now.year * 10000 + dt_now.month * 100 + dt_now.day
    return str(timestamp_date)

def make_timestamp_time():
    dt_now = datetime.datetime.now()
    timestamp_time = dt_now.hour * 10000 + dt_now.minute * 100 + dt_now.second
    return str(timestamp_time)

if __name__ == "__main__":
    config = load_config()

    try:
        ser = open_serial(config)
        time.sleep(2)  # Arduinoのリセット待ち（重要）

        # ステップ1：TIMESTAMP 開始
        send_command_and_wait_response(ser, "TIMESTAMP", label="STEP 1")

        # ステップ2：日付送信
        date_str = make_timestamp_date()
        send_command_and_wait_response(ser, date_str, label="STEP 2")

        # ステップ3：時刻送信
        time_str = make_timestamp_time()
        send_command_and_wait_response(ser, time_str, label="STEP 3")

        ser.close()

    except Exception as e:
        print(f"Serial connection failed: {e}")
