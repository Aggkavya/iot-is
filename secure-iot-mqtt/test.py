import paho.mqtt.client as mqtt
import time

def on_publish(client, userdata, mid, reason_code, properties):
    print(f'reason_code is {reason_code}')
    print(f'reason_code.value is {getattr(reason_code, "value", reason_code)}')
    print(f'reason_code == 135? {reason_code == 135}')
    print(f'reason_code == 0? {reason_code == 0}')

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='test1', protocol=mqtt.MQTTv5)
client.username_pw_set('attacker_test', 'hacker123')
client.on_publish = on_publish
client.connect('127.0.0.1', 1883, 60)
client.loop_start()
client.publish('iot/building/door/command', 'msg', qos=1).wait_for_publish()
time.sleep(1)
