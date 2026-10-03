import time
import json
import paho.mqtt.client as mqtt

# Configuration
BROKER = "127.0.0.1"
PORT = 1884
USERNAME = "light_device"
PASSWORD = "light123"
DEVICE_ID = "LIGHT-001"

COMMAND_TOPIC = "iot/building/light/command"
STATUS_TOPIC = "iot/building/light/status"

# Initial State
current_status = "OFF"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("[MQTT] CONNECTED")
        client.subscribe(COMMAND_TOPIC)
        print(f"[MQTT] Subscribed to {COMMAND_TOPIC}")
        publish_status(client)
    else:
        print(f"[MQTT] Connection failed: {reason_code}")

def on_message(client, userdata, msg):
    global current_status
    print(f"\n[MQTT] Command received on {msg.topic}:")
    try:
        payload = msg.payload.decode("utf-8")
        print(payload)
        data = json.loads(payload)
        
        if data.get("deviceId") != DEVICE_ID:
            print("[DEVICE] Ignored command: Not for this device ID")
            return
            
        command = data.get("command")
        
        if command == "ON":
            if current_status != "ON":
                current_status = "ON"
                print("[DEVICE] Light turned ON.")
                publish_status(client)
            else:
                print("[DEVICE] Light is already ON.")
        elif command == "OFF":
            if current_status != "OFF":
                current_status = "OFF"
                print("[DEVICE] Light turned OFF.")
                publish_status(client)
            else:
                print("[DEVICE] Light is already OFF.")
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
    print("      SMART LIGHT DEVICE        ")
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
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nShutting down device.")
        client.disconnect()
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    main()
