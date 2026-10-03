# College Presentation / Viva Script

Use this guide to confidently explain your project to the evaluator.

## 1. Introduction: What is this project?
"Hello, my project is a **Secure MQTT-Based IoT Access Control System**. It demonstrates how easily an IoT smart building can be hacked if it relies solely on user authentication without proper topic-level authorization, and it demonstrates exactly how to fix it."

## 2. What is the Vulnerability? (The Flaw)
"In many IoT deployments, devices and users are given a username and password to connect to the MQTT broker. However, administrators often make the mistake of assuming that *Authentication* (proving who you are) is enough. 

The vulnerability here is **Missing Topic-Level Access Control (Broken Access Control)**. When a broker does not enforce an Access Control List (ACL), any connected client can publish messages to *any* topic on the network. This means a low-privileged user, or an attacker who managed to get a basic credential, can control devices they shouldn't have access to."

## 3. What Attack are we performing?
"We are performing an **Unauthorized Command Injection Attack**. 
In a normal scenario, only the official Dashboard should be allowed to publish commands (like `UNLOCK`) to the Smart Door topic (`iot/building/door/command`).

In my Vulnerable Demonstration, I act as an attacker using a low-privileged account (`attacker_test`). Even though I am not the Dashboard, I inject a JSON payload containing the `UNLOCK` command directly into the door's MQTT topic. Because the broker's ACL is missing or misconfigured, it blindly forwards my malicious command to the Door, and the physical door unlocks."

## 4. How are we solving it? (The Mitigation)
"We solve this by implementing strict **Identity-Based Authorization using MQTT Access Control Lists (ACL)**. 

We enforce the principle of **Least Privilege**. In the Protected mode, I configured the MQTT broker's ACL file so that:
- The Door Device is *only* allowed to read its own command topic.
- The Light Device is *only* allowed to read its own command topic.
- The Dashboard is allowed to write to all command topics.
- The Attacker is explicitly granted **zero** publish permissions to these critical topics.

Now, when the attacker attempts the exact same Command Injection, the MQTT broker inspects the packet against the ACL, immediately drops the unauthorized message, and returns an `MQTTv5 Error Code 135 (Not Authorized)`. The attack is stopped at the network edge, before the payload ever reaches the smart device."

## 5. Summary / Conclusion
"By building this project, I demonstrated that true IoT security requires both Authentication (identifying the client) and Authorization (verifying what the client is allowed to do). Without ACLs, the entire IoT network is vulnerable to lateral movement and command injection."
