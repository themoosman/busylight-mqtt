# BlyncLight MQTT Server
This is a program to automate updating an [Embrava BlyncLight](https://embrava.com/collections/blynclight-series).  This is intended to make the BlyncLight a network light and have its status updated by reading an MQTT topic. 

## Why
The ultimate goal is to control the light from Home Assistant.

## Requirements
This application uses the [BusyLight for Humans](https://pypi.org/project/busylight-for-humans/) Python package to make the device calls.


## MQTT
This deployment requires an MQTT server as it will update it config from the subscribed topic.


## Install

### Required Packages

1) Install the necessary Python packages
````bash
python3 -m pip install -r requirements.txt
````

### Create environment file
The application needs a set of environment variables to run correctly.  Copy the `service.env.sample` to `service.env` and update the values to match your environment.

### Service
The Python app can be run as a service.  See the instructions in the `.service` files for instructions.

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `LOG_FILENAME` | Location of log file | `/var/log/busylight_mqtt_server.log` |
| `LOG_LEVEL` | Sets the level of logging | `INFO` |
| `LOG_FORMAT` | Log file format | `%(message)s` |
| `MQTT_HOST` | Hostname of port of the MQTT server | `mqtt.apps.example.com` |
| `MQTT_PORT` | Port of the MQTT server | `1883` |
| `MQTT_TOPIC` | MQTT topic to monitor for state | `homeassistant/lights/busylight/state` |

## Home Assistant Integrations

### Sensors

TODO

## TODO

1. Containerize this deployment