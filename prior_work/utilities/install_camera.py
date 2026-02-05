#!/usr/bin/env python3
"""
OpenRiverCam Camera Installation Script
Installs and configures all camera components for Raspberry Pi 5

This script performs a complete camera setup including:
1. Hardware configuration (raspi-config, boot settings)
2. System package installation (libcamera-apps, python libraries)
3. Virtual environment setup with camera dependencies
4. Camera testing and validation
5. Creation of test scripts and activation helpers

Requires: Raspberry Pi 5, sudo access, internet connection
"""

import os
import sys
import subprocess
import time
import shutil
import re
from pathlib import Path

class CameraInstaller:
    def __init__(self):
        self.is_pi = self._detect_raspberry_pi()
        self.venv_path = Path.home() / "openrivercam" / "venv"
        self.scripts_path = Path.home() / "openrivercam" / "scripts"
        self.config_txt = Path("/boot/firmware/config.txt")
        self.cmdline_txt = Path("/boot/firmware/cmdline.txt")
        self.verbose = True
        
        # Check for older Pi OS versions
        if not self.config_txt.exists():
            self.config_txt = Path("/boot/config.txt")
            self.cmdline_txt = Path("/boot/cmdline.txt")
        
    def _detect_raspberry_pi(self):
        """Detect if running on Raspberry Pi"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                content = f.read()
                return 'Raspberry Pi' in content or 'BCM' in content
        except:
            return False
    
    def _run_command(self, cmd, description, check=True, shell=False, show_output=True, timeout=None):
        """Run a command with error handling and detailed logging"""
        if self.verbose:
            cmd_str = cmd if isinstance(cmd, str) else ' '.join(cmd)
            print(f"🔄 {description}...")
            print(f"   💻 Command: {cmd_str}")
        
        try:
            kwargs = {
                'check': check,
                'capture_output': True,
                'text': True
            }
            if timeout:
                kwargs['timeout'] = timeout
                
            if shell:
                result = subprocess.run(cmd, shell=True, **kwargs)
            else:
                result = subprocess.run(cmd, **kwargs)
            
            if show_output and result.stdout and result.stdout.strip():
                print(f"   📝 Output: {result.stdout.strip()}")
            if result.stderr and result.stderr.strip():
                print(f"   ⚠️  Stderr: {result.stderr.strip()}")
                
            if self.verbose:
                print(f"   ✅ Command completed (exit code: {result.returncode})")
            return result
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Command failed with exit code {e.returncode}")
            if e.stderr and e.stderr.strip():
                print(f"   📝 Error output: {e.stderr.strip()}")
            if check:
                raise
            return e
        except subprocess.TimeoutExpired as e:
            print(f"   ⏰ Command timed out after {timeout} seconds")
            if check:
                raise
            return e
    
    def check_prerequisites(self):
        """Check system prerequisites and environment"""
        print("\n" + "=" * 60)
        print("🔍 STEP 1: CHECKING PREREQUISITES AND SYSTEM STATUS")
        print("=" * 60)
        
        # Detect hardware
        print("\n📊 Hardware Detection:")
        if not self.is_pi:
            print("   ⚠️  Warning: Not detected as Raspberry Pi")
            print("   📝 This script is designed for Raspberry Pi hardware")
            response = input("   ❓ Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("   🚪 Exiting installation")
                sys.exit(0)
        else:
            print("   ✅ Raspberry Pi detected")
            
            # Get Pi model info
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    content = f.read()
                    model_match = re.search(r'Model\s*:\s*(.+)', content)
                    if model_match:
                        print(f"   📝 Model: {model_match.group(1).strip()}")
                    
                    revision_match = re.search(r'Revision\s*:\s*(.+)', content)
                    if revision_match:
                        print(f"   📝 Revision: {revision_match.group(1).strip()}")
            except Exception as e:
                print(f"   ⚠️  Could not read detailed hardware info: {e}")
        
        # Check OS version
        print("\n🐧 Operating System:")
        try:
            result = self._run_command(['lsb_release', '-a'], "Getting OS info", check=False, show_output=False)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        print(f"   📝 {line.strip()}")
        except:
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            os_name = line.split('=', 1)[1].strip('"\n')
                            print(f"   📝 OS: {os_name}")
                            break
            except:
                print("   ⚠️  Could not determine OS version")
        
        # Check user permissions
        print("\n👤 User Permissions:")
        if os.geteuid() == 0:
            print("   ❌ Error: Running as root user")
            print("   📝 This script should be run as a regular user")
            print("   📝 Sudo will be used automatically when needed")
            sys.exit(1)
        else:
            current_user = os.getenv('USER', 'unknown')
            print(f"   ✅ Running as user: {current_user}")
            
            # Check sudo access
            try:
                result = self._run_command(['sudo', '-n', 'true'], 
                                         "Testing sudo access", check=False, show_output=False)
                if result.returncode == 0:
                    print("   ✅ Sudo access available (passwordless)")
                else:
                    print("   ⚠️  Sudo may require password prompts")
            except:
                print("   ⚠️  Could not test sudo access")
        
        # Check internet connectivity
        print("\n🌐 Network Connectivity:")
        try:
            result = self._run_command(['ping', '-c', '1', '-W', '3', '8.8.8.8'], 
                                     "Testing internet connectivity", check=False, show_output=False, timeout=5)
            if result.returncode == 0:
                print("   ✅ Internet connection available")
            else:
                print("   ❌ No internet connection detected")
                print("   📝 Internet is required for package installation")
                response = input("   ❓ Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(1)
        except:
            print("   ⚠️  Could not test internet connectivity")
        
        # Check boot partition access
        print("\n💾 Boot Configuration Access:")
        if self.config_txt.exists():
            print(f"   ✅ Found boot config: {self.config_txt}")
            if os.access(self.config_txt, os.R_OK):
                print("   ✅ Boot config is readable")
            else:
                print("   ⚠️  Boot config requires sudo to read")
        else:
            print(f"   ❌ Boot config not found at {self.config_txt}")
            print("   📝 This may indicate an unusual Pi OS setup")
        
        # Check existing camera status
        print("\n📷 Current Camera Status:")
        if self.is_pi:
            # Check vcgencmd camera status
            try:
                result = self._run_command(['vcgencmd', 'get_camera'], 
                                         "Checking hardware camera status", check=False, show_output=False)
                if result.returncode == 0 and result.stdout:
                    status = result.stdout.strip()
                    print(f"   📝 Hardware status: {status}")
                    if 'supported=1' in status and 'detected=1' in status:
                        print("   ✅ Camera hardware is enabled and detected")
                    elif 'supported=1' in status:
                        print("   ⚠️  Camera supported but not detected - check connection")
                    else:
                        print("   ❌ Camera hardware not enabled in config")
                else:
                    print("   ⚠️  Could not check camera hardware status")
            except:
                print("   ⚠️  vcgencmd not available or failed")
            
            # Check for existing camera software
            camera_tools = ['rpicam-hello', 'libcamera-hello', 'raspistill']
            found_tools = []
            for tool in camera_tools:
                if shutil.which(tool):
                    found_tools.append(tool)
            
            if found_tools:
                print(f"   📝 Found camera tools: {', '.join(found_tools)}")
            else:
                print("   📝 No camera tools found (will be installed)")
        
        print("\n✅ Prerequisites check completed")
    
    def configure_hardware(self):
        """Configure camera hardware using raspi-config and boot settings"""
        print("\n" + "=" * 60)
        print("🔧 STEP 2: CONFIGURING CAMERA HARDWARE")
        print("=" * 60)
        
        if not self.is_pi:
            print("\n⚠️  Skipping hardware configuration (not on Raspberry Pi)")
            return True
        
        # Enable camera using raspi-config
        print("\n📷 Enabling Camera Interface:")
        print("   📝 Using raspi-config to enable camera interface...")
        print("   📝 This configures the camera subsystem at the hardware level")
        
        try:
            # Use raspi-config nonint to enable camera
            result = self._run_command(['sudo', 'raspi-config', 'nonint', 'do_camera', '0'], 
                                     "Enabling camera interface via raspi-config", check=False)
            if result.returncode == 0:
                print("   ✅ Camera interface enabled successfully")
            else:
                print("   ⚠️  raspi-config camera enable may have failed")
                print("   📝 This might be normal on some Pi OS versions")
        except Exception as e:
            print(f"   ⚠️  Could not run raspi-config: {e}")
            print("   📝 Will proceed with manual configuration")
        
        # Configure boot settings
        self._configure_boot_settings()
        
        # Configure GPU memory split
        self._configure_gpu_memory()
        
        # Enable I2C (often needed for camera modules)
        print("\n🔌 Enabling I2C Interface:")
        try:
            result = self._run_command(['sudo', 'raspi-config', 'nonint', 'do_i2c', '0'], 
                                     "Enabling I2C interface", check=False)
            if result.returncode == 0:
                print("   ✅ I2C interface enabled")
            else:
                print("   ⚠️  I2C enable may have failed")
        except Exception as e:
            print(f"   ⚠️  Could not enable I2C: {e}")
        
        return True
    
    def _configure_boot_settings(self):
        """Configure boot settings for camera support"""
        print("\n⚙️  Configuring Boot Settings:")
        print(f"   📝 Checking boot configuration file: {self.config_txt}")
        
        if not self.config_txt.exists():
            print("   ❌ Boot config file not found")
            return False
        
        try:
            # Read current config
            with open(self.config_txt, 'r') as f:
                config_content = f.read()
            
            print("   📝 Reading current boot configuration...")
            
            # Settings to ensure for camera support
            required_settings = {
                'camera_auto_detect': '1',
                'dtoverlay': 'vc4-kms-v3d',
                'gpu_mem': '128'  # Will be handled separately
            }
            
            config_lines = config_content.split('\n')
            modified = False
            
            # Check and add camera settings
            print("   🔍 Checking camera-related boot settings...")
            
            # Check for camera_auto_detect
            has_camera_auto_detect = any('camera_auto_detect' in line and not line.strip().startswith('#') 
                                       for line in config_lines)
            
            if not has_camera_auto_detect:
                print("   📝 Adding camera_auto_detect=1")
                config_lines.append('camera_auto_detect=1')
                modified = True
            else:
                print("   ✅ camera_auto_detect already configured")
            
            # Check for VC4 overlay (needed for modern camera stack)
            has_vc4_overlay = any('dtoverlay=vc4-kms-v3d' in line and not line.strip().startswith('#') 
                                for line in config_lines)
            
            if not has_vc4_overlay:
                print("   📝 Adding VC4 KMS overlay for camera support")
                config_lines.append('dtoverlay=vc4-kms-v3d')
                modified = True
            else:
                print("   ✅ VC4 KMS overlay already configured")
            
            # Write back if modified
            if modified:
                print("   💾 Writing updated boot configuration...")
                backup_path = f"{self.config_txt}.backup.{int(time.time())}"
                
                # Create backup
                result = self._run_command(['sudo', 'cp', str(self.config_txt), backup_path], 
                                         f"Creating backup at {backup_path}")
                
                # Write new config
                new_config = '\n'.join(config_lines)
                with open('/tmp/new_config.txt', 'w') as f:
                    f.write(new_config)
                
                result = self._run_command(['sudo', 'cp', '/tmp/new_config.txt', str(self.config_txt)], 
                                         "Updating boot configuration")
                
                # Clean up temp file
                os.unlink('/tmp/new_config.txt')
                
                print("   ✅ Boot configuration updated successfully")
                print(f"   📝 Backup saved as: {backup_path}")
            else:
                print("   ✅ Boot configuration already optimal for camera")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to configure boot settings: {e}")
            return False
    
    def _configure_gpu_memory(self):
        """Configure GPU memory split for camera operations"""
        print("\n🎮 Configuring GPU Memory Split:")
        print("   📝 Camera operations require sufficient GPU memory")
        print("   📝 Checking current GPU memory allocation...")
        
        try:
            # Check current GPU memory
            result = self._run_command(['vcgencmd', 'get_mem', 'gpu'], 
                                     "Getting current GPU memory", check=False, show_output=False)
            
            if result.returncode == 0 and result.stdout:
                current_gpu_mem = result.stdout.strip()
                print(f"   📝 Current GPU memory: {current_gpu_mem}")
                
                # Parse the memory value
                gpu_mem_match = re.search(r'gpu=(\d+)M', current_gpu_mem)
                if gpu_mem_match:
                    gpu_mem_mb = int(gpu_mem_match.group(1))
                    print(f"   📝 Parsed GPU memory: {gpu_mem_mb}MB")
                    
                    if gpu_mem_mb < 128:
                        print(f"   ⚠️  GPU memory ({gpu_mem_mb}MB) is below recommended 128MB")
                        print("   📝 Setting GPU memory to 128MB for optimal camera performance")
                        
                        try:
                            # Use raspi-config to set GPU memory
                            result = self._run_command(['sudo', 'raspi-config', 'nonint', 'do_memory_split', '128'], 
                                                     "Setting GPU memory split to 128MB")
                            print("   ✅ GPU memory split updated to 128MB")
                        except Exception as e:
                            print(f"   ⚠️  Could not set GPU memory via raspi-config: {e}")
                            print("   📝 Will attempt manual configuration")
                            self._set_gpu_memory_manual()
                    else:
                        print(f"   ✅ GPU memory ({gpu_mem_mb}MB) is sufficient for camera operations")
                else:
                    print("   ⚠️  Could not parse GPU memory value")
            else:
                print("   ⚠️  Could not get current GPU memory")
                
        except Exception as e:
            print(f"   ⚠️  Error checking GPU memory: {e}")
    
    def _set_gpu_memory_manual(self):
        """Manually set GPU memory in config.txt"""
        print("   🔧 Manually configuring GPU memory in boot config...")
        
        try:
            with open(self.config_txt, 'r') as f:
                config_content = f.read()
            
            config_lines = config_content.split('\n')
            
            # Look for existing gpu_mem setting
            gpu_mem_line_idx = None
            for i, line in enumerate(config_lines):
                if line.strip().startswith('gpu_mem=') and not line.strip().startswith('#'):
                    gpu_mem_line_idx = i
                    break
            
            if gpu_mem_line_idx is not None:
                # Update existing line
                config_lines[gpu_mem_line_idx] = 'gpu_mem=128'
                print("   📝 Updated existing gpu_mem setting")
            else:
                # Add new line
                config_lines.append('gpu_mem=128')
                print("   📝 Added new gpu_mem=128 setting")
            
            # Write back
            new_config = '\n'.join(config_lines)
            with open('/tmp/gpu_config.txt', 'w') as f:
                f.write(new_config)
            
            result = self._run_command(['sudo', 'cp', '/tmp/gpu_config.txt', str(self.config_txt)], 
                                     "Updating boot config with GPU memory setting")
            
            os.unlink('/tmp/gpu_config.txt')
            print("   ✅ GPU memory manually configured")
            
        except Exception as e:
            print(f"   ❌ Failed to manually set GPU memory: {e}")
    
    def _check_reboot_required(self):
        """Check if a reboot is required and prompt user"""
        print("\n🔄 Checking Reboot Requirements:")
        
        reboot_needed = False
        
        # Check if reboot-required flag exists
        if Path("/var/run/reboot-required").exists():
            print("   ⚠️  System indicates reboot is required")
            reboot_needed = True
        
        # Check if we modified boot config
        try:
            result = self._run_command(['sudo', 'find', str(self.config_txt.parent), 
                                      '-name', f"{self.config_txt.name}.backup.*"], 
                                     "Checking for boot config backups", 
                                     check=False, show_output=False)
            if result.returncode == 0 and result.stdout.strip():
                print("   📝 Boot configuration was modified during this session")
                reboot_needed = True
        except:
            pass
        
        if reboot_needed:
            print("\n🚨 REBOOT REQUIRED")
            print("   📝 Hardware configuration changes require a system reboot")
            print("   📝 After reboot, you can continue with:")
            print(f"      python3 {Path(__file__).absolute()}")
            print("   📝 Or manually run camera tests")
            
            response = input("\n   ❓ Reboot now? (y/N): ")
            if response.lower() == 'y':
                print("   🔄 Rebooting system...")
                try:
                    subprocess.run(['sudo', 'reboot'], check=True)
                except:
                    print("   ❌ Reboot command failed - please reboot manually")
                sys.exit(0)
            else:
                print("   ⚠️  Please reboot manually when convenient")
                print("   📝 Camera may not work properly until reboot")
        else:
            print("   ✅ No reboot required")
    
    def install_system_packages(self):
        """Install required system packages"""
        print("\n" + "=" * 60)
        print("📦 STEP 3: INSTALLING SYSTEM PACKAGES")
        print("=" * 60)
        
        print("\n📋 Package Installation Overview:")
        print("   📝 This step installs essential system packages for camera support")
        print("   📝 Packages include: libcamera tools, Python bindings, OpenCV, and dependencies")
        print("   📝 Installation may take 5-15 minutes depending on network speed")
        
        packages = [
            'libcamera-apps',  # Provides rpicam-* commands
            'python3-libcamera',  # Python libcamera bindings
            'python3-kms++',  # KMS bindings for display
            'python3-picamera2',  # System picamera2 (for reference)
            'python3-opencv',  # System OpenCV (for dependencies)
            'python3-numpy',  # NumPy
            'python3-pil',  # Pillow
            'python3-pip',  # Pip
            'python3-venv',  # Virtual environment
        ]
        
        # Update package list
        print("\n🔄 Updating Package Database:")
        print("   📝 Refreshing APT package database to get latest versions...")
        try:
            result = self._run_command(['sudo', 'apt', 'update'], 
                                     "Updating APT package database", timeout=60)
            print("   ✅ Package database updated successfully")
        except subprocess.TimeoutExpired:
            print("   ⚠️  Package update timed out - continuing anyway")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to update package database: {e}")
            print("   📝 This may cause installation issues")
            return False
        
        # Install packages with detailed progress
        print(f"\n📥 Installing {len(packages)} Essential Packages:")
        failed_packages = []
        
        for i, package in enumerate(packages, 1):
            print(f"\n   📦 Package {i}/{len(packages)}: {package}")
            
            # Check if already installed
            try:
                check_result = self._run_command(['dpkg', '-l', package], 
                                               f"Checking if {package} is installed", 
                                               check=False, show_output=False)
                if check_result.returncode == 0 and 'ii' in check_result.stdout:
                    print(f"      ✅ {package} already installed")
                    continue
            except:
                pass  # Continue with installation
            
            # Install package
            try:
                print(f"      🔄 Installing {package}...")
                result = self._run_command(['sudo', 'apt', 'install', '-y', package], 
                                         f"Installing {package}", timeout=300, show_output=False)
                
                if result.returncode == 0:
                    print(f"      ✅ {package} installed successfully")
                else:
                    print(f"      ❌ {package} installation failed")
                    failed_packages.append(package)
                    
            except subprocess.TimeoutExpired:
                print(f"      ⏰ {package} installation timed out")
                failed_packages.append(package)
            except subprocess.CalledProcessError as e:
                print(f"      ❌ Failed to install {package}: {e}")
                if 'python3-picamera2' in package:
                    print("         📝 picamera2 will be installed via pip instead")
                else:
                    failed_packages.append(package)
        
        # Report results
        if failed_packages:
            print(f"\n⚠️  Some packages failed to install: {', '.join(failed_packages)}")
            print("   📝 This may not prevent camera functionality")
        else:
            print(f"\n✅ All {len(packages)} system packages installed successfully")
        
        return True
    
    def test_rpicam_tools(self):
        """Test rpicam command line tools"""
        print("\n🔧 Testing rpicam tools...")
        
        # Check if rpicam-hello exists
        if not shutil.which('rpicam-hello'):
            print("   ❌ rpicam-hello not found")
            return False
        
        print("   ✅ rpicam-hello found")
        
        # Test camera detection
        try:
            result = self._run_command(['rpicam-hello', '--list-cameras'], 
                                     "Testing camera detection", timeout=10)
            if 'No cameras available' in result.stdout:
                print("   ❌ No cameras detected")
                return False
            else:
                print("   ✅ Camera detected successfully")
                return True
        except subprocess.TimeoutExpired:
            print("   ❌ Camera detection timed out")
            return False
        except Exception as e:
            print(f"   ❌ Camera detection failed: {e}")
            return False
    
    def setup_virtual_environment(self):
        """Set up Python virtual environment"""
        print(f"\n🐍 Setting up virtual environment at {self.venv_path}...")
        
        # Create openrivercam directory
        openrivercam_dir = self.venv_path.parent
        openrivercam_dir.mkdir(parents=True, exist_ok=True)
        
        # Create virtual environment
        if self.venv_path.exists():
            print("   ⚠️  Virtual environment already exists")
            response = input("   Recreate? (y/N): ")
            if response.lower() == 'y':
                shutil.rmtree(self.venv_path)
            else:
                print("   ✅ Using existing virtual environment")
                return True
        
        try:
            self._run_command([sys.executable, '-m', 'venv', str(self.venv_path)], 
                            "Creating virtual environment")
            print("   ✅ Virtual environment created")
        except Exception as e:
            print(f"   ❌ Failed to create virtual environment: {e}")
            return False
        
        # Create activation script
        activate_script = openrivercam_dir / "activate_env.sh"
        with open(activate_script, 'w') as f:
            f.write(f"""#!/bin/bash
# OpenRiverCam Environment Activation Script
source {self.venv_path}/bin/activate
export PYTHONPATH="{self.venv_path}/lib/python3.11/site-packages:$PYTHONPATH"
echo "✅ OpenRiverCam environment activated"
echo "Python: $(which python3)"
echo "Location: {self.venv_path}"
""")
        activate_script.chmod(0o755)
        print(f"   ✅ Activation script created: {activate_script}")
        
        return True
    
    def install_python_packages(self):
        """Install Python packages in virtual environment"""
        print("\n📚 Installing Python packages...")
        
        pip_path = self.venv_path / "bin" / "pip"
        python_path = self.venv_path / "bin" / "python"
        
        if not pip_path.exists():
            print("   ❌ Virtual environment pip not found")
            return False
        
        # Upgrade pip first
        try:
            self._run_command([str(pip_path), 'install', '--upgrade', 'pip'], 
                            "Upgrading pip")
            print("   ✅ Pip upgraded")
        except Exception as e:
            print(f"   ⚠️  Pip upgrade failed: {e}")
        
        # Install packages
        packages = [
            'picamera2',
            'opencv-python',
            'numpy',
            'pillow',
            'scipy',
            'pandas',
        ]
        
        for package in packages:
            try:
                self._run_command([str(pip_path), 'install', package], 
                                f"Installing {package}")
                print(f"   ✅ Installed {package}")
            except Exception as e:
                print(f"   ❌ Failed to install {package}: {e}")
                if package == 'picamera2':
                    print("   ⚠️  Will try alternative installation method")
                    continue
                return False
        
        # Test imports
        print("   🧪 Testing package imports...")
        test_imports = [
            ('cv2', 'OpenCV'),
            ('numpy', 'NumPy'),
            ('PIL', 'Pillow'),
        ]
        
        for module, name in test_imports:
            try:
                result = self._run_command([str(python_path), '-c', f'import {module}; print("{name} OK")'], 
                                         f"Testing {name}")
                print(f"   ✅ {name} import successful")
            except Exception as e:
                print(f"   ❌ {name} import failed: {e}")
        
        # Test picamera2 separately (may need system libraries)
        try:
            result = self._run_command([str(python_path), '-c', 'from picamera2 import Picamera2; print("Picamera2 OK")'], 
                                     "Testing Picamera2")
            print("   ✅ Picamera2 import successful")
        except Exception as e:
            print(f"   ⚠️  Picamera2 import failed: {e}")
            print("   📝 This may require system library symlinks")
        
        return True
    
    def create_camera_test_script(self):
        """Create camera test script"""
        print(f"\n📝 Creating camera test script...")
        
        self.scripts_path.mkdir(parents=True, exist_ok=True)
        test_script_path = self.scripts_path / "test_camera.py"
        
        test_script_content = '''#!/usr/bin/env python3
"""
OpenRiverCam Camera Test Script
Tests camera functionality for Raspberry Pi 5
"""

import sys
import os
import time
import subprocess
from pathlib import Path

def check_rpicam_tools():
    """Test rpicam command line tools"""
    print("🔧 Testing rpicam tools...")
    
    try:
        result = subprocess.run(['rpicam-hello', '--list-cameras'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Camera detection via rpicam-hello:")
            print(result.stdout)
            return True
        else:
            print("❌ rpicam-hello failed to detect cameras")
            return False
    except FileNotFoundError:
        print("❌ rpicam-hello not found - install libcamera-apps")
        return False
    except subprocess.TimeoutExpired:
        print("❌ rpicam-hello timed out")
        return False
    except Exception as e:
        print(f"❌ rpicam test failed: {e}")
        return False

def test_python_camera():
    """Test Python camera libraries"""
    print("\\n🐍 Testing Python camera libraries...")
    
    # Test imports
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        from picamera2 import Picamera2
        print("✅ Picamera2 imported successfully")
    except ImportError as e:
        print(f"❌ Picamera2 import failed: {e}")
        print("   Install with: pip install picamera2")
        return False
    
    # Test camera initialization
    try:
        print("📷 Initializing camera...")
        picam2 = Picamera2()
        
        config = picam2.create_still_configuration(
            main={"size": (1920, 1080), "format": "RGB888"}
        )
        picam2.configure(config)
        
        print("🔄 Starting camera...")
        picam2.start()
        time.sleep(2)
        
        print("📸 Capturing test image...")
        image = picam2.capture_array()
        
        # Basic image analysis
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        height, width = gray.shape
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        print(f"✅ Camera test successful!")
        print(f"   Resolution: {width}x{height}")
        print(f"   Brightness: {brightness:.1f}")
        print(f"   Contrast: {contrast:.1f}")
        
        # Save test image
        data_dir = Path.home() / "openrivercam" / "data" / "raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = data_dir / f"camera_test_{timestamp}.jpg"
        
        cv2.imwrite(str(filename), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        print(f"   Image saved: {filename}")
        
        picam2.stop()
        return True
        
    except Exception as e:
        print(f"❌ Python camera test failed: {e}")
        try:
            picam2.stop()
        except:
            pass
        return False

def main():
    """Run all camera tests"""
    print("🎥 OpenRiverCam Camera Test")
    print("=" * 40)
    
    # Test rpicam tools
    rpicam_ok = check_rpicam_tools()
    
    # Test Python libraries
    python_ok = test_python_camera()
    
    print("\\n" + "=" * 40)
    if rpicam_ok and python_ok:
        print("🎉 All camera tests passed!")
        return 0
    else:
        print("❌ Some camera tests failed")
        if not rpicam_ok:
            print("   - Install system packages: sudo apt install libcamera-apps")
        if not python_ok:
            print("   - Install Python packages: pip install picamera2 opencv-python")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
        
        with open(test_script_path, 'w') as f:
            f.write(test_script_content)
        
        test_script_path.chmod(0o755)
        print(f"   ✅ Test script created: {test_script_path}")
        
        return True
    
    def run_final_test(self):
        """Run final camera test"""
        print("\n🧪 Running final camera test...")
        
        test_script = self.scripts_path / "test_camera.py"
        python_path = self.venv_path / "bin" / "python"
        
        if not test_script.exists():
            print("   ❌ Test script not found")
            return False
        
        try:
            result = self._run_command([str(python_path), str(test_script)], 
                                     "Running camera test")
            return result.returncode == 0
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            return False
    
    def print_summary(self):
        """Print installation summary"""
        print("\n" + "=" * 50)
        print("🎉 Camera Installation Complete!")
        print("=" * 50)
        print(f"Virtual Environment: {self.venv_path}")
        print(f"Test Script: {self.scripts_path}/test_camera.py")
        print(f"Activation Script: {self.venv_path.parent}/activate_env.sh")
        print()
        print("To use the camera:")
        print(f"1. Activate environment: source {self.venv_path.parent}/activate_env.sh")
        print(f"2. Test camera: python {self.scripts_path}/test_camera.py")
        print()
        print("Available rpicam commands:")
        print("  rpicam-hello --list-cameras    # List cameras")
        print("  rpicam-hello --nopreview --timeout 5000ms  # Test camera")
        print("  rpicam-still --nopreview -o image.jpg      # Capture image")
        print()
    
    def run(self):
        """Run the complete installation process"""
        print("🎥 OpenRiverCam Camera Installation & Configuration")
        print("=" * 60)
        print("📝 This script will configure your Raspberry Pi 5 for camera operations")
        print("📝 The process includes hardware config, software installation, and testing")
        print("📝 Total estimated time: 15-30 minutes")
        print("📝 A reboot may be required after hardware configuration")
        print("=" * 60)
        
        try:
            # Step 1: Check prerequisites
            self.check_prerequisites()
            
            # Step 2: Configure hardware (may require reboot)
            print("\n⚠️  Hardware configuration may modify boot settings")
            print("   📝 If boot settings are changed, a reboot will be required")
            
            if not self.configure_hardware():
                print("❌ Hardware configuration failed")
                print("   📝 You may need to manually enable camera in raspi-config")
                response = input("   ❓ Continue with software installation anyway? (y/N): ")
                if response.lower() != 'y':
                    return False
            
            # Check if reboot is needed
            self._check_reboot_required()
            
            # Step 3: Install system packages
            if not self.install_system_packages():
                print("❌ System package installation failed")
                print("   📝 Check internet connection and package repositories")
                return False
            
            # Step 4: Test rpicam tools
            print("\n" + "=" * 60)
            print("🧪 STEP 4: TESTING CAMERA HARDWARE")
            print("=" * 60)
            
            if not self.test_rpicam_tools():
                print("❌ Camera hardware test failed")
                print("   📝 Possible issues:")
                print("      - Camera not connected properly")
                print("      - Camera not enabled (reboot may be required)")
                print("      - Hardware incompatibility")
                
                response = input("   ❓ Continue with Python setup anyway? (y/N): ")
                if response.lower() != 'y':
                    return False
            
            # Step 5: Set up virtual environment
            if not self.setup_virtual_environment():
                print("❌ Virtual environment setup failed")
                return False
            
            # Step 6: Install Python packages
            if not self.install_python_packages():
                print("❌ Python package installation failed")
                return False
            
            # Create test script
            if not self.create_camera_test_script():
                print("❌ Test script creation failed")
                return False
            
            # Run final test
            test_passed = self.run_final_test()
            
            # Print summary
            self.print_summary()
            
            if test_passed:
                print("✅ Installation and testing completed successfully!")
            else:
                print("⚠️  Installation completed but camera test failed")
                print("   Run the test script manually to debug issues")
            
            return True
            
        except KeyboardInterrupt:
            print("\n❌ Installation interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Installation failed: {e}")
            return False

def main():
    """Main entry point"""
    installer = CameraInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()