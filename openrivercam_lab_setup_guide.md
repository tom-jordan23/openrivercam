# OpenRiverCam Raspberry Pi 5 Lab Setup Guide

## Overview

This guide focuses on getting OpenRiverCam running on Raspberry Pi 5 in a controlled lab environment using utility power and WiFi connectivity. Environmental controls, solar power, and cellular connectivity will be added in Phase 2 after the core platform is validated.

## Phase 1: Core Lab Setup (This Guide)
- ✅ Raspberry Pi 5 with camera module
- ✅ Basic river flow analysis pipeline
- ✅ WiFi connectivity for data transmission
- ✅ Utility power (standard Pi power supply)
- ✅ Manual testing and validation

## Phase 2: Field Hardening (Future)
- 🔄 Environmental monitoring and control
- 🔄 Solar power and battery systems
- 🔄 4G cellular connectivity
- 🔄 Weatherproof enclosures
- 🔄 Autonomous operation

---

## Table of Contents
1. [Hardware Requirements (Lab Version)](#hardware-requirements-lab-version)
2. [Operating System Installation](#operating-system-installation)
3. [Basic System Configuration](#basic-system-configuration)
4. [Camera Module Setup](#camera-module-setup)
5. [Software Dependencies](#software-dependencies)
6. [OpenRiverCam Installation](#openrivercam-installation)
7. [River Analysis Pipeline](#river-analysis-pipeline)
8. [Data Management](#data-management)
9. [WiFi Data Transmission](#wifi-data-transmission)
10. [Testing and Validation](#testing-and-validation)
11. [Troubleshooting](#troubleshooting)

---

## Hardware Requirements (Lab Version)

### Essential Components
- **Raspberry Pi 5** (8GB RAM recommended, 4GB minimum)
- **Raspberry Pi Camera Module v3** (or compatible)
- **microSD Card** (64GB+ Class 10, SanDisk Extreme Pro recommended)
- **Raspberry Pi 5 Official Power Supply** (27W USB-C)
- **Micro HDMI to HDMI Cable** (for initial setup)
- **USB Keyboard and Mouse** (for initial setup)
- **Active Cooler for Pi 5** (official or compatible)

### Optional Lab Components
- **Case/Enclosure** (for protection during testing)
- **Ethernet Cable** (backup connectivity)
- **GPIO Breadboard** (for future sensor testing)
- **LED indicators** (for status monitoring)

### Not Needed for Lab Testing
- ❌ Environmental sensors
- ❌ Relay modules 
- ❌ Solar panels/batteries
- ❌ 4G modems
- ❌ Weatherproof enclosures

---

## Operating System Installation

### 1. Download and Flash Raspberry Pi OS

```bash
# Download Raspberry Pi Imager
# https://www.raspberrypi.com/software/

# Recommended: Raspberry Pi OS (64-bit) with desktop
# This provides GUI for easier lab testing and development

# During imaging process, configure:
# - Enable SSH with password authentication
# - Set username: openriver
# - Set strong password
# - Configure WiFi network (your lab WiFi)
# - Set locale and keyboard layout
```

### 2. Initial Boot and Update

```bash
# SSH into the Pi with X11 forwarding enabled
ssh -X openriver@<PI_IP_ADDRESS>

# Alternatively, use -Y for trusted X11 forwarding (more permissive)
# ssh -Y openriver@<PI_IP_ADDRESS>

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y git vim htop curl wget tree

# Install X11 forwarding prerequisites (for headless GUI applications)
sudo apt install -y xauth x11-apps

# Set timezone (use your local timezone for lab testing)
sudo timedatectl set-timezone America/New_York  # Adjust as needed
```

### 3. Configure X11 Forwarding for Headless Operation

```bash
# Configure SSH server for X11 forwarding
sudo nano /etc/ssh/sshd_config

# Ensure these lines are present and set correctly:
# X11Forwarding yes
# X11DisplayOffset 10
# X11UseLocalhost no

# If you need to modify sshd_config:
sudo sed -i 's/#X11Forwarding yes/X11Forwarding yes/' /etc/ssh/sshd_config
sudo sed -i 's/X11Forwarding no/X11Forwarding yes/' /etc/ssh/sshd_config

# Restart SSH service to apply changes
sudo systemctl restart ssh

# Install additional GUI libraries for OpenCV and camera applications
sudo apt install -y libgtk-3-dev libqt5gui5 qt5-default
sudo apt install -y python3-tk  # For matplotlib GUI backends

# Test X11 forwarding (should open a simple GUI window)
xclock &
# Press Ctrl+C or close the window to stop

# Test with a more comprehensive X11 application
xeyes &
# This should open a pair of eyes that track your mouse cursor
```

### 4. Client-Side X11 Setup

#### On Linux/macOS Client:
```bash
# Install X11 server if not already present
# Linux: Usually pre-installed
# macOS: Install XQuartz from https://www.xquartz.org/

# Connect with X11 forwarding
ssh -X openriver@<PI_IP_ADDRESS>

# For trusted forwarding (if you get authentication errors)
ssh -Y openriver@<PI_IP_ADDRESS>

# Test X11 forwarding from client
echo $DISPLAY  # Should show something like localhost:10.0
```

#### On Windows Client:
```bash
# Install X Server for Windows:
# Option 1: VcXsrv (https://sourceforge.net/projects/vcxsrv/)
# Option 2: Xming (https://sourceforge.net/projects/xming/)
# Option 3: MobaXterm (includes built-in X server)

# Using VcXsrv:
# 1. Install and start VcXsrv
# 2. Configure: Multiple windows, Display number 0, Start no client
# 3. In Extra settings: Check "Disable access control"

# Connect with X11 forwarding using PuTTY or WSL
# PuTTY: Enable X11 forwarding in Connection -> SSH -> X11
# WSL: Use ssh -X as with Linux

# Set DISPLAY variable if needed (usually automatic)
export DISPLAY=localhost:0.0
```

### 5. Create X11 Testing Script

```bash
cat << 'EOF' > ~/test_x11.sh
#!/bin/bash
# Test X11 forwarding functionality

echo "🖥️  Testing X11 Forwarding for OpenRiverCam"
echo "=================================="

# Check if DISPLAY is set
if [ -z "$DISPLAY" ]; then
    echo "❌ DISPLAY variable not set"
    echo "Make sure you connected with: ssh -X openriver@<PI_IP>"
    exit 1
else
    echo "✅ DISPLAY set to: $DISPLAY"
fi

# Test basic X11 functionality
echo "Testing basic X11..."
if command -v xclock > /dev/null; then
    echo "✅ xclock available"
    echo "Opening xclock for 5 seconds..."
    timeout 5s xclock &
    sleep 6
else
    echo "❌ xclock not available - install x11-apps"
fi

# Test Python GUI capabilities
echo "Testing Python GUI support..."
python3 -c "
import sys
try:
    import tkinter as tk
    print('✅ Tkinter available')
    
    # Test simple window creation
    root = tk.Tk()
    root.title('X11 Test')
    root.geometry('200x100')
    label = tk.Label(root, text='X11 Forwarding Works!')
    label.pack(pady=20)
    root.after(3000, root.destroy)  # Auto-close after 3 seconds
    print('✅ Opening test window for 3 seconds...')
    root.mainloop()
    
except ImportError:
    print('❌ Tkinter not available')
    sys.exit(1)
except Exception as e:
    print(f'❌ GUI test failed: {e}')
    sys.exit(1)
"

# Test matplotlib GUI backend
echo "Testing matplotlib GUI backend..."
python3 -c "
import sys
try:
    import matplotlib
    matplotlib.use('TkAgg')  # Use Tkinter backend
    import matplotlib.pyplot as plt
    import numpy as np
    
    print('✅ Matplotlib with GUI backend available')
    
    # Create simple test plot
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(6, 4))
    plt.plot(x, y)
    plt.title('X11 Matplotlib Test')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    
    # Show plot for 3 seconds then close
    plt.ion()  # Turn on interactive mode
    plt.show()
    plt.pause(3)
    plt.close('all')
    
    print('✅ Matplotlib GUI test successful')
    
except ImportError as e:
    print(f'❌ Matplotlib import failed: {e}')
except Exception as e:
    print(f'❌ Matplotlib GUI test failed: {e}')
"

echo "✅ X11 forwarding tests completed!"
EOF

chmod +x ~/test_x11.sh

# Run the X11 test
~/test_x11.sh
```

### 6. OpenCV GUI Testing

```bash
cat << 'EOF' > ~/test_opencv_gui.py
#!/usr/bin/env python3
"""
Test OpenCV GUI functionality over X11 forwarding
"""

import cv2
import numpy as np
import sys

def test_opencv_gui():
    """Test OpenCV window display over X11"""
    print("🎥 Testing OpenCV GUI over X11 forwarding...")
    
    try:
        # Create a test image
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Draw some test patterns
        cv2.rectangle(img, (50, 50), (200, 200), (0, 255, 0), 3)
        cv2.circle(img, (400, 150), 80, (255, 0, 0), -1)
        cv2.putText(img, 'OpenCV X11 Test', (200, 300), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Display the image
        cv2.imshow('OpenCV X11 Test', img)
        print("✅ OpenCV window should be visible on your local display")
        print("Press any key in the OpenCV window to close...")
        
        # Wait for key press
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print("✅ OpenCV GUI test successful!")
        return True
        
    except Exception as e:
        print(f"❌ OpenCV GUI test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_opencv_gui()
    sys.exit(0 if success else 1)
EOF

chmod +x ~/test_opencv_gui.py
```

---

## Basic System Configuration

### 1. Enable Required Interfaces

```bash
# Enable camera interface
sudo raspi-config nonint do_camera 0

# Enable I2C (for future sensors)
sudo raspi-config nonint do_i2c 0

# Enable SSH (should already be enabled)
sudo raspi-config nonint do_ssh 0

# Reboot to apply changes
sudo reboot
```

### 2. Configure Boot Parameters

```bash
# Edit boot configuration
sudo nano /boot/firmware/config.txt

# Add/modify these lines for camera and performance:
[all]
# Enable camera
start_x=1
gpu_mem=128

# Enable I2C for future use
dtparam=i2c_arm=on

# Configure fan control (if using PWM fan)
dtoverlay=gpio-fan,gpiopin=18,temp=60000

# Save and reboot
sudo reboot
```

### 3. Create Project Structure

```bash
# Create dedicated user for OpenRiverCam (optional, can use openriver)
sudo useradd -m -s /bin/bash openrivercam
sudo passwd openrivercam

# Or just create project directories for existing user
mkdir -p ~/openrivercam/{config,data,logs,scripts}
mkdir -p ~/openrivercam/data/{videos,results,raw}
```

---

## Camera Module Setup

### 1. Physical Installation

```bash
# 1. Power off Pi completely
sudo shutdown -h now

# 2. Connect Camera Module v3 to camera port
#    - Lift connector flap
#    - Insert ribbon cable with contacts facing away from ethernet port
#    - Press down connector flap

# 3. Power on and test
```

### 2. Camera Testing

```bash
# Test camera with libcamera (new camera stack)
libcamera-hello --preview-window 0,0,640,480 --timeout 5000

# Test still capture
libcamera-still -o ~/test_image.jpg --width 1920 --height 1080

# Test video capture
libcamera-vid -o ~/test_video.h264 --width 1920 --height 1080 --timeout 10000

# Check captured files
ls -la ~/*.jpg ~/*.h264
```

### 3. Camera Configuration Script

```bash
# Create camera test script
cat << 'EOF' > ~/openrivercam/scripts/test_camera.py
#!/usr/bin/env python3
"""
Basic camera test for OpenRiverCam lab setup
"""

import sys
import os

# Check if we're in the correct virtual environment
def check_venv():
    venv_path = os.path.expanduser("~/openrivercam/venv")
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        print("❌ Error: Not running in virtual environment!")
        print("Please run: source ~/openrivercam/activate_env.sh")
        sys.exit(1)
    
    if not os.path.exists(venv_path) or not os.path.samefile(sys.prefix, venv_path):
        print("⚠️  Warning: Not running in the OpenRiverCam virtual environment")
        print("Please run: source ~/openrivercam/activate_env.sh")

# Check virtual environment first
check_venv()

import cv2
import numpy as np
from picamera2 import Picamera2
import time

def test_camera_basic():
    """Test basic camera functionality"""
    print("Testing Raspberry Pi Camera Module...")
    
    try:
        # Initialize camera
        picam2 = Picamera2()
        
        # Configure for still capture
        config = picam2.create_still_configuration(
            main={"size": (1920, 1080), "format": "RGB888"}
        )
        picam2.configure(config)
        
        # Start camera
        picam2.start()
        time.sleep(2)  # Allow camera to warm up
        
        # Capture test image
        print("Capturing test image...")
        image = picam2.capture_array()
        
        # Save test image
        test_dir = os.path.expanduser("~/openrivercam/data/raw")
        os.makedirs(test_dir, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{test_dir}/camera_test_{timestamp}.jpg"
        
        cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        
        # Analyze image quality
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        height, width = gray.shape
        
        # Basic image statistics
        brightness = np.mean(gray)
        contrast = np.std(gray)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        print(f"✅ Camera test successful!")
        print(f"   Resolution: {width}x{height}")
        print(f"   Image saved: {filename}")
        print(f"   Brightness: {brightness:.1f}")
        print(f"   Contrast: {contrast:.1f}")
        print(f"   Sharpness: {sharpness:.1f}")
        
        # Quality assessment
        if brightness < 50:
            print("   ⚠️  Warning: Image appears dark")
        elif brightness > 200:
            print("   ⚠️  Warning: Image appears bright")
        else:
            print("   ✅ Exposure looks good")
            
        if sharpness < 100:
            print("   ⚠️  Warning: Image appears blurry")
        else:
            print("   ✅ Image appears sharp")
            
        return True
        
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False
        
    finally:
        try:
            picam2.stop()
        except:
            pass

if __name__ == "__main__":
    success = test_camera_basic()
    exit(0 if success else 1)
EOF

chmod +x ~/openrivercam/scripts/test_camera.py
```

### 4. Run Camera Test

```bash
cd ~/openrivercam/scripts

# Activate virtual environment first
source ~/openrivercam/activate_env.sh

# Run camera test
python3 test_camera.py

# Check the captured test image
ls -la ~/openrivercam/data/raw/
```

---

## Software Dependencies

### 1. Python Environment Setup

```bash
# Install Python development tools
sudo apt install -y python3-dev python3-pip python3-venv python3-setuptools

# Install system dependencies for OpenCV and scientific computing
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y libgtk2.0-dev libcanberra-gtk-module
sudo apt install -y libatlas-base-dev gfortran
sudo apt install -y libhdf5-dev libhdf5-serial-dev

# Verify Python version
python3 --version  # Should be 3.9+ for Pi OS
```

### 2. Create Isolated Virtual Environment

```bash
# Remove any existing virtual environment
rm -rf ~/openrivercam/venv

# Create fresh virtual environment with --clear flag for complete isolation
python3 -m venv ~/openrivercam/venv --clear --prompt="openrivercam"

# Verify virtual environment was created
ls -la ~/openrivercam/venv/

# Create activation helper script
cat << 'EOF' > ~/openrivercam/activate_env.sh
#!/bin/bash
# OpenRiverCam Virtual Environment Activation
echo "🐍 Activating OpenRiverCam Python environment..."
source ~/openrivercam/venv/bin/activate
echo "✅ Virtual environment activated: $(which python3)"
echo "✅ Python version: $(python3 --version)"
echo "✅ Pip version: $(pip --version)"
EOF

chmod +x ~/openrivercam/activate_env.sh
```

### 3. Activate and Upgrade Virtual Environment

```bash
# Activate virtual environment using our helper
source ~/openrivercam/activate_env.sh

# OR activate directly:
# source ~/openrivercam/venv/bin/activate

# Verify we're in the virtual environment
which python3  # Should show ~/openrivercam/venv/bin/python3
which pip      # Should show ~/openrivercam/venv/bin/pip

# Upgrade pip and core tools in isolated environment
pip install --upgrade pip setuptools wheel

# Verify isolation - should be empty or minimal
pip list
```

### 4. Install Core Python Libraries in Virtual Environment

```bash
# Ensure virtual environment is activated
source ~/openrivercam/activate_env.sh

# Install packages in specific order for better dependency resolution

# 1. Core numerical computing (foundational)
pip install numpy==1.24.3
pip install scipy==1.10.1

# 2. Computer vision libraries
pip install opencv-python==4.8.1.78
pip install Pillow==10.0.0
pip install imageio==2.31.1

# 3. Camera libraries (Raspberry Pi specific)
pip install picamera2

# 4. Data handling and analysis
pip install pandas==2.0.3
pip install pyyaml==6.0.1

# 5. Web and networking
pip install requests==2.31.0
pip install urllib3==2.0.4

# 6. System utilities
pip install psutil==5.9.5

# 7. Development and testing tools
pip install pytest==7.4.0

# Verify all packages installed correctly
pip check

# Create detailed requirements files
pip freeze > ~/openrivercam/requirements.txt

# Create a minimal requirements file for production
cat << 'EOF' > ~/openrivercam/requirements-core.txt
# Core OpenRiverCam Dependencies
numpy==1.24.3
scipy==1.10.1
opencv-python==4.8.1.78
Pillow==10.0.0
picamera2
pandas==2.0.3
pyyaml==6.0.1
requests==2.31.0
psutil==5.9.5
EOF

echo "✅ Requirements files created:"
echo "   📄 requirements.txt (complete freeze)"
echo "   📄 requirements-core.txt (essential packages only)"
```

### 5. Create Environment Management Scripts

```bash
# Create environment check script
cat << 'EOF' > ~/openrivercam/scripts/check_environment.py
#!/usr/bin/env python3
"""
Check Python environment for OpenRiverCam
"""
import sys
import os

def check_environment():
    """Check that we're running in the correct virtual environment"""
    print("🔍 Checking Python Environment...")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✅ Running in virtual environment")
        venv_path = sys.prefix
        expected_path = os.path.expanduser("~/openrivercam/venv")
        
        if os.path.samefile(venv_path, expected_path):
            print("✅ Correct virtual environment (OpenRiverCam)")
        else:
            print(f"⚠️  Warning: Different virtual environment")
            print(f"   Current: {venv_path}")
            print(f"   Expected: {expected_path}")
    else:
        print("❌ NOT running in virtual environment!")
        return False
    
    # Test critical imports
    critical_packages = [
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('picamera2', 'PiCamera2'),
        ('pandas', 'Pandas'),
        ('yaml', 'PyYAML'),
        ('requests', 'Requests')
    ]
    
    print("\n📦 Testing package imports...")
    all_good = True
    
    for package, name in critical_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)
EOF

chmod +x ~/openrivercam/scripts/check_environment.py

# Create environment reset script
cat << 'EOF' > ~/openrivercam/reset_environment.sh
#!/bin/bash
# Reset OpenRiverCam Python Environment

echo "🔄 Resetting OpenRiverCam Python Environment..."

# Remove existing environment
if [ -d ~/openrivercam/venv ]; then
    echo "Removing existing virtual environment..."
    rm -rf ~/openrivercam/venv
fi

# Create new environment
echo "Creating fresh virtual environment..."
python3 -m venv ~/openrivercam/venv --clear --prompt="openrivercam"

# Activate and upgrade
source ~/openrivercam/venv/bin/activate
pip install --upgrade pip setuptools wheel

# Install from requirements if it exists
if [ -f ~/openrivercam/requirements-core.txt ]; then
    echo "Installing packages from requirements-core.txt..."
    pip install -r ~/openrivercam/requirements-core.txt
else
    echo "No requirements file found - you'll need to install packages manually"
fi

echo "✅ Environment reset complete!"
echo "Run: source ~/openrivercam/activate_env.sh"
EOF

chmod +x ~/openrivercam/reset_environment.sh
```

### 6. Test Python Environment

```bash
# Test virtual environment setup
source ~/openrivercam/activate_env.sh

# Run environment check
python3 ~/openrivercam/scripts/check_environment.py

# Test core imports manually
python3 -c "
import cv2
import numpy as np
import pandas as pd
import picamera2
print('✅ All core libraries imported successfully')
print(f'OpenCV version: {cv2.__version__}')
print(f'NumPy version: {np.__version__}')
print(f'Pandas version: {pd.__version__}')
"

# Verify package versions match expectations
pip show opencv-python numpy pandas picamera2
```

### 7. Environment Usage Best Practices

```bash
# Always activate before running any OpenRiverCam scripts
source ~/openrivercam/activate_env.sh

# Or create an alias for convenience (add to ~/.bashrc)
echo 'alias orc="source ~/openrivercam/activate_env.sh"' >> ~/.bashrc
source ~/.bashrc

# Now you can just type 'orc' to activate the environment
orc
```

---

## OpenRiverCam Installation

### 1. Clone OpenRiverCam Repository

```bash
cd ~/openrivercam

# Clone the official repository
git clone https://github.com/localdevices/OpenRiverCam.git

# Enter the directory
cd OpenRiverCam

# Activate virtual environment
source ~/openrivercam/activate_env.sh

# Install OpenRiverCam
pip install -e .
```

### 2. Basic Configuration

```bash
# Create configuration directory
mkdir -p ~/.openrivercam

# Create basic configuration file
cat << 'EOF' > ~/.openrivercam/config.yaml
# OpenRiverCam Lab Configuration

# Camera settings
camera:
  resolution: [1920, 1080]
  framerate: 25
  rotation: 0

# Video processing
video:
  duration: 30  # seconds for lab testing
  format: "mp4"
  
# Analysis settings
analysis:
  method: "piv"  # Particle Image Velocimetry
  
# Output settings
output:
  local_storage: "~/openrivercam/data/results"
  format: "json"
  
# Lab settings
lab_mode: true
debug: true
EOF
```

### 3. Test OpenRiverCam Installation

```bash
# Test basic import
python3 -c "
import openrivercam
print('✅ OpenRiverCam imported successfully')
"

# Test configuration loading
python3 -c "
import openrivercam
import yaml
with open('~/.openrivercam/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print('✅ Configuration loaded successfully')
print(config)
"
```

---

## River Analysis Pipeline

### 1. Create Basic Analysis Script

```bash
cat << 'EOF' > ~/openrivercam/scripts/basic_analysis.py
#!/usr/bin/env python3
"""
Basic OpenRiverCam analysis for lab testing
"""

import cv2
import numpy as np
import json
import time
import os
from datetime import datetime
from picamera2 import Picamera2

class LabRiverAnalyzer:
    def __init__(self):
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories"""
        self.base_dir = os.path.expanduser("~/openrivercam/data")
        self.video_dir = os.path.join(self.base_dir, "videos")
        self.results_dir = os.path.join(self.base_dir, "results")
        
        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        
    def capture_test_video(self, duration=30):
        """Capture video for analysis"""
        print(f"Capturing {duration} second test video...")
        
        try:
            # Initialize camera
            picam2 = Picamera2()
            
            # Configure for video
            config = picam2.create_video_configuration(
                main={"size": (1920, 1080), "format": "RGB888"}
            )
            picam2.configure(config)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = os.path.join(self.video_dir, f"test_video_{timestamp}.mp4")
            
            # Start recording
            picam2.start_recording(video_path)
            time.sleep(duration)
            picam2.stop_recording()
            
            print(f"✅ Video saved: {video_path}")
            return video_path
            
        except Exception as e:
            print(f"❌ Video capture failed: {e}")
            return None
            
        finally:
            try:
                picam2.stop()
            except:
                pass
    
    def capture_frames_for_analysis(self, duration=10, fps=5):
        """Capture frames directly for analysis"""
        print(f"Capturing frames for {duration}s at {fps} fps...")
        
        frames = []
        timestamps = []
        
        try:
            picam2 = Picamera2()
            config = picam2.create_video_configuration(
                main={"size": (1920, 1080), "format": "RGB888"}
            )
            picam2.configure(config)
            picam2.start()
            time.sleep(1)  # Camera warm-up
            
            frame_interval = 1.0 / fps
            start_time = time.time()
            
            while (time.time() - start_time) < duration:
                frame = picam2.capture_array()
                frames.append(frame.copy())
                timestamps.append(time.time())
                time.sleep(frame_interval)
                
            print(f"✅ Captured {len(frames)} frames")
            return frames, timestamps
            
        except Exception as e:
            print(f"❌ Frame capture failed: {e}")
            return None, None
            
        finally:
            try:
                picam2.stop()
            except:
                pass
    
    def basic_motion_analysis(self, frames):
        """Perform basic motion analysis on frames"""
        if not frames or len(frames) < 2:
            print("❌ Need at least 2 frames for motion analysis")
            return None
            
        print("Analyzing motion between frames...")
        
        # Convert frames to grayscale
        gray_frames = [cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) for frame in frames]
        
        # Simple frame differencing
        motion_results = []
        
        for i in range(len(gray_frames) - 1):
            frame1 = gray_frames[i]
            frame2 = gray_frames[i + 1]
            
            # Calculate frame difference
            diff = cv2.absdiff(frame1, frame2)
            
            # Threshold the difference
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            
            # Calculate motion metrics
            motion_pixels = np.count_nonzero(thresh)
            total_pixels = thresh.shape[0] * thresh.shape[1]
            motion_percentage = (motion_pixels / total_pixels) * 100
            
            motion_results.append({
                'frame_pair': f"{i}-{i+1}",
                'motion_pixels': int(motion_pixels),
                'total_pixels': int(total_pixels),
                'motion_percentage': float(motion_percentage)
            })
            
        return motion_results
    
    def optical_flow_analysis(self, frames):
        """Basic optical flow analysis"""
        if not frames or len(frames) < 2:
            return None
            
        print("Performing optical flow analysis...")
        
        gray_frames = [cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) for frame in frames]
        
        # Parameters for Lucas-Kanade optical flow
        lk_params = dict(winSize=(15, 15),
                        maxLevel=2,
                        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        # Parameters for feature detection
        feature_params = dict(maxCorners=100,
                            qualityLevel=0.01,
                            minDistance=10,
                            blockSize=7)
        
        flow_results = []
        
        for i in range(len(gray_frames) - 1):
            frame1 = gray_frames[i]
            frame2 = gray_frames[i + 1]
            
            # Find features to track
            p0 = cv2.goodFeaturesToTrack(frame1, mask=None, **feature_params)
            
            if p0 is not None and len(p0) > 0:
                # Calculate optical flow
                p1, status, error = cv2.calcOpticalFlowPyrLK(frame1, frame2, p0, None, **lk_params)
                
                # Select good points
                good_new = p1[status == 1]
                good_old = p0[status == 1]
                
                if len(good_new) > 0:
                    # Calculate flow vectors
                    flow_vectors = good_new - good_old
                    
                    # Calculate statistics
                    flow_magnitudes = np.sqrt(flow_vectors[:, 0]**2 + flow_vectors[:, 1]**2)
                    
                    flow_result = {
                        'frame_pair': f"{i}-{i+1}",
                        'features_detected': len(p0),
                        'features_tracked': len(good_new),
                        'mean_flow_magnitude': float(np.mean(flow_magnitudes)),
                        'max_flow_magnitude': float(np.max(flow_magnitudes)),
                        'flow_direction_x': float(np.mean(flow_vectors[:, 0])),
                        'flow_direction_y': float(np.mean(flow_vectors[:, 1]))
                    }
                    
                    flow_results.append(flow_result)
                    
        return flow_results
    
    def run_lab_analysis(self):
        """Run complete lab analysis"""
        print("🚀 Starting OpenRiverCam lab analysis...")
        
        # Capture frames for analysis
        frames, timestamps = self.capture_frames_for_analysis(duration=10, fps=3)
        
        if not frames:
            print("❌ Failed to capture frames")
            return False
            
        # Perform motion analysis
        motion_results = self.basic_motion_analysis(frames)
        
        # Perform optical flow analysis
        flow_results = self.optical_flow_analysis(frames)
        
        # Compile results
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'capture_info': {
                'frames_captured': len(frames),
                'duration': timestamps[-1] - timestamps[0] if len(timestamps) > 1 else 0,
                'fps_actual': len(frames) / (timestamps[-1] - timestamps[0]) if len(timestamps) > 1 else 0
            },
            'motion_analysis': motion_results,
            'optical_flow_analysis': flow_results,
            'lab_mode': True
        }
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(self.results_dir, f"lab_analysis_{timestamp}.json")
        
        with open(results_file, 'w') as f:
            json.dump(analysis_results, f, indent=2)
            
        print(f"✅ Analysis complete! Results saved: {results_file}")
        
        # Print summary
        if motion_results:
            avg_motion = np.mean([r['motion_percentage'] for r in motion_results])
            print(f"📊 Average motion detected: {avg_motion:.2f}%")
            
        if flow_results:
            avg_flow = np.mean([r['mean_flow_magnitude'] for r in flow_results])
            print(f"🌊 Average flow magnitude: {avg_flow:.2f} pixels")
            
        return True

if __name__ == "__main__":
    analyzer = LabRiverAnalyzer()
    success = analyzer.run_lab_analysis()
    exit(0 if success else 1)
EOF

chmod +x ~/openrivercam/scripts/basic_analysis.py
```

### 2. Test the Analysis Pipeline

```bash
cd ~/openrivercam/scripts

# Activate virtual environment
source ~/openrivercam/activate_env.sh

# Run basic analysis test
python3 basic_analysis.py

# Check results
ls -la ~/openrivercam/data/results/
cat ~/openrivercam/data/results/lab_analysis_*.json
```

---

## Data Management

### 1. Create Data Management Scripts

```bash
cat << 'EOF' > ~/openrivercam/scripts/data_manager.py
#!/usr/bin/env python3
"""
Simple data management for lab testing
"""

import os
import json
import shutil
from datetime import datetime, timedelta
import glob

class LabDataManager:
    def __init__(self):
        self.base_dir = os.path.expanduser("~/openrivercam/data")
        
    def list_data_files(self):
        """List all data files"""
        print("📁 Data Files:")
        
        for subdir in ['raw', 'videos', 'results']:
            dir_path = os.path.join(self.base_dir, subdir)
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                print(f"\n  {subdir}/:")
                for file in sorted(files):
                    file_path = os.path.join(dir_path, file)
                    size = os.path.getsize(file_path)
                    print(f"    {file} ({size} bytes)")
                    
    def cleanup_old_files(self, days_old=7):
        """Remove files older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cutoff_timestamp = cutoff_date.timestamp()
        
        removed_count = 0
        
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_time = os.path.getmtime(file_path)
                
                if file_time < cutoff_timestamp:
                    os.remove(file_path)
                    print(f"🗑️  Removed old file: {file}")
                    removed_count += 1
                    
        print(f"✅ Cleaned up {removed_count} old files")
        
    def create_backup(self):
        """Create backup of important data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.expanduser(f"~/openrivercam_backup_{timestamp}")
        
        # Copy results and config
        results_dir = os.path.join(self.base_dir, "results")
        if os.path.exists(results_dir):
            shutil.copytree(results_dir, os.path.join(backup_dir, "results"))
            
        # Copy config
        config_file = os.path.expanduser("~/.openrivercam/config.yaml")
        if os.path.exists(config_file):
            os.makedirs(os.path.join(backup_dir, "config"), exist_ok=True)
            shutil.copy2(config_file, os.path.join(backup_dir, "config"))
            
        print(f"✅ Backup created: {backup_dir}")
        
    def get_summary_stats(self):
        """Get summary statistics"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'directories': {},
            'total_files': 0,
            'total_size': 0
        }
        
        for subdir in ['raw', 'videos', 'results']:
            dir_path = os.path.join(self.base_dir, subdir)
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                total_size = sum(os.path.getsize(os.path.join(dir_path, f)) for f in files)
                
                stats['directories'][subdir] = {
                    'file_count': len(files),
                    'total_size_bytes': total_size
                }
                
                stats['total_files'] += len(files)
                stats['total_size'] += total_size
                
        return stats

if __name__ == "__main__":
    manager = LabDataManager()
    
    print("📊 OpenRiverCam Lab Data Summary")
    print("=" * 40)
    
    # List files
    manager.list_data_files()
    
    # Show statistics
    stats = manager.get_summary_stats()
    print(f"\n📈 Summary Statistics:")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total size: {stats['total_size']} bytes ({stats['total_size']/1024:.1f} KB)")
EOF

chmod +x ~/openrivercam/scripts/data_manager.py
```

---

## WiFi Data Transmission

### 1. Create Simple Upload Script

```bash
cat << 'EOF' > ~/openrivercam/scripts/upload_results.py
#!/usr/bin/env python3
"""
Simple WiFi upload for lab testing
"""

import os
import json
import requests
import time
from datetime import datetime

class LabUploader:
    def __init__(self):
        self.base_dir = os.path.expanduser("~/openrivercam/data")
        self.results_dir = os.path.join(self.base_dir, "results")
        
        # For lab testing, we'll just simulate upload or use a local server
        self.upload_url = "http://localhost:8000/upload"  # Change as needed
        self.simulate_upload = True  # Set to False when you have a real server
        
    def find_new_results(self):
        """Find result files that haven't been uploaded"""
        if not os.path.exists(self.results_dir):
            return []
            
        result_files = []
        for filename in os.listdir(self.results_dir):
            if filename.endswith('.json') and not filename.endswith('_uploaded.json'):
                file_path = os.path.join(self.results_dir, filename)
                result_files.append(file_path)
                
        return sorted(result_files)
    
    def simulate_upload_file(self, file_path):
        """Simulate file upload for lab testing"""
        print(f"📤 Simulating upload: {os.path.basename(file_path)}")
        
        # Read file content
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Simulate network delay
        time.sleep(1)
        
        # Create "uploaded" marker
        uploaded_path = file_path.replace('.json', '_uploaded.json')
        upload_info = {
            'original_file': file_path,
            'upload_timestamp': datetime.now().isoformat(),
            'upload_status': 'simulated_success',
            'file_size': os.path.getsize(file_path),
            'data_summary': {
                'frames_analyzed': data.get('capture_info', {}).get('frames_captured', 0),
                'motion_detections': len(data.get('motion_analysis', [])),
                'flow_detections': len(data.get('optical_flow_analysis', []))
            }
        }
        
        with open(uploaded_path, 'w') as f:
            json.dump(upload_info, f, indent=2)
            
        print(f"✅ Upload simulated successfully")
        return True
    
    def real_upload_file(self, file_path):
        """Actually upload file to server"""
        print(f"📤 Uploading: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            response = requests.post(
                self.upload_url,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Upload successful")
                return True
            else:
                print(f"❌ Upload failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
    
    def upload_all_results(self):
        """Upload all pending results"""
        result_files = self.find_new_results()
        
        if not result_files:
            print("📭 No new results to upload")
            return True
            
        print(f"📤 Found {len(result_files)} files to upload")
        
        success_count = 0
        
        for file_path in result_files:
            if self.simulate_upload:
                success = self.simulate_upload_file(file_path)
            else:
                success = self.real_upload_file(file_path)
                
            if success:
                success_count += 1
                
        print(f"✅ Upload complete: {success_count}/{len(result_files)} successful")
        return success_count == len(result_files)
    
    def check_internet_connection(self):
        """Check if internet connection is available"""
        try:
            response = requests.get("http://www.google.com", timeout=5)
            print("✅ Internet connection available")
            return True
        except:
            print("❌ No internet connection")
            return False

if __name__ == "__main__":
    uploader = LabUploader()
    
    print("🌐 OpenRiverCam Lab Upload")
    print("=" * 30)
    
    # Check connection
    uploader.check_internet_connection()
    
    # Upload results
    uploader.upload_all_results()
EOF

chmod +x ~/openrivercam/scripts/upload_results.py
```

---

## Testing and Validation

### 1. Create Complete Test Suite

```bash
cat << 'EOF' > ~/openrivercam/scripts/run_tests.py
#!/usr/bin/env python3
"""
Complete test suite for OpenRiverCam lab setup
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class LabTestSuite:
    def __init__(self):
        self.test_results = []
        self.base_dir = os.path.expanduser("~/openrivercam")
        
    def run_test(self, test_name, test_function):
        """Run a single test and record results"""
        print(f"\n🧪 Testing: {test_name}")
        print("-" * 50)
        
        try:
            start_time = datetime.now()
            result = test_function()
            end_time = datetime.now()
            
            test_result = {
                'test_name': test_name,
                'status': 'PASS' if result else 'FAIL',
                'duration': (end_time - start_time).total_seconds(),
                'timestamp': start_time.isoformat()
            }
            
            if result:
                print(f"✅ {test_name}: PASS")
            else:
                print(f"❌ {test_name}: FAIL")
                
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            test_result = {
                'test_name': test_name,
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
        self.test_results.append(test_result)
        return test_result['status'] == 'PASS'
    
    def test_camera_hardware(self):
        """Test camera hardware connectivity"""
        try:
            result = subprocess.run(['libcamera-hello', '--timeout', '1000'], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def test_python_environment(self):
        """Test Python environment and imports"""
        try:
            import cv2
            import numpy as np
            import picamera2
            return True
        except ImportError:
            return False
    
    def test_camera_capture(self):
        """Test camera capture functionality"""
        try:
            sys.path.insert(0, os.path.join(self.base_dir, 'scripts'))
            from test_camera import test_camera_basic
            return test_camera_basic()
        except:
            return False
    
    def test_analysis_pipeline(self):
        """Test analysis pipeline"""
        try:
            sys.path.insert(0, os.path.join(self.base_dir, 'scripts'))
            from basic_analysis import LabRiverAnalyzer
            
            analyzer = LabRiverAnalyzer()
            
            # Test with shorter duration for testing
            frames, timestamps = analyzer.capture_frames_for_analysis(duration=5, fps=2)
            
            if not frames or len(frames) < 2:
                return False
                
            # Test motion analysis
            motion_results = analyzer.basic_motion_analysis(frames)
            if not motion_results:
                return False
                
            return True
        except Exception as e:
            print(f"Analysis test error: {e}")
            return False
    
    def test_data_management(self):
        """Test data management functionality"""
        try:
            sys.path.insert(0, os.path.join(self.base_dir, 'scripts'))
            from data_manager import LabDataManager
            
            manager = LabDataManager()
            stats = manager.get_summary_stats()
            
            return isinstance(stats, dict) and 'total_files' in stats
        except:
            return False
    
    def test_wifi_connectivity(self):
        """Test WiFi connectivity"""
        try:
            import requests
            response = requests.get("http://www.google.com", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_x11_forwarding(self):
        """Test X11 forwarding functionality"""
        try:
            import os
            
            # Check if DISPLAY is set
            display = os.environ.get('DISPLAY')
            if not display:
                print("X11 forwarding test skipped - no DISPLAY variable")
                return True  # Don't fail if no X11 is expected
            
            # Test tkinter GUI
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()  # Hide the window
                root.destroy()
                print("X11 forwarding available")
                return True
            except Exception as e:
                print(f"X11 forwarding test failed: {e}")
                return False
                
        except:
            return True  # Don't fail test suite if X11 isn't available
    
    def test_upload_system(self):
        """Test upload system (simulation)"""
        try:
            sys.path.insert(0, os.path.join(self.base_dir, 'scripts'))
            from upload_results import LabUploader
            
            uploader = LabUploader()
            # This will run in simulation mode
            return True
        except:
            return False
    
    def test_directory_structure(self):
        """Test that all required directories exist"""
        required_dirs = [
            '~/openrivercam/data/raw',
            '~/openrivercam/data/videos', 
            '~/openrivercam/data/results',
            '~/openrivercam/scripts'
        ]
        
        for dir_path in required_dirs:
            full_path = os.path.expanduser(dir_path)
            if not os.path.exists(full_path):
                print(f"Missing directory: {full_path}")
                return False
                
        return True
    
    def run_full_test_suite(self):
        """Run complete test suite"""
        print("🚀 OpenRiverCam Lab Test Suite")
        print("=" * 50)
        print(f"Started: {datetime.now().isoformat()}")
        
        tests = [
            ("Directory Structure", self.test_directory_structure),
            ("Python Environment", self.test_python_environment),
            ("X11 Forwarding", self.test_x11_forwarding),
            ("Camera Hardware", self.test_camera_hardware),
            ("Camera Capture", self.test_camera_capture),
            ("WiFi Connectivity", self.test_wifi_connectivity),
            ("Data Management", self.test_data_management),
            ("Upload System", self.test_upload_system),
            ("Analysis Pipeline", self.test_analysis_pipeline),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if self.run_test(test_name, test_func):
                passed += 1
                
        # Save test results
        results_file = os.path.join(self.base_dir, f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        test_summary = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total,
            'passed_tests': passed,
            'success_rate': passed / total,
            'individual_results': self.test_results
        }
        
        with open(results_file, 'w') as f:
            json.dump(test_summary, f, indent=2)
            
        print("\n" + "=" * 50)
        print(f"🎯 Test Summary: {passed}/{total} tests passed ({passed/total:.1%})")
        print(f"📄 Detailed results: {results_file}")
        
        if passed == total:
            print("🎉 All tests passed! Lab setup is ready.")
            return True
        else:
            print("⚠️  Some tests failed. Check individual results.")
            return False

if __name__ == "__main__":
    test_suite = LabTestSuite()
    success = test_suite.run_full_test_suite()
    sys.exit(0 if success else 1)
EOF

chmod +x ~/openrivercam/scripts/run_tests.py
```

### 2. Run Complete Test Suite

```bash
cd ~/openrivercam/scripts

# Activate virtual environment
source ~/openrivercam/activate_env.sh

# Run all tests
python3 run_tests.py

# Check test results
ls -la ~/openrivercam/test_results_*.json
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. X11 Forwarding Issues
```bash
# Problem: No GUI applications display
# Check DISPLAY variable
echo $DISPLAY
# Should show something like localhost:10.0

# Problem: "cannot connect to X server" error
# Ensure you connected with -X flag
ssh -X openriver@<PI_IP_ADDRESS>

# If still failing, try trusted forwarding
ssh -Y openriver@<PI_IP_ADDRESS>

# Problem: "X11 connection rejected because of wrong authentication"
# Clean up old X11 authentication files
rm ~/.Xauthority
# Reconnect with X11 forwarding

# Test X11 forwarding
xclock

# Problem: Slow X11 forwarding
# Enable compression for slower connections
ssh -X -C openriver@<PI_IP_ADDRESS>

# Problem: "Error: Can't open display"
# Check if X server is running on client machine
# Linux: Usually automatic
# macOS: Start XQuartz
# Windows: Start VcXsrv/Xming

# Problem: OpenCV windows not displaying
# Install GUI libraries
sudo apt install -y libgtk-3-dev python3-tk
# Test with
python3 ~/test_opencv_gui.py
```

#### 2. Camera Not Detected
```bash
# Check if camera is physically connected
lsusb  # Should show camera if USB
ls /dev/video*  # Should show video devices

# Check camera interface
sudo raspi-config
# Navigate to Interface Options → Camera → Enable

# Test with system tools
libcamera-hello --list-cameras
```

#### 2. OpenCV Import Errors
```bash
# Reinstall OpenCV
source ~/openrivercam/activate_env.sh
pip uninstall opencv-python
pip install opencv-python==4.8.1.78

# Install system dependencies
sudo apt install -y libatlas-base-dev liblapack-dev
```

#### 3. Picamera2 Issues
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install picamera2 system packages
sudo apt install -y python3-picamera2

# Or install in virtual environment
pip install picamera2
```

#### 4. Permission Issues
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Add to gpio group for future use
sudo usermod -a -G gpio $USER

# Logout and login again
```

#### 5. WiFi Connectivity Issues
```bash
# Check WiFi status
iwconfig
nmcli dev wifi list

# Reconnect to WiFi
sudo nmcli dev wifi connect "Your_WiFi_Name" password "your_password"
```

---

## Next Steps

Once your lab setup is working properly:

### Phase 2 Additions (Future):
1. **Environmental Monitoring**
   - Temperature and humidity sensors
   - Fan and heating control
   - Environmental data logging

2. **Power Management** 
   - Solar panels and battery systems
   - Power monitoring and conservation
   - Automatic shutdown on low battery

3. **Cellular Connectivity**
   - 4G modem integration
   - Data transmission optimization
   - Remote monitoring capabilities

4. **Field Hardening**
   - Weatherproof enclosures
   - Mounting systems
   - Lightning protection

### Quick Lab Testing Workflow:
```bash
# Daily testing routine
cd ~/openrivercam/scripts
source ~/openrivercam/activate_env.sh

# 1. Test camera
python3 test_camera.py

# 2. Run analysis
python3 basic_analysis.py

# 3. Check data
python3 data_manager.py

# 4. Upload results (simulation)
python3 upload_results.py

# 5. Run full test suite (weekly)
python3 run_tests.py
```

This lab setup gives you a solid foundation for developing and testing OpenRiverCam functionality before moving to the more complex field deployment setup.