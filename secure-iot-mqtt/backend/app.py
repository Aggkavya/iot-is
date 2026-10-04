import os
import json
import time
from threading import Lock
from flask import Flask, request, jsonify, send_from_directory, Response
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__, static_folder='../frontend')

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "127.0.0.1")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1884))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "dashboard_user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "dash123")

# Global State
devices_state = {
    "DOOR-001": "UNKNOWN",
    "LIGHT-001": "UNKNOWN",
    "ALARM-001": "UNKNOWN"
}
state_lock = Lock()
security_logs = []

# SSE functionality
clients = []

def notify_clients():
    data = json.dumps({
        "type": "state_update",
        "devices": devices_state
    })
    for c in clients:
        c.append(data)

def log_security_event(client_identity, topic, action, result, reason):
    event = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "client": client_identity,
        "topic": topic,
        "action": action,
        "result": result,
        "reason": reason
    }
    security_logs.append(event)
    # Notify clients
    data = json.dumps({
        "type": "security_log",
        "event": event
    })
    for c in clients:
        c.append(data)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("[BACKEND] Connected to MQTT broker")
        client.subscribe("iot/building/+/status")
    else:
        print(f"[BACKEND] Connection failed: {reason_code}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"[BACKEND] Received status on {msg.topic}: {payload}")
    try:
        data = json.loads(payload)
        device_id = data.get("deviceId")
        status = data.get("status")
        
        if device_id:
            with state_lock:
                devices_state[device_id] = status
            notify_clients()
    except json.JSONDecodeError:
        pass

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="dashboard_backend")
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Start MQTT in a background thread
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"MQTT Connection Error: {e}")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/state')
def get_state():
    with state_lock:
        return jsonify(devices_state)

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    device = data.get("device")
    command = data.get("command")
    
    if not device or not command:
        return jsonify({"error": "Missing device or command"}), 400
        
    topic_map = {
        "door": "iot/building/door/command",
        "light": "iot/building/light/command",
        "alarm": "iot/building/alarm/command"
    }
    
    if device not in topic_map:
        return jsonify({"error": "Unknown device"}), 400
        
    topic = topic_map[device]
    device_ids = {
        "door": "DOOR-001",
        "light": "LIGHT-001",
        "alarm": "ALARM-001"
    }
    
    payload = json.dumps({
        "deviceId": device_ids[device],
        "command": command
    })
    
    # Log legitimate command
    log_security_event(MQTT_USERNAME, topic, "PUBLISH", "ALLOWED", "LEGITIMATE DASHBOARD COMMAND")
    
    mqtt_client.publish(topic, payload)
    return jsonify({"success": True, "message": f"Command sent to {device}"})

@app.route('/api/logs')
def get_logs():
    return jsonify(security_logs)

@app.route('/api/log_external', methods=['POST'])
def log_external():
    # Allow external entities (like attacker scripts) to report their attempts
    # so we can show them on the dashboard
    data = request.json
    log_security_event(
        data.get("client", "UNKNOWN"),
        data.get("topic", "UNKNOWN"),
        data.get("action", "PUBLISH"),
        data.get("result", "UNKNOWN"),
        data.get("reason", "REPORTED EVENT")
    )
    return jsonify({"success": True})

@app.route('/stream')
def stream():
    def event_stream():
        messages = []
        clients.append(messages)
        try:
            while True:
                if messages:
                    msg = messages.pop(0)
                    yield f"data: {msg}\n\n"
                time.sleep(0.1)
        finally:
            clients.remove(messages)
            
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
