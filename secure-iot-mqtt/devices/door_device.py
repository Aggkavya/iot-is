import time
import json
import paho.mqtt.client as mqtt

# Configuration
BROKER = "127.0.0.1"
PORT = 1884
USERNAME = "door_device"
PASSWORD = "door123"
DEVICE_ID = "DOOR-001"

COMMAND_TOPIC = "iot/building/door/command"
STATUS_TOPIC = "iot/building/door/status"

# Initial State
current_status = "LOCKED"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("[MQTT] CONNECTED")
        # Subscribe to command topic
        client.subscribe(COMMAND_TOPIC)
        print(f"[MQTT] Subscribed to {COMMAND_TOPIC}")
        publish_status(client)
    else:
        print(f"[MQTT] Connection failed with reason code: {reason_code}")

def on_message(client, userdata, msg):
    global current_status
    print(f"\n[MQTT] Command received on {msg.topic}:")
    try:
        # Expecting JSON payload
        payload = msg.payload.decode("utf-8")
        print(payload)
        
        data = json.loads(payload)
        
        if data.get("deviceId") != DEVICE_ID:
            print("[DEVICE] Ignored command: Not for this device ID")
            return
            
        command = data.get("command")
        
        if command == "UNLOCK":
            if current_status != "UNLOCKED":
                current_status = "UNLOCKED"
                print("[DEVICE] Door unlocked.")
                publish_status(client)
            else:
                print("[DEVICE] Door is already unlocked.")
        elif command == "LOCK":
            if current_status != "LOCKED":
                current_status = "LOCKED"
                print("[DEVICE] Door locked.")
                publish_status(client)
            else:
                print("[DEVICE] Door is already locked.")
        else:
            print(f"[DEVICE] Unknown command: {command}")
            
    except json.JSONDecodeError:
        print("[DEVICE] Error: Payload must be valid JSON")

def publish_status(client):
    status_payload = json.dumps({
        "deviceId": DEVICE_ID,
        "status": current_status
    })
    client.publish(STATUS_TOPIC, status_payload)
    print(f"[DEVICE] Publishing status: {current_status} to {STATUS_TOPIC}")

def main():
    print("================================")
    print("       SMART DOOR DEVICE        ")
    print("================================")
    print(f"Device ID: {DEVICE_ID}")
    print(f"Status:    {current_status}")
    print("Waiting for connection...")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=DEVICE_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    # Start loop
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nShutting down device.")
        client.disconnect()

if __name__ == "__main__":
    main()
