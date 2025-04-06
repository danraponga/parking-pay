import json
import paho.mqtt.client as mqtt
from config import config

def send_parking_command():
    client = mqtt.Client()
    client.username_pw_set(config.mqtt_username, config.mqtt_password)
    client.connect(config.mqtt_host, config.mqtt_port, 60)

    topic = "v2/2001315C7BCC/client/state/set"
    payload = {
        "request_id": 55234,
        "relay": [{"id": 0, "state": True}]
    }

    client.publish(topic, json.dumps(payload))
    client.disconnect()
