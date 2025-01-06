import os

# General Settings
LOG_FILENAME = "/var/log/busylight_mqtt_server.log"
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.environ.get('LOG_FORMAT', '%(message)s')

# MQTT
MQTT_HOST = os.environ.get('MQTT_HOST', 'mqtt.apps.example.com')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 8883))
MQTT_TOPIC = os.environ.get('MQTT_TOPIC', 'homeassistant/lights/busylight/state')
