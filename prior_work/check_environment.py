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
