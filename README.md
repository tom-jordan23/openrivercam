# OpenRiverCam Lab Setup

Documentation spot for my notes setting up NodeORC on a Raspberry Pi with solar and IR integration for unattended day and night river observations.

## Tom's realizations
 - I need to have a place to send the data, so I need a LiveOpenRiverCam setup somewhere

## Pi Setup

- Raspberry PI 5 8GB
- Heat sink and PWM fan
- RTC battery

## OS Setup
- Bookworm Lite (no GUI environment), running headless
- Configuration via SSH
- TODO: add instructions for cloning repo onto device
- configure shell to autorun `source ~/orc/venv/bin/activate` on login

### System packages (install with sudo apt install):

  libcamera-apps
  python3-libcamera
  python3-kms++
  python3-pip
  python3-venv
  python3-dev
  libcap-dev

### requirements_camera.txt:

  picamera2>=0.3.12
  opencv-python>=4.5.0
  numpy>=1.21.0
  pillow>=8.0.0

### Hardware setup commands:
  # Enable camera and I2C
  sudo raspi-config nonint do_camera 0
  sudo raspi-config nonint do_i2c 0

### # Set GPU memory to 128MB
  echo 'gpu_mem=128' | sudo tee -a /boot/firmware/config.txt

### Reboot required after hardware changes
  sudo reboot


## Installation Notes

1. Update OS
2. Using a base directory of $HOME/orc
3. Activate the camera using `sudo raspi-config nonint do_camera 0`
4. Restart using `sudo reboot` or `sudo init 6`
5. Verify environment using `test_environment.py`
6. Verify camera using `test_camera.py`
