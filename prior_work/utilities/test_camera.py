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

import time
import subprocess

# Import libraries with error handling
try:
    import cv2
    import numpy as np
    from picamera2 import Picamera2
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some dependencies not available: {e}")
    print("This is normal if camera test is run before OpenCV installation")
    DEPENDENCIES_AVAILABLE = False

def test_camera_basic():
    """Test basic camera functionality"""
    print("Testing Raspberry Pi Camera Module...")
    
    # First check if camera is detected using rpicam tools
    try:
        result = subprocess.run(['rpicam-hello', '--list-cameras'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("📷 Camera detection via rpicam-hello:")
            print(result.stdout)
        else:
            print("❌ rpicam-hello failed to detect cameras")
            return False
    except Exception as e:
        print(f"❌ Failed to run rpicam-hello: {e}")
        return False
    
    # Check if Python dependencies are available
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Python camera libraries not yet installed")
        print("Basic camera detection successful - run this test again after OpenCV installation")
        return True
    
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
