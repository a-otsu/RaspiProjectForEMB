import serial
import requests
import yaml
import time
import os

def load_config(config_name="config.yaml"):
    
    """設定ファイルを読み込む"""
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    config_path = os.path.join(current_dir, config_name)
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def load_board_config(config):
    url= config["board_config"]["url_base"] + config["user_info"]["user_name"] + ".json"
    header= {"content-type": "application/json"}
    r=requests.get(url, header)
    print(r.json())
    data=r.json()
    return data

def send_command_to_arduino(config, command):
    """Arduinoにコマンドを送信"""
    try:
        ser = serial.Serial(config["data_config"]["serial_port"], baudrate=config["data_config"]["baudrate"])
        ser.write(command.encode())
        print(f"Command '{command}' sent to Arduino.")
        ser.close()
    except Exception as e:
        print(f"Error sending command to Arduino: {e}")


if __name__ == "__main__":
    config = load_config()
    first_command="START"
    send_command_to_arduino(config,first_command)
    time.sleep(5)
    data = load_board_config(config)
    command=data["enable_maintenance"]
    send_command_to_arduino(config,command)
    time.sleep(5)
    command=data["activation_interval"]
    send_command_to_arduino(config,command)
    time.sleep(5)
    final_command="END"
    send_command_to_arduino(config,final_command)