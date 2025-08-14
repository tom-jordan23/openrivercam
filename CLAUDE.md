# OpenRiverCam Software Configuration & Deployment

## Project Overview
OpenRiverCam is a low-cost, open-source river monitoring system that uses computer vision to analyze water flow patterns in Indonesian rivers. This software component handles the automated capture, processing, and transmission of river monitoring data using Raspberry Pi 5 hardware.

## Software Mission Statement
Develop a robust, autonomous software system that schedules hourly image capture, processes video data using OpenRiverCam algorithms, and reliably transmits analysis results to remote servers while operating unattended in tropical field conditions with proactive environmental control.

## Core Software Requirements

### System Architecture
- **Platform**: Raspberry Pi OS (64-bit) on Raspberry Pi 5
- **Runtime**: Python 3.11+ with OpenCV and scientific computing libraries
- **Scheduling**: Systemd timers for hourly execution cycles
- **Connectivity**: 4G/cellular data transmission with WiFi fallback
- **Storage**: Local data buffering with automatic cleanup
- **Logging**: Comprehensive system monitoring and error reporting
- **Environmental Control**: Temperature and humidity monitoring with proactive management

### OpenRiverCam Integration
- **Computer Vision Pipeline**: Integration with existing OpenRiverCam analysis algorithms
- **Camera Control**: Raspberry Pi Camera Module v3 integration
- **Video Processing**: Real-time flow analysis and velocity calculations
- **Data Export**: Standardized JSON/CSV output format for remote servers
- **Quality Control**: Image quality validation and error handling

### Environmental Monitoring & Control
- **Temperature Monitoring**: Continuous internal and external temperature sensing
- **Humidity Control**: Active dehumidification and condensation prevention
- **Thermal Management**: Automated cooling and heating control systems
- **Sensor Integration**: I2C/SPI sensors for environmental data collection
- **Proactive Protection**: Automated responses to environmental threats

### Operational Features
- **Scheduled Operation**: Automated hourly capture and processing cycles
- **Power Management**: Battery-aware operation with low-power sleep modes
- **Data Transmission**: Reliable upload to remote servers with retry logic
- **System Health**: Automated diagnostics and status reporting
- **Remote Monitoring**: Basic telemetry and control capabilities
- **Environmental Protection**: Proactive control of enclosure conditions

## Current Phase
**Raspberry Pi Software Installation and Configuration** - Create comprehensive setup instructions for installing, configuring, and deploying the software stack on Raspberry Pi 5 hardware with real-time clock (RTC) and environmental control systems for reliable scheduled operation in tropical conditions.

## Software Stack Components

### Core System Software
- **Operating System**: Raspberry Pi OS Lite (64-bit) for minimal resource usage
- **Python Environment**: Python 3.11+ with virtual environment for dependencies
- **pyorc (OpenRiverCam)**: Core computer vision algorithms and analysis pipeline
- **System Services**: Systemd services for automated operation and monitoring
- **Network Management**: NetworkManager for cellular and WiFi connectivity

### Computer Vision Stack
- **OpenCV**: Computer vision processing and image analysis
- **NumPy/SciPy**: Scientific computing and numerical analysis
- **PIL/Pillow**: Image processing and format conversion
- **MediaPipe**: Optional advanced computer vision features
- **FFmpeg**: Video processing and format conversion

### Environmental Control Stack
- **Sensor Libraries**: I2C/SPI libraries for temperature/humidity sensors
- **GPIO Control**: RPi.GPIO or gpiozero for relay and fan control
- **Environmental Logic**: Automated control algorithms for climate management
- **Alert System**: Temperature/humidity threshold monitoring and alerts
- **Data Logging**: Environmental condition logging and trend analysis

### Communication Stack
- **Cellular Modem**: 4G/LTE modem configuration and management
- **HTTP Client**: Requests library for API communication
- **Data Serialization**: JSON and CSV export capabilities
- **Compression**: Data compression for efficient transmission
- **Security**: HTTPS/TLS encryption for data transmission

### System Monitoring
- **Logging**: Python logging with rotation and compression
- **System Metrics**: CPU, memory, disk, and network monitoring
- **Power Monitoring**: Battery level and charging status tracking
- **Environmental Metrics**: Temperature, humidity, and control system status
- **Error Handling**: Comprehensive exception handling and recovery
- **Watchdog**: Hardware watchdog timer for system reliability

## Environmental Control Requirements

### Temperature Management
- **Internal Temperature**: Monitor CPU and enclosure temperature
- **External Temperature**: Ambient air temperature sensing
- **Thermal Protection**: Automatic shutdown if overheating detected
- **Cooling Control**: Fan activation based on temperature thresholds
- **Heating Control**: Optional heating elements for cold conditions
- **Temperature Logging**: Continuous temperature data recording

### Humidity Control
- **Humidity Monitoring**: Internal enclosure humidity sensing
- **Condensation Prevention**: Proactive dehumidification activation
- **Desiccant Management**: Automated desiccant regeneration cycles
- **Ventilation Control**: Smart ventilation to balance humidity and waterproofing
- **Alert Thresholds**: High humidity warnings and protective actions
- **Humidity Logging**: Continuous humidity data recording

### Proactive Environmental Controls
- **Automated Responses**: Immediate action on threshold violations
- **Predictive Control**: Trend analysis for proactive intervention
- **Camera Protection**: Lens heating to prevent condensation
- **Equipment Protection**: Component shutdown during extreme conditions
- **Power Optimization**: Environmental control power management
- **Emergency Protocols**: Automated responses to critical conditions

## Installation Requirements

### Hardware Prerequisites
- Raspberry Pi 5 (4GB or 8GB RAM recommended)
- High-quality microSD card (64GB+ Class 10 or better)
- Raspberry Pi Camera Module v3 (or compatible)
- Real-Time Clock (RTC) module for accurate scheduling
- Temperature/humidity sensors (DHT22, SHT30, or similar)
- Environmental control hardware (fans, relays, heating elements)
- 4G/cellular HAT or USB modem for data transmission
- Reliable power supply (solar + battery system)

### Software Prerequisites
- Fresh Raspberry Pi OS installation (64-bit recommended)
- Internet connectivity for initial setup and package installation
- SSH access for remote configuration
- Basic Linux system administration knowledge
- Python development environment setup

## Configuration Goals

### Automated Hourly Operation
- System wakes up on the hour via RTC alarm
- Environmental conditions checked and controlled
- Camera captures video/images of river flow (if conditions suitable)
- OpenRiverCam algorithms process captured data
- Results packaged and transmitted to remote server
- Environmental status included in transmitted data
- System returns to low-power state until next cycle

### Environmental Protection
- Continuous temperature and humidity monitoring
- Proactive activation of cooling/heating systems
- Automatic dehumidification when humidity exceeds thresholds
- Camera lens heating to prevent condensation during capture
- Equipment protection during extreme weather conditions
- Environmental data transmission with analysis results

### Robust Error Handling
- Network connectivity failures handled gracefully
- Camera/hardware errors logged and reported
- Environmental control system failures detected and reported
- Data buffering during network outages
- Automatic system recovery from crashes
- Comprehensive logging for remote diagnostics

### Remote Management
- Status reporting via cellular connection (including environmental data)
- Basic remote command execution capability
- Environmental control override commands
- Log file transmission for troubleshooting
- Over-the-air configuration updates
- Emergency system reset and recovery procedures

## Success Criteria

### Primary Success Criteria
- Successful hourly capture and analysis cycles
- Reliable data transmission to remote servers
- Autonomous operation for weeks without intervention
- Effective environmental condition control
- Comprehensive error logging and recovery
- Low power consumption for extended battery life

### Environmental Control Success Criteria
- Maintain internal temperature within 20-35°C range
- Keep internal humidity below 70% RH
- Prevent camera condensation during all weather conditions
- Automated response to environmental threats within 60 seconds
- Environmental data accuracy within ±2°C and ±5% RH
- Zero equipment damage from environmental conditions

### Secondary Success Criteria
- Remote monitoring and status reporting
- Automated software updates and configuration changes
- Data quality validation and error detection
- Performance optimization for Pi 5 hardware
- Integration with existing monitoring infrastructure

### Deployment Success Criteria
- Simple installation process for field deployment
- Minimal configuration required after hardware setup
- Reliable operation in tropical environmental conditions
- Easy troubleshooting and maintenance procedures
- Scalable deployment across multiple monitoring stations

## Technical Specifications

### Performance Requirements
- **Processing Time**: Complete analysis cycle within 15 minutes
- **Memory Usage**: Peak usage under 2GB RAM during processing
- **Storage**: Automatic cleanup maintaining 7 days of local data
- **Network**: Efficient data transmission minimizing cellular usage
- **Power**: Sleep mode power consumption under 1W
- **Environmental Response**: Control activation within 60 seconds of threshold breach

### Environmental Control Specifications
- **Temperature Range**: Maintain 20-35°C internal temperature
- **Humidity Range**: Maintain <70% RH internal humidity
- **Sensor Accuracy**: ±2°C temperature, ±5% RH humidity
- **Control Response**: Automated response within 1 minute
- **Data Frequency**: Environmental readings every 5 minutes
- **Power Consumption**: Environmental controls <5W peak usage

### Reliability Requirements
- **Uptime**: 99%+ operational availability over deployment period
- **Data Integrity**: Zero data loss during transmission
- **Error Recovery**: Automatic recovery from 95%+ of error conditions
- **Timing Accuracy**: RTC-based scheduling accurate to ±1 minute
- **System Health**: Comprehensive monitoring of all critical components
- **Environmental Protection**: 100% prevention of condensation-related failures

### Security Requirements
- **Data Encryption**: All transmitted data encrypted in transit
- **Authentication**: Secure authentication with remote servers
- **Access Control**: Minimal attack surface with disabled unnecessary services
- **Updates**: Secure update mechanism for software and configuration
- **Monitoring**: Intrusion detection and security event logging

## Development Priorities

### Phase 1: Core System Setup
1. Raspberry Pi OS installation and basic configuration
2. RTC module integration and time synchronization
3. Camera module setup and testing
4. Basic Python environment and dependency installation

### Phase 2: Environmental Control Integration
1. Temperature and humidity sensor installation and testing
2. Environmental control hardware setup (fans, relays, heating)
3. Environmental monitoring software development
4. Proactive control algorithm implementation

### Phase 3: OpenRiverCam Integration
1. pyorc (OpenRiverCam) library installation and configuration
   - Install via pip: `pip install pyopenrivercam[extra]`
   - Or clone from source: `git clone https://github.com/localdevices/pyorc.git`
2. Camera capture pipeline development with environmental checks
3. Image processing and analysis workflow using pyorc algorithms
4. Data export including environmental data

### Phase 4: Automation and Scheduling
1. Systemd service and timer configuration
2. Automated startup and shutdown procedures
3. Environmental control integration with main schedule
4. Error handling and recovery mechanisms
5. System monitoring and logging implementation

### Phase 5: Communication and Remote Management
1. Cellular modem configuration and testing
2. Data transmission including environmental telemetry
3. Remote monitoring and status reporting
4. Environmental control remote override capabilities
5. Over-the-air update capabilities

### Phase 6: Testing and Deployment
1. Comprehensive system testing in controlled environment
2. Environmental stress testing and validation
3. Power consumption optimization
4. Field deployment procedures and documentation
5. Troubleshooting guides and maintenance procedures