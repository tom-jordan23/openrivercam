# OpenRiverCam Raspberry Pi Deployment

## Project Overview

This project provides comprehensive documentation and setup guides for deploying OpenRiverCam river monitoring systems on Raspberry Pi 5 hardware. OpenRiverCam is an open-source computer vision system that analyzes water flow patterns in rivers using particle image velocimetry and optical flow techniques.

### Mission Statement

Develop autonomous, low-cost river monitoring stations that can operate in remote locations to support flood monitoring and disaster preparedness efforts, with initial deployment planned for Indonesian rivers in collaboration with the Indonesian Red Cross (PMI).

## Repository Structure

### 📋 **Configuration Files**
- **`CLAUDE.md`** - AI assistant configuration for software development phase
- **`prompt.md`** - Detailed implementation instructions for AI-assisted development

### 📚 **Setup Guides**

#### **Phase 1: Lab Development**
- **`openrivercam_lab_setup_guide.md`** - Complete setup guide for lab testing
  - Raspberry Pi 5 + Camera Module configuration
  - Isolated Python virtual environment setup
  - Core OpenRiverCam functionality testing
  - WiFi connectivity and data management
  - Comprehensive testing framework

#### **Phase 2: Field Deployment** 
- **`openrivercam_pi5_setup_guide.md`** - Full field deployment documentation
  - Environmental monitoring and control systems
  - Solar power and battery management
  - 4G cellular connectivity for remote locations
  - Weatherproof enclosures and autonomous operation
  - Advanced system monitoring and diagnostics

### 🏗️ **Hardware Documentation**
- **`hardware/`** directory contains:
  - **`CLAUDE.md`** - Hardware engineering specifications
  - **`prompt.md`** - Hardware design and sourcing instructions
  - **`bom_*.csv`** - Bill of materials for different budget tiers
  - **`power_analysis.md`** - Power system calculations and requirements
  - **`reference_solutions.csv`** - Comparison of commercial alternatives

## Quick Start Guide

### For Lab Testing (Recommended Starting Point)

1. **Follow the Lab Setup Guide**
   ```bash
   # Read the comprehensive lab guide
   cat openrivercam_lab_setup_guide.md
   ```

2. **Key Prerequisites**
   - Raspberry Pi 5 (4GB+ RAM)
   - Raspberry Pi Camera Module v3
   - microSD card (64GB+ Class 10)
   - Reliable power supply and WiFi connection

3. **Core Setup Steps**
   - Install Raspberry Pi OS (64-bit)
   - Configure camera and basic system settings
   - Set up isolated Python virtual environment
   - Install OpenRiverCam and dependencies
   - Run comprehensive test suite

### For Field Deployment (After Lab Testing)

1. **Complete Lab Setup First** - Ensure core functionality works reliably
2. **Follow Field Deployment Guide** - Adds environmental controls and autonomous operation
3. **Hardware Integration** - Add sensors, power systems, and communication modules

## Project Phases

### 🏠 **Phase 1: Lab Development** (Current)
**Goal**: Get core OpenRiverCam functionality working in controlled environment

**Components**:
- ✅ Raspberry Pi 5 + Camera Module
- ✅ Standard power supply (utility power)
- ✅ WiFi connectivity
- ✅ Basic cooling system
- ✅ Desktop/lab environment

**Features**:
- 🎥 Camera capture and calibration
- 🔬 River flow analysis using OpenCV
- 📊 Data processing and export
- 📡 WiFi-based data transmission
- 🧪 Comprehensive testing framework

### 🌿 **Phase 2: Field Hardening** (Future)
**Goal**: Deploy autonomous monitoring stations in remote locations

**Additional Components**:
- 🌡️ Environmental monitoring (temperature, humidity)
- ⚡ Solar power system with battery backup
- 📱 4G cellular connectivity
- 🏠 Weatherproof enclosure
- 🕐 Real-time clock for scheduling

**Advanced Features**:
- 🤖 Fully autonomous operation
- 🌊 Environmental condition management
- 📡 Remote monitoring and control
- 🔋 Power-aware scheduling
- 📈 Advanced diagnostics and telemetry

## Technical Specifications

### Software Stack
- **Operating System**: Raspberry Pi OS (64-bit) - headless configuration
- **Computer Vision**: OpenCV 4.8.1+ with custom flow analysis
- **Camera Interface**: PiCamera2 for Raspberry Pi Camera Module v3
- **Data Processing**: NumPy, SciPy, Pandas
- **Communication**: HTTP/HTTPS with data compression
- **Scheduling**: Systemd timers with RTC backup
- **Remote Access**: SSH with X11 forwarding for GUI applications

### Hardware Targets
- **Computing**: Raspberry Pi 5 (4GB/8GB RAM)
- **Storage**: 64GB+ microSD (expandable)
- **Camera**: Raspberry Pi Camera Module v3 (12MP)
- **Connectivity**: WiFi 6 (lab) / 4G LTE (field)
- **Power**: 5V/5A (lab) / Solar+Battery (field)

## Development Workflow

### Lab Testing Cycle
```bash
# 1. Activate Python environment
source ~/openrivercam/activate_env.sh

# 2. Test camera functionality
python3 ~/openrivercam/scripts/test_camera.py

# 3. Run river analysis
python3 ~/openrivercam/scripts/basic_analysis.py

# 4. Validate data management
python3 ~/openrivercam/scripts/data_manager.py

# 5. Test data transmission
python3 ~/openrivercam/scripts/upload_results.py

# 6. Run comprehensive test suite
python3 ~/openrivercam/scripts/run_tests.py
```

### Field Deployment Preparation
1. **Complete lab validation** - All tests passing consistently
2. **Hardware integration** - Add environmental and power systems  
3. **Field testing** - Validate in controlled outdoor environment
4. **Deployment** - Install at remote monitoring location

## Key Features

### 🎯 **Core Functionality**
- **Automated River Analysis** - Hourly capture and processing cycles
- **Computer Vision Processing** - Optical flow and particle tracking
- **Quality Assessment** - Image quality validation and error handling
- **Data Management** - Local storage with automatic cleanup
- **Remote Transmission** - Reliable data upload with retry logic

### 🔧 **System Management**
- **Isolated Environment** - Complete Python virtual environment isolation
- **Comprehensive Testing** - Automated test suite for all components
- **Error Recovery** - Robust error handling and automatic recovery
- **Remote Monitoring** - System health and status reporting
- **Maintenance Tools** - Easy troubleshooting and diagnostics

### 🌍 **Field-Ready Design** (Phase 2)
- **Environmental Control** - Temperature and humidity management
- **Power Management** - Solar charging with battery backup
- **Cellular Communication** - 4G connectivity for remote locations
- **Weather Resistance** - IP65/67 rated enclosures
- **Autonomous Operation** - Months of unattended operation

## Contributing

### Documentation Structure
- Each setup guide is comprehensive and standalone
- Code examples are tested and validated
- Hardware specifications include sourcing information
- Troubleshooting sections cover common issues

### Testing Requirements
- All scripts include virtual environment validation
- Complete test suites verify functionality
- Hardware compatibility is documented
- Performance benchmarks are provided

## Deployment Locations

### Target Environment
- **Primary**: Indonesian rivers for flood monitoring
- **Climate**: Tropical jungle conditions (high humidity, temperature variation)
- **Infrastructure**: Limited or no grid power/internet connectivity
- **Maintenance**: Remote locations with infrequent service access

### Collaboration
- **Indonesian Red Cross (PMI)** - Flood monitoring and disaster preparedness
- **Local Communities** - Installation and basic maintenance support
- **Research Organizations** - Data analysis and algorithm improvement

## Support and Troubleshooting

### Documentation Resources
1. **Lab Setup Issues** - See `openrivercam_lab_setup_guide.md` troubleshooting section
2. **Field Deployment** - See `openrivercam_pi5_setup_guide.md` for advanced topics
3. **Hardware Problems** - Check hardware documentation in `hardware/` directory

### Common Issues
- **Camera not detected** - Check physical connection and enable camera interface
- **Python import errors** - Verify virtual environment activation
- **Network connectivity** - Test WiFi configuration and internet access
- **Performance issues** - Monitor system resources and optimize settings

## License and Credits

This project builds upon the [OpenRiverCam](https://github.com/localdevices/OpenRiverCam) open-source computer vision framework for river flow analysis.

### Acknowledgments
- OpenRiverCam development team for the core computer vision algorithms
- Indonesian Red Cross (PMI) for deployment collaboration and requirements
- Raspberry Pi Foundation for the computing platform
- Open source community for various software components

---

## Getting Started

**New to the project?** Start with the [Lab Setup Guide](openrivercam_lab_setup_guide.md) to get OpenRiverCam running on your Raspberry Pi 5 in a controlled environment.

**Ready for deployment?** After successful lab testing, proceed to the [Field Deployment Guide](openrivercam_pi5_setup_guide.md) for autonomous operation setup.

**Questions?** Check the troubleshooting sections in the respective guides or review the hardware documentation for component-specific issues.