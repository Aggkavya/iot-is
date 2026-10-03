# Experiment & Demonstration Guide

When presenting this project to your professor or evaluator, the visual setup and the code you highlight are critical to proving you understand the core concepts. Follow this guide to ace your demonstration.

## 1. How to Setup Your Screen (The Visuals)
Don't just show them code! Set up your screen so they can see the attack happening in real-time.

*   **Left Half of Screen:** Open the web browser showing the **IoT Command Center Dashboard** (`http://localhost:5000`).
*   **Right Half of Screen (Top):** Place the terminal running the `attacker.py` script.
*   **Right Half of Screen (Bottom):** Show the Code Editor (VS Code) to point out specific files.

## 2. The 3 Crucial Files to Show (Code Walkthrough)

When the evaluator asks "Show me the code that makes this work", do not show them the frontend HTML or CSS. Show them these 3 specific backend/security files:

### A. The Core Vulnerability (The Device Script)
**File to open:** `devices/door_device.py`
**What to point at:** The `on_message` function (around line 30).
**What to say:** *"This is the Python code running on the physical Door. Notice that when it receives a message on its command topic, it blindly parses the JSON and executes `command == "UNLOCK"`. It does not check WHO sent the message. It entirely trusts the MQTT broker to secure the network."*

### B. The Mitigation (The ACL Files)
**Files to open:** `broker/acl_vulnerable.conf` AND `broker/acl_protected.conf`
**What to point at:** The `user attacker_test` block in both files.
**What to say:** *"Because the IoT devices blindly trust the network, the security MUST be enforced at the Broker. In the vulnerable file, you can see the attacker has `topic write iot/building/+/command` (Wildcard access). In the protected file, the attacker is explicitly given ZERO write permissions to those topics. This enforces the Principle of Least Privilege."*

### C. The Attack Mechanism & Detection
**File to open:** `attacker/attacker.py`
**What to point at:** The `on_publish` function (around line 30) where `reason_code == 135` is checked.
**What to say:** *"This is the attacker's script. We are utilizing MQTT version 5. When the attacker tries to publish an unauthorized command in Protected mode, the Mosquitto broker instantly drops the packet and returns an MQTTv5 Reason Code of `135`, which stands for 'Not Authorized'. You can see my Python code specifically catches this error code to log the blocked attack."*

## 3. The Live Demonstration Steps
1.  Use `control_panel.ps1` to start the **Vulnerable** environment.
2.  Show the dashboard and click a few buttons normally to prove the system works.
3.  Run the attacker script and choose **Attack A (Door)**. The door will unlock on the dashboard. Tell the evaluator: *"The attack succeeded because the broker lacked ACLs."*
4.  Stop everything and use the control panel to start the **Protected** environment.
5.  Run the attacker script again and choose **Attack A (Door)**. 
6.  Point to the dashboard where the red **BLOCKED** log appears, and point to the attacker terminal showing **[X] PUBLISH DENIED**. Tell the evaluator: *"The network edge successfully dropped the malicious command using Identity-Based Authorization."*
