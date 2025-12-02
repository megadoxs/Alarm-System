import paho.mqtt.client as mqtt
import csv
import os
from datetime import datetime

class MQTT_Controller:
    def __init__(self, broker, port, timeout, username, key, logs):
        try:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.username_pw_set(username, key)
            self.mqtt_client.connect(broker, port, timeout)
            self.mqtt_client.loop_start()
            self.connected = True
            self.username = username
            self.logs = logs
            self.mqtt_client.on_message = self._route_message
            self.callbacks = {}

        except Exception as e:
            self.connected = False

    def save(self, topic, message):
        if not self.connected:
            return False

        try:
            result, _ = self.mqtt_client.publish(f"{self.username}/feeds/{topic}", str(message))
            return result == mqtt.MQTT_ERR_SUCCESS
        except Exception:
            return False

    def _route_message(self, client, userdata, msg):
        cb = self.callbacks.get(msg.topic)
        if cb:
            try:
                cb(msg.payload.decode())
            except Exception:
                pass

    def sub(self, topic, callback):
        if not self.connected:
            return False

        try:
            full_topic = f"{self.username}/feeds/{topic}"

            # save callback for this topic
            self.callbacks[full_topic] = callback

            # subscribe normally
            result, _ = self.mqtt_client.subscribe(full_topic)
            return result == mqtt.MQTT_ERR_SUCCESS

        except Exception:
            return False
