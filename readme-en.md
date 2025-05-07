---
marp: false
---

# Raspberry Pi Setup Guide for Environmental Sensor Board

## How to install project using git
1. check git installation by executing
  ```bash
  git --version
  ```
  - if not installed : install git by executing
  ```bash
  sudo apt update
  sudo apt install git
  ```

2. git clone
  clone repository by executing
  ```bash
  git clone [url to github repository] [install directory name]
  ```
  url: https://github.com/a-otsu/RaspiProjectForEMB.git
  directory name is optional.


## About the Distributed Files

- **Python Scripts (.py)**
  - `send_data.py`  
    Sends commands to the Arduino to receive sensor data and uploads it to the server.
  - `send_images.py`  
    Captures images using a camera and uploads them to the server.

- **Shell Script (.sh)**
  - `run_scripts.sh`  
    A shell script that runs the Python scripts at the appropriate timing.

- **Configuration File (.yaml)**
  - `config.yaml`  
    Contains various settings.  
    See the comments in the YAML file for descriptions of each setting.

- **Systemd Service File (.service)**
  - `script_sequence.service`  
    A service file to run the shell script automatically on boot.

## Required Python Modules

The following Python modules are required to run the programs:

- `pyserial`  
    Used for serial communication with the Arduino.
- `requests`  
    Used to send HTTP requests to the server.
- `pyyaml`  
    Used to read the configuration file.
- `cv2`  
    Used for capturing images from the camera.

Install them by running the following commands in the terminal.  
Some dependencies require installation in order, so it's recommended to run them from top to bottom:

```bash
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo pip3 install opencv-python --break-system-packages
sudo pip install pyserial --break-system-packages
sudo pip install requests --break-system-packages
sudo pip install pyyaml --break-system-packages
```

After placing the file, enable the service by running:
```bash
sudo systemctl enable script_sequence.service
```

## Enabling UART Communication
If you're using UART pins for serial communication, note that UART is disabled by default in many Raspberry Pi OS setups.
This step is unnecessary when using USB, but UART is used here due to hardware requirements.

If Using the GUI:
Open the Start Menu → Preferences → Raspberry Pi Configuration.

Go to the Interfaces tab.

Enable Serial Port and disable Serial Console. 
