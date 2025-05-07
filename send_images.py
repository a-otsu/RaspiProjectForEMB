import subprocess
import re
import cv2
import os
import datetime
from pathlib import Path
import requests
import yaml

def load_config(config_name="config.yaml"):
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    config_path = os.path.join(current_dir, config_name)
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def send_image(image_path, config):
    url = config["image_config"]["url"]
    user_name = config["user_info"]["user_name"]
    password = config["user_info"]["password"]
    delete_after_upload = config["image_config"].get("delete_after_upload", False)  # デフォルトは削除しない

    try:
        with open(image_path, 'rb') as image_file:
            data = {'user_name': user_name, 'pass': password}
            files = {'image': image_file}
            response = requests.post(url, data=data, files=files)
            
            if response.status_code == 200:
                print(f"Image successfully sent!")
                # アップロード後に削除する
                if delete_after_upload:
                    os.remove(image_path)
                    print(f"Image deleted: {image_path}")
            else:
                print(f"Failed to send image. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error occurred while sending image: {e}")

def get_camera_devices():
    """v4l2-ctl の出力から実際のカメラデバイス（/dev/video*）の一覧を取得"""
    try:
        result = subprocess.run(['v4l2-ctl', '--list-devices'], stdout=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.splitlines()

        devices = []
        current_device = []

        for line in lines:
            if line.strip() == "":
                continue
            if not line.startswith("\t"):  # カメラ名の行
                if current_device:
                    devices.append(current_device)
                    current_device = []
            else:  # デバイスファイルの行
                match = re.search(r'/dev/video\d+', line)
                if match:
                    current_device.append(match.group())

        if current_device:
            devices.append(current_device)

        # 各カメラの最初の videoデバイスのみ使用
        return [dev_list[0] for dev_list in devices if dev_list]
    except Exception as e:
        print(f"Failed to get camera devices: {e}")
        return []

def capture_photos(config):
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    output_dir_name = config["image_config"]["output_directory"]
    output_dir = os.path.join(current_dir, output_dir_name)

    valid_devices = get_camera_devices()
    print(f"Detected cameras: {valid_devices}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, dev_path in enumerate(valid_devices):
        try:
            cap = cv2.VideoCapture(dev_path)
            if not cap.isOpened():
                print(f"Camera at {dev_path} could not be opened.")
                continue

            ret, frame = cap.read()
            if ret:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(output_dir, f"camera_{timestamp}_{i}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Photo saved: {filename}")
                send_image(filename, config)
            else:
                print(f"Failed to capture photo from camera {dev_path}.")
            cap.release()
        except Exception as e:
            print(f"Error with camera {dev_path}: {e}")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    config = load_config()  # 設定ファイルを読み込む
    capture_photos(config)
