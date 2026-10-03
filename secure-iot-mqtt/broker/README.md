# Phase 1: MQTT Broker Setup

This directory contains the configuration files to run Mosquitto locally in two modes: Vulnerable and Protected.

## 1. Install Mosquitto
You need to install the Mosquitto broker on your machine if you haven't already.
Run this command in an Administrator PowerShell to install it via winget:
```powershell
winget install -e --id EclipseFoundation.Mosquitto
```
After installation, open a new terminal or add `C:\Program Files\mosquitto` to your PATH.

## 2. Set Up Users
Run the `setup_users.ps1` script to create the `password.txt` file containing the credentials for our project.
```powershell
.\setup_users.ps1
```

## 3. Start the Broker

### Vulnerable Mode
To start the broker in **Vulnerable Mode**, run:
```powershell
mosquitto -v -c mosquitto_vulnerable.conf
```
*Note: The `-v` flag enables verbose logging so you can see all connection and ACL evaluation events.*

### Protected Mode
To start the broker in **Protected Mode**, stop the vulnerable instance (Ctrl+C) and run:
```powershell
mosquitto -v -c mosquitto_protected.conf
```
