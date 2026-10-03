# IoT MQTT Access Control Project

This repository demonstrates an Unauthorized Command Injection Attack against a Smart Building IoT infrastructure using MQTT, and how to mitigate it using proper Access Control Lists (ACL) and topic-level authorization.

## Project Structure
- `broker/`: Contains Mosquitto configurations (Vulnerable and Protected modes).
- `devices/`: Simulates real IoT devices (Door, Light, Alarm) using `paho-mqtt`.
- `backend/`: Flask web application for real-time monitoring.
- `frontend/`: Real-time dashboard for IoT Command Center.
- `attacker/`: Python scripts simulating the unauthorized command injection attack.
- `docs/`: Security and architectural documentation.

## Installation & Running
Read the detailed setup and run instructions in the `docs/` folder or follow the college 5-minute demonstration guide.

## How to Switch Modes
- **VULNERABLE MODE**: `mosquitto -v -c broker/mosquitto_vulnerable.conf`
- **PROTECTED MODE**: `mosquitto -v -c broker/mosquitto_protected.conf`
