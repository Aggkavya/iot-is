# Viva Questions & Answers

**Q: What is IoT?**
A: The Internet of Things is a network of physical objects embedded with sensors, software, and networking capabilities to connect and exchange data over the internet.

**Q: Why MQTT is commonly used in IoT?**
A: It is lightweight, uses a publish/subscribe model, requires minimal network bandwidth, and supports varying levels of Quality of Service (QoS), making it ideal for constrained devices.

**Q: What are publishers and subscribers?**
A: Publishers send messages to a central broker on a specific "topic", and subscribers tell the broker they want to receive messages from a specific "topic". They never connect directly to each other.

**Q: What is a topic?**
A: A string representing a routing path for a message (e.g., `iot/building/door/command`).

**Q: What is an MQTT broker?**
A: A central server that receives all published messages and routes them to the correct subscribers based on their topic subscriptions.

**Q: What is authentication?**
A: The process of verifying the identity of a client (e.g., checking a username and password).

**Q: What is authorization (and ACL)?**
A: Authorization determines *what* an authenticated identity is allowed to do. An Access Control List (ACL) explicitly defines which users can read/write to which topics.

**Q: What is an unauthorized command injection attack?**
A: When a malicious actor publishes a command to an IoT device's control topic without having the proper authorization to do so, causing the device to execute an unintended physical action.

**Q: Why should every IoT device have separate credentials?**
A: This enforces the principle of "Least Privilege". If an attacker steals the Light's credentials, they can only control the Light, not the Door or the Alarm.

**Q: What does Wireshark demonstrate here?**
A: Wireshark captures the exact TCP/IP packets between the MQTT clients and the broker. It demonstrates the raw MQTT protocol behavior (e.g. `Connect`, `Publish`, and `PubAck`) and proves that the message is actually transmitted over a network.
