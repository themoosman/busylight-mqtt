import os

# General Settings
LOG_FILENAME = "/var/log/busylight_mqtt_server.log"
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.environ.get('LOG_FORMAT', '%(asctime)-15s %(levelname)-8s %(message)s')

# MQTT
MQTT_HOST = os.environ.get('MQTT_HOST', '127.0.0.1')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_TOPIC = os.environ.get('MQTT_TOPIC', 'homeassistant/lights/busylight/state')
MQTT_TLS = (os.getenv('MQTT_TLS', 'False') == 'True')
MQTT_CERT = os.environ.get('MQTT_CERT', 'bundle.crt')
