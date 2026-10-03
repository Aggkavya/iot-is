# Experiment Report: Secure MQTT-Based IoT Access Control System

## 1. Aim of the Experiment
To design, implement, and analyze a secure Internet of Things (IoT) network using the MQTT protocol, specifically demonstrating an "Unauthorized Command Injection" attack against IoT devices and successfully mitigating it using broker-level Identity-Based Authorization (Access Control Lists).

## 2. Theoretical Background

### 2.1 The MQTT Protocol
MQTT (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe network protocol designed for constrained devices and low-bandwidth networks. 
*   **Publish/Subscribe Model:** Devices do not communicate directly. Instead, a central server (the Broker) receives messages from "Publishers" and routes them to interested "Subscribers".
*   **Topics:** Messages are routed based on "topics", which are hierarchical strings (e.g., `iot/building/door/command`).
*   **MQTTv5 Reason Codes:** The latest version of the protocol (MQTTv5) introduces detailed reason codes. For example, if a publish fails due to security restrictions, the broker returns a PUBACK packet with Reason Code `135` (Not Authorized).

### 2.2 Eclipse Mosquitto Broker
Mosquitto is a highly popular, open-source MQTT broker. It acts as the central hub of our IoT network. In this experiment, it handles two primary security mechanisms:
1.  **Authentication:** Verifying the identity of a device (checking `username` and `password` via `password_file`).
2.  **Authorization:** Verifying what an authenticated device is allowed to do (enforced via the `acl_file`).

### 2.3 The Vulnerability: Broken Access Control
In many real-world IoT deployments, administrators incorrectly assume that providing a device with a username and password (Authentication) is sufficient security. However, if the broker does not enforce an Access Control List (Authorization), *any* authenticated user can publish to *any* topic. 

### 2.4 The Attack: Unauthorized Command Injection
Exploiting Broken Access Control allows a low-privileged attacker (e.g., a compromised guest account or a thermometer device) to inject malicious payloads into critical control topics (e.g., sending an `UNLOCK` command to a smart door). Because the end-device blindly trusts the network, it executes the command, leading to physical security breaches.

## 3. Methodology & Implementation

The experiment was divided into two distinct environments to demonstrate the flaw and the fix.

### 3.1 Network Architecture
*   **IoT Devices:** Three Python-based MQTT clients simulating a Smart Door, Light, and Alarm. They subscribe to their respective `command` topics and publish their states to `status` topics.
*   **Dashboard:** A Flask-based web application acting as the legitimate Command Center.
*   **Attacker:** A malicious Python script acting as a rogue client on the network.

### 3.2 Phase 1: The Vulnerable Setup
The broker was configured with authentication (`password.txt`) but with a heavily flawed ACL (`acl_vulnerable.conf`). The attacker was given wildcard publish access (`topic write iot/building/+/command`). 
*   **Execution:** The attacker published a JSON payload `{"command": "UNLOCK"}` to the door's topic.
*   **Observation:** The broker routed the message. The door received it and physically unlocked, proving the vulnerability.

### 3.3 Phase 2: The Mitigation (Protected Setup)
The broker was restarted using a strict, Least Privilege ACL (`acl_protected.conf`). 
*   **Security Rule:** The attacker identity was explicitly granted zero write permissions to the command topics. The devices were restricted to only read their specific command topics.
*   **Execution:** The attacker attempted the exact same Command Injection attack.
*   **Observation:** The Mosquitto broker inspected the ACL, immediately dropped the malicious packet at the network edge, and returned an `MQTTv5 Error Code 135 (Not Authorized)` to the attacker. The smart door remained safely locked.

## 4. Results & Analysis

| Scenario | Attacker Action | Broker Response | End Device State | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Vulnerable Mode** | Publish `UNLOCK` | Routes message (RC: 0) | Unlocked | ❌ SYSTEM COMPROMISED |
| **Protected Mode** | Publish `UNLOCK` | Drops message (RC: 135) | Remained Locked | ✅ SYSTEM SECURE |

The implementation of `acl_protected.conf` successfully demonstrated that perimeter security (Broker-level ACLs) is mandatory. Relying on application-level security inside the constrained IoT devices is insufficient and dangerous.

## 5. Conclusion
This experiment successfully demonstrated that Authentication without Authorization provides a false sense of security in IoT networks. By leveraging MQTT Access Control Lists, we successfully mitigated Unauthorized Command Injection attacks, ensuring that even if an attacker compromises a low-privileged credential, they cannot perform lateral movement or control unauthorized infrastructure.
