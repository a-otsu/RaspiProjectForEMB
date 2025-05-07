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

def get_usb_camera_count(max_devices=10):
    count = 0
    for i in range(max_devices):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            count += 1
            cap.release()
    return count

def capture_photos(config):
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    output_dir_name = config["image_config"]["output_directory"]
    output_dir = os.path.join(current_dir, output_dir_name)

    num_cameras = get_usb_camera_count()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for cam_id in range(num_cameras):
        try:
            cap = cv2.VideoCapture(cam_id)
            if not cap.isOpened():
                print(f"Camera {cam_id} could not be opened.")
                continue

            ret, frame = cap.read()
            if ret:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(output_dir, f"camera_{timestamp}{cam_id}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Photo saved: {filename}")
                send_image(filename, config)
            else:
                print(f"Failed to capture photo from camera {cam_id}.")
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error with camera {cam_id}: {e}")

if __name__ == "__main__":
    config = load_config()  # 設定ファイルを読み込む
    capture_photos(config)
