# IoT Home Defense System

A Raspberry Pi-based security system featuring motion detection, RFID authentication, real-time monitoring, and automated alerts with MQTT integration.

## Team Members
- Nathan Roos
- Louis Caron

## System Overview

This IoT home defense system provides comprehensive security monitoring with the following features:

- **Motion Detection**: PIR sensor monitors for unauthorized movement
- **RFID Authentication**: Secure arm/disarm using RFID key cards
- **Visual Indicators**: Three-LED system (Green/Yellow/Red) shows system state
- **Audio Alerts**: Buzzer provides warning beeps and alarm sounds
- **LCD Display**: 16x2 character display shows countdown timers and temperature
- **Camera Integration**: Captures photos on disarm and records video during alerts
- **Environmental Monitoring**: DHT11 sensor tracks temperature
- **MQTT Integration**: Real-time status updates to cloud dashboard
- **Data Logging**: CSV logging of all system events

### System States

1. **DISARMED** (Green LED): System idle, displays time and temperature
2. **ARMING** (Yellow LED blinking): 15-second countdown with warning beeps
3. **ARMED** (Red LED): Motion detection active
4. **DISARMING** (Yellow LED blinking): User has limited time to present RFID key
5. **ALERT** (Red LED blinking): Alarm triggered, recording video

### Block Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Raspberry Pi 4                              │
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Main       │      │   MQTT       │      │   Camera     │  │
│  │   Controller │◄────►│   Client     │      │   Module     │  │
│  │   (main.py)  │      │              │      │   (Pi Cam)   │  │
│  └──────┬───────┘      └──────────────┘      └──────┬───────┘  │
│         │                                             │           │
│         ├─────────────────────────────────────────────┤           │
│         │                                             │           │
└─────────┼─────────────────────────────────────────────┼───────────┘
          │                                             │
    ┌─────┴─────────────────────────────────────────────┴─────┐
    │                                                           │
    ▼                                                           ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│  PIR   │  │  RFID  │  │ Button │  │ Buzzer │  │  LEDs  │  │  LCD   │
│ Motion │  │ RC522  │  │        │  │        │  │  x3    │  │ 16x2   │
│ Sensor │  │ Reader │  │        │  │        │  │        │  │        │
└────────┘  └────────┘  └────────┘  └────────┘  └────────┘  └────────┘
    │           │           │           │           │           │
    └───────────┴───────────┴───────────┴───────────┴───────────┘
                          GPIO Interface
```

## Bill of Materials

| Component | Model | Quantity | Link |
|-----------|-------|----------|------|
| Microcontroller | Raspberry Pi 4 Model B (4GB) | 1 | [Adafruit](https://www.adafruit.com/product/4296) |
| Camera | Raspberry Pi Camera Module V2 | 1 | [Adafruit](https://www.adafruit.com/product/3099) |
| Motion Sensor | HC-SR501 PIR Motion Sensor | 1 | [Amazon](https://www.amazon.com/HC-SR501-Sensor-Infrared-Arduino-Raspberry/dp/B07KZW86YR) |
| RFID Reader | MFRC522 RFID Module | 1 | [Amazon](https://www.amazon.com/HiLetgo-RFID-Kit-Arduino-Raspberry/dp/B01CSTW0IA) |
| Temperature Sensor | DHT11 Temperature & Humidity Sensor | 1 | [Adafruit](https://www.adafruit.com/product/386) |
| Display | 16x2 Character LCD (HD44780) | 1 | [Adafruit](https://www.adafruit.com/product/181) |
| LEDs | 5mm LEDs (Red, Yellow, Green) | 3 | [Amazon](https://www.amazon.com/eBoot-Pieces-Emitting-Diodes-Assorted/dp/B06XPV4CSH) |
| Buzzer | Active Buzzer 5V | 1 | [Amazon](https://www.amazon.com/MCIGICM-Terminals-Electronic-Computers-Printers/dp/B07FCDBBXJ) |
| Push Button | Tactile Push Button 12mm | 1 | [Adafruit](https://www.adafruit.com/product/1119) |
| Resistors | 220Ω Resistors (for LEDs) | 3 | [Amazon](https://www.amazon.com/EDGELEC-Resistor-Tolerance-Resistance-Optional/dp/B07QG1V4BK) |
| Breadboard | 830 Point Solderless Breadboard | 1 | [Adafruit](https://www.adafruit.com/product/239) |
| Jumper Wires | Male-to-Male/Male-to-Female | 1 set | [Amazon](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY) |
| Power Supply | 5V 3A USB-C Power Supply | 1 | [Adafruit](https://www.adafruit.com/product/4298) |
| MicroSD Card | 32GB MicroSD Card Class 10 | 1 | [Amazon](https://www.amazon.com/SanDisk-Ultra-microSDHC-Memory-Adapter/dp/B08GY9NYRM) |

**Estimated Total Cost**: ~$150-200 USD

## Wiring Diagram

### GPIO Pin Assignments

| Component | GPIO Pin | Physical Pin | Notes |
|-----------|----------|--------------|-------|
| PIR Motion Sensor | GPIO 4 | Pin 7 | Signal output |
| DHT11 Sensor | GPIO 5 | Pin 29 | Data line |
| LCD RS | GPIO 23 | Pin 16 | Register select |
| LCD Enable | GPIO 24 | Pin 18 | Enable signal |
| LCD D4 | GPIO 6 | Pin 31 | Data bit 4 |
| LCD D5 | GPIO 13 | Pin 33 | Data bit 5 |
| LCD D6 | GPIO 19 | Pin 35 | Data bit 6 |
| LCD D7 | GPIO 26 | Pin 37 | Data bit 7 |
| Button | GPIO 12 | Pin 32 | Pull-up resistor |
| Buzzer | GPIO 18 | Pin 12 | PWM capable |
| Green LED | GPIO 16 | Pin 36 | Via 220Ω resistor |
| Yellow LED | GPIO 20 | Pin 38 | Via 220Ω resistor |
| Red LED | GPIO 21 | Pin 40 | Via 220Ω resistor |
| RFID SDA | GPIO 8 (CE0) | Pin 24 | SPI chip select |
| RFID SCK | GPIO 11 (SCLK) | Pin 23 | SPI clock |
| RFID MOSI | GPIO 10 (MOSI) | Pin 19 | SPI data out |
| RFID MISO | GPIO 9 (MISO) | Pin 21 | SPI data in |
| RFID RST | GPIO 25 | Pin 22 | Reset (optional) |

### Schematic Diagram

```
                    Raspberry Pi 4
                    ┌────────────┐
                    │            │
    PIR ────────────┤ GPIO 4     │
    DHT11 ──────────┤ GPIO 5     │
                    │            │
    Button ─────────┤ GPIO 12    │
    Buzzer ─────────┤ GPIO 18    │
                    │            │
    Green LED ──────┤ GPIO 16    │
    Yellow LED ─────┤ GPIO 20    │
    Red LED ────────┤ GPIO 21    │
                    │            │
    LCD RS ─────────┤ GPIO 23    │
    LCD EN ─────────┤ GPIO 24    │
    LCD D4 ─────────┤ GPIO 6     │
    LCD D5 ─────────┤ GPIO 13    │
    LCD D6 ─────────┤ GPIO 19    │
    LCD D7 ─────────┤ GPIO 26    │
                    │            │
    RFID SDA ───────┤ GPIO 8     │
    RFID SCK ───────┤ GPIO 11    │
    RFID MOSI ──────┤ GPIO 10    │
    RFID MISO ──────┤ GPIO 9     │
    RFID RST ───────┤ GPIO 25    │
                    │            │
    Camera ─────────┤ CSI Port   │
                    │            │
    GND ────────────┤ GND        │
    5V ─────────────┤ 5V         │
    3.3V ───────────┤ 3.3V       │
                    └────────────┘

LED Connections (each):
GPIO Pin ──── 220Ω Resistor ──── LED Anode ──── Cathode ──── GND

Button Connection:
GPIO 12 ──── Button ──── GND (Internal pull-up enabled)
```

### Photos

<img width="4032" height="2268" alt="image" src="https://github.com/user-attachments/assets/7d52df6d-9563-435a-bb08-734f144d5d14" />



## Setup Instructions

### 1. Operating System Preparation

```bash
# Flash Raspberry Pi OS (64-bit) to microSD card using Raspberry Pi Imager
# Boot the Pi and run initial updates
sudo apt update && sudo apt upgrade -y

# Enable required interfaces
sudo raspi-config
# Navigate to: Interface Options
# Enable: Camera, SPI, I2C

# Reboot to apply changes
sudo reboot
```

### 2. Install System Dependencies

```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Install system libraries
sudo apt install libgpiod2 python3-libgpiod -y
sudo apt install python3-picamera2 -y
sudo apt install libcap-dev -y

# Install SPI and I2C tools
sudo apt install python3-spidev python3-smbus i2c-tools -y

# Install OpenCV dependencies
sudo apt install libatlas-base-dev libhdf5-dev libhdf5-serial-dev libjasper-dev libqtgui4 libqt4-test -y
```

### 3. Project Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/iot-home-defense-system.git
cd iot-home-defense-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Install Python Dependencies

Create a `requirements.txt` file:

```txt
python-dotenv==1.0.0
paho-mqtt==1.6.1
adafruit-circuitpython-dht==3.7.8
adafruit-circuitpython-charlcd==3.4.5
picamera2==0.3.12
opencv-python==4.8.1.78
spidev==3.6
mfrc522==0.0.7
```

Install:
```bash
pip install -r requirements.txt
```

### 5. Environment Variables

Create a `.env` file in the project root:

```bash
# LED Configuration
LED_BLINK_INTERVAL=0.5

# Timing Configuration (seconds)
DETECTION_DELAY=10
ALARM_DELAY=15

# MQTT Configuration
MQTT_HOST=io.adafruit.com
MQTT_PORT=1883
MQTT_TIMEOUT=60
MQTT_USERNAME=your_adafruit_username
MQTT_KEY=your_adafruit_io_key
TOPICS=alarm-status,temperature

# Camera Configuration
IMAGE_LOCATION=/home/pi/alarm_images
```

### 6. Create Required Directories

```bash
# Create image storage directory
mkdir -p /home/pi/alarm_images
chmod 755 /home/pi/alarm_images

# Create log directory
mkdir -p /home/pi/alarm_system/logs
```

### 7. Configure RFID Keys

```bash
# Run the RFID enrollment script
python3 utils/enroll_rfid.py

# Follow prompts to scan and register authorized RFID cards
```

## How to Run

### Manual Execution

```bash
# Activate virtual environment
source venv/bin/activate

# Run the main program
python3 main.py
```

### Run as System Service

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/alarm-system.service
```

Add the following content:

```ini
[Unit]
Description=IoT Home Defense Alarm System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/iot-home-defense-system
Environment="PATH=/home/pi/iot-home-defense-system/venv/bin"
ExecStart=/home/pi/iot-home-defense-system/venv/bin/python3 main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable alarm-system.service

# Start the service
sudo systemctl start alarm-system.service

# Check status
sudo systemctl status alarm-system.service

# View logs
journalctl -u alarm-system.service -f
```

### Dashboard Access

**Adafruit IO Dashboard**: `https://io.adafruit.com/{your_username}/dashboards`

Create feeds for:
- `alarm-status`: Displays current system state
- `temperature`: Shows real-time temperature readings

### CLI Commands

```bash
# Start the system
sudo systemctl start alarm-system.service

# Stop the system
sudo systemctl stop alarm-system.service

# Restart the system
sudo systemctl restart alarm-system.service

# View real-time logs
journalctl -u alarm-system.service -f

# View recent logs
journalctl -u alarm-system.service -n 100

# Check system status
sudo systemctl status alarm-system.service
```

## Data Format Specification

### CSV Log Files

The system generates two CSV files for data logging:

#### 1. `alarm-status.csv`

Records all system state changes.

**Fields**:
- `timestamp` (ISO 8601 format): Date and time of state change
- `message` (string): System state value

**States**:
- `disarmed`: System inactive
- `arming`: Countdown active
- `armed`: Motion detection enabled
- `disarming`: User authentication in progress
- `alert`: Alarm triggered

**Example**:
```csv
timestamp,message
2025-11-04T14:23:15.123456,disarmed
2025-11-04T14:25:30.654321,arming
2025-11-04T14:25:45.789012,armed
2025-11-04T14:30:12.345678,disarming
2025-11-04T14:30:15.901234,alert
```

#### 2. `temperature.csv`

Records temperature readings from DHT11 sensor.

**Fields**:
- `timestamp` (ISO 8601 format): Date and time of reading
- `message` (float): Temperature in Celsius

**Units**: Degrees Celsius (°C)

**Example**:
```csv
timestamp,message
2025-11-04T14:23:15.123456,22.0
2025-11-04T14:23:20.234567,22.5
2025-11-04T14:23:25.345678,23.0
```

### Image/Video Files

**Photo Naming Convention**:
```
disarmed_YYYYMMDD_HHMMSS.jpg
```
- Captured when system is successfully disarmed
- Stores in `/home/pi/alarm_images/`

**Video Naming Convention**:
```
alert_YYYYMMDD_HHMMSS.mp4
```
- Recorded during alert state
- Continues until system is disarmed
- Stores in `/home/pi/alarm_images/`

### File Rotation Policy

**CSV Files**:
- No automatic rotation implemented
- Manual archival recommended monthly
- Suggested script for monthly rotation:

```bash
#!/bin/bash
# Add to crontab: 0 0 1 * * /home/pi/rotate_logs.sh

DATE=$(date +%Y%m)
cd /home/pi/iot-home-defense-system

# Archive CSV files
mkdir -p archives/$DATE
mv alarm-status.csv archives/$DATE/alarm-status-$DATE.csv
mv temperature.csv archives/$DATE/temperature-$DATE.csv

# Compress archives older than 3 months
find archives/* -type d -mtime +90 -exec tar -czf {}.tar.gz {} \; -exec rm -rf {} \;
```

**Media Files**:
- Images and videos accumulate in `/home/pi/alarm_images/`
- Recommended: Review and archive weekly
- Suggested cleanup for files older than 30 days:

```bash
# Delete media files older than 30 days
find /home/pi/alarm_images -type f -mtime +30 -delete
```

## Known Limitations

### Hardware Limitations

1. **PIR Sensor Sensitivity**
   - Fixed detection range (~7 meters)
   - Cannot distinguish between authorized and unauthorized movement
   - Sensitive to temperature changes and small animals
   - 2-second minimum interval between detections

2. **DHT11 Accuracy**
   - Temperature accuracy: ±2°C
   - Humidity not currently utilized
   - Slow response time (~2 seconds per reading)

3. **Camera Module**
   - Requires adequate lighting for quality capture
   - Fixed position limits coverage area
   - Video files can be large (no compression implemented)

4. **RFID Reader**
   - Limited read range (~3-5cm)
   - Only supports MIFARE Classic cards
   - No encryption on stored card IDs

### Software Limitations

1. **Single User Authentication**
   - No multi-user support
   - All authorized RFID cards have equal access
   - No logging of which specific card was used

2. **Network Dependency**
   - MQTT failures don't prevent local operation but lose remote monitoring
   - No automatic reconnection with exponential backoff
   - No offline queueing of messages

3. **Error Handling**
   - Limited recovery from hardware disconnections
   - Camera failures don't gracefully degrade
   - No watchdog timer for system hangs

4. **Storage Management**
   - No automatic cleanup of old images/videos
   - CSV files grow indefinitely
   - No disk space monitoring

5. **Security Concerns**
   - MQTT credentials stored in plaintext `.env` file
   - RFID card IDs not encrypted
   - No tamper detection on physical components
   - Camera images not encrypted at rest

## Future Work

### Short-term Enhancements (1-3 months)

1. **Improved Authentication**
   - Multi-user RFID support with individual codes
   - PIN pad backup authentication method
   - Logging of specific user access events
   - Duress code feature to silently alert authorities

2. **Enhanced Monitoring**
   - Web dashboard for real-time status
   - Mobile app notifications via MQTT/push services
   - Email alerts with attached photos
   - SMS alerts for critical events

3. **Better Error Handling**
   - Automatic MQTT reconnection with exponential backoff
   - Graceful degradation when components fail
   - Hardware watchdog timer integration
   - Self-diagnostic on startup

4. **Storage Management**
   - Automatic file rotation and archiving
   - Disk space monitoring with alerts
   - Video compression to reduce storage
   - Cloud backup integration (AWS S3, Google Drive)

### Medium-term Goals (3-6 months)

1. **AI/ML Integration**
   - Person detection using TensorFlow Lite
   - Facial recognition for known individuals
   - Anomaly detection in motion patterns
   - False alarm reduction through learning

2. **Multiple Zones**
   - Support for multiple PIR sensors
   - Zone-based arming (e.g., perimeter only)
   - Different alert levels per zone
   - Chaining multiple Raspberry Pis

3. **Advanced Camera Features**
   - Pan-tilt mechanism for wider coverage
   - Night vision using IR camera
   - Motion-based tracking
   - Time-lapse recording

4. **Enhanced Security**
   - Encrypted MQTT communication (TLS)
   - Encrypted storage of credentials
   - Hardware security module (HSM) for key storage
   - Tamper detection on enclosure

### Long-term Vision (6-12 months)

1. **Professional Features**
   - Integration with professional monitoring services
   - Z-Wave/Zigbee integration for smart home
   - Voice control via Alexa/Google Assistant
   - Geofencing for automatic arm/disarm

2. **Distributed System**
   - Multi-location support with central dashboard
   - Peer-to-peer alerting between systems
   - Mesh network for sensor communication
   - Edge computing for local AI processing

3. **Compliance & Standards**
   - UL/CE certification for alarm systems
   - GDPR compliance for data storage
   - AES-256 encryption throughout
   - Professional installer mode

4. **Business Model**
   - Subscription service for cloud features
   - Professional installation option
   - Insurance integration for discounts
   - Open API for third-party integrations

## Troubleshooting

### Common Issues

**System won't start**:
```bash
# Check service status
sudo systemctl status alarm-system.service

# Check for Python errors
python3 main.py

# Verify GPIO permissions
sudo usermod -a -G gpio,spi,i2c pi
```

**RFID not reading**:
```bash
# Test SPI interface
ls -l /dev/spidev*

# Check connections
python3 -c "from mfrc522 import SimpleMFRC522; reader = SimpleMFRC522(); print('Place card...'); print(reader.read())"
```

**Camera not working**:
```bash
# Test camera
libcamera-still -o test.jpg

# Check camera enabled
sudo raspi-config
```

**MQTT not connecting**:
- Verify credentials in `.env`
- Check network connectivity: `ping io.adafruit.com`
- Review firewall rules

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- Adafruit for CircuitPython libraries and tutorials
- Raspberry Pi Foundation for hardware documentation
- MFRC522 library contributors
- IoT community for inspiration and support
