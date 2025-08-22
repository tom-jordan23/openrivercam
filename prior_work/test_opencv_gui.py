#!/usr/bin/env python3
"""
Test OpenCV GUI functionality over X11 forwarding
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

# Check virtual environment first
check_venv()

import cv2
import numpy as np

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
