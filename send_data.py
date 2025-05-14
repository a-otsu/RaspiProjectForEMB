import serial
import requests
import yaml
import os
import time

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

def read_data_from_arduino(config):
    """Arduinoからデータを取得"""
    try:
        ser = serial.Serial(config["data_config"]["serial_port"], baudrate=config["data_config"]["baudrate"], timeout=config["data_config"]["timeout"])
        text = ser.read(200).decode()  # バイナリデータをデコード
        ser.close()
        print(text)

        start_tag = config["data_config"]["start_tag"]
        end_tag = config["data_config"]["end_tag"]

        # データの部分を抽出
        start_index = text.find(start_tag) + len(start_tag)
        end_index = text.find(end_tag)
        data_text = text[start_index:end_index]
        print("Extracted data:")
        print(data_text)
        return data_text
    except Exception as e:
        print(f"Error reading data from Arduino: {e}")
        return None

def send_data_to_database(config, data_text):
    """データをサーバーに送信"""
    try:
        url = config["data_config"]["url"]
        payload = {
            "user_name": config["user_info"]["user_name"],
            "pass": config["user_info"]["password"],
            "sensor_data": data_text
        }

        response = requests.post(url, data=payload)
        print(f"Response status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to the database: {e}")

if __name__ == "__main__":
    # 設定ファイルの読み込み
    config = load_config()

    # シリアルポート接続の確認
    check_serial_connection(config)

    #Arduinoに開始フラグを送る
    send_command_to_arduino(config, "START")
    time.sleep(5)

    # Arduinoにコマンドを送る
    send_command_to_arduino(config, "s")
    time.sleep(5)

    # Arduinoからデータを取得
    data_text = read_data_from_arduino(config)

    if data_text:
        # サーバーにデータを送信
        send_data_to_database(config, data_text)



