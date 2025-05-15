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

def check_serial_connection(config):
    """シリアルポートに接続できるか確認"""
    try:
        ser = serial.Serial(config["data_config"]["serial_port"], baudrate=config["data_config"]["baudrate"], timeout=config["data_config"]["timeout"])
        print(f"Successfully connected to {config['data_config']['serial_port']}")
        ser.close()  # 忘れずに閉じる
    except serial.SerialException as e:
        print(f"Failed to connect to {config['data_config']['serial_port']}: {e}")

def send_command_to_arduino(config, command):
    """Arduinoにコマンドを送信"""
    try:
        ser = serial.Serial(config["data_config"]["serial_port"], baudrate=config["data_config"]["baudrate"])
        ser.write(command.encode())
        print(f"Command '{command}' sent to Arduino.")
        ser.close()
    except Exception as e:
        print(f"Error sending command to Arduino: {e}")

    
def make_timestamp_date():
    dt_now=datetime.datetime.now()
    timestamp_date = dt_now.year*10000 + dt_now.month*100 + dt_now.day
    print(timestamp_date)
    return timestamp_date

def make_timestamp_time():
    dt_now=datetime.datetime.now()
    timestamp_time = dt_now.hour*10000 + dt_now.minute*100 + dt_now.second
    print(timestamp_time)
    return timestamp_time



if __name__ == "__main__":
    # 設定ファイルの読み込み
    config = load_config()

    # シリアルポート接続の確認
    check_serial_connection(config)

    #Arduinoに開始フラグを送る
    send_command_to_arduino(config, "TIMESTAMP")
    time.sleep(5)

    # Arduinoにタイムスタンプを送る
    send_command_to_arduino(config, str(make_timestamp_date()))
    time.sleep(5)

    # Arduinoにタイムスタンプを送る
    send_command_to_arduino(config, str(make_timestamp_time()))
    time.sleep(5)
