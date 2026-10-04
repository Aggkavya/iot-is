# Wireshark Demonstration

To analyze the network traffic for this project, you can use Wireshark to observe the MQTT packets directly. 
*Note: We are not using TLS (encryption) for this educational demonstration specifically so the raw MQTT structure can be observed.*

### Steps to Capture:
1. Start Wireshark.
2. Select your loopback interface (e.g., `Adapter for loopback traffic capture` on Windows) since everything is running on `127.0.0.1`.
3. Apply the filter: `tcp.port == 1884` or `mqtt`.
4. Start capturing.
5. In your web dashboard, click **UNLOCK** on the door.
6. Run the **Attacker Script**.
7. Stop capturing.

### Expected Analysis:
- **Normal Command:** You will see a `Publish Message` packet sent from the Dashboard to the Broker, followed by another `Publish Message` packet routed from the Broker to the Door Device.
- **Vulnerable Attack:** You will see the attacker client send a `Connect Command`, followed by a `Publish Message` that the broker happily forwards to the Door Device.
- **Blocked Attack (Protected Mode):** Using MQTTv5, when the attacker publishes the payload, you will observe the broker returning a `PubAck` packet. If you inspect the `PubAck` payload in Wireshark, you will see the Reason Code `0x87 (Not authorized)`.

**Important Disclaimer:** Wireshark cannot see broker-side ACL evaluations directly. It only shows the consequence: either the broker routes the message to the end device, or it returns an error code (MQTTv5).
