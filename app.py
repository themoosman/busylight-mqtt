#!/usr/bin/python3

import logging
import logging.handlers as handlers
import sys
import os
import traceback
import app_cfg as cfg
import paho.mqtt.client as mqtt
import json
from blynclightrunner import BlyncLightRunner

logger = logging.getLogger(__name__)
light = BlyncLightRunner(logger)


def setup_logger():
    rootLogger = logging.getLogger()
    # Set up logging
    log_level = logging.getLevelName(cfg.LOG_LEVEL)
    rootLogger.setLevel(log_level)

    if "TTY" in os.environ:
        logging.basicConfig(format=cfg.LOG_FORMAT, level=log_level)
    else:
        if sys.stdout.isatty():
            # Connected to a real terminal - log to stdout
            logging.basicConfig(format=cfg.LOG_FORMAT, level=log_level)
        else:
            # Add the log message handler to the logger
            logHandler = handlers.TimedRotatingFileHandler(
                filename=cfg.LOG_FILENAME, when="D", interval=1, backupCount=2)
            logHandler.setLevel(log_level)
            logFormatter = logging.Formatter(cfg.LOG_FORMAT)
            logHandler.setFormatter(logFormatter)
            if not rootLogger.handlers:
                rootLogger.addHandler(logHandler)

    logger = logging.getLogger(__name__)

    logger.info("Log setup complete")

    return logger


def on_connect(client, userdata, flags, rc):
    logger.debug("Connected with result code {0}".format(str(rc)))
    client.subscribe((cfg.MQTT_TOPIC, 0))


def on_disconnect(client, userdata, rc):
    logger.info("client disconnected ok")


def on_message(client, userdata, msg):
    try:
        logger.info("Message received-> " + msg.topic + " " + str(msg.payload))
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        logger.debug("data Received type %s" % type(m_decode))
        logger.debug("data Received: %s" % m_decode)
        m_in = json.loads(m_decode)

        logger.debug("color_name: %s" % m_in["color_name"])
        logger.debug("flash: %s" % m_in["flash"])
        logger.debug("on: %s" % m_in["on"])
        logger.debug("speed: %s" % m_in["speed"])

        status = int(m_in["on"])

        if status == 0:
            logger.debug("hit off")
            light.on = False
        else:
            logger.debug("hit on")
            light.flash = int(m_in["flash"])
            light.flashspeed = int(m_in["speed"])
            light.colorname = str(m_in["color_name"])
            light.on = True

    except Exception as ex:
        logger.error(ex)


# App entry point.
if __name__ == "__main__":
    try:
        logger = setup_logger()
        logger.info("==========================================================")
        logger.info("Starting Busy Light MQTT Server")
        # Server Properties
        try:
            # mqtt_connected = False
            mqtt_client = mqtt.Client(
                client_id="busylight_client", clean_session=False, protocol=mqtt.MQTTv311, transport="tcp")

            # Setup MQTT client connection to the broker
            mqtt_broker_host = cfg.MQTT_HOST
            mqtt_port = cfg.MQTT_PORT
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message
            mqtt_client.on_disconnect = on_disconnect
            cert_path = "%s%s%s" % (str(os.path.dirname(os.path.abspath(
                __file__))), "/certs/", "bundle.crt")
            mqtt_client.tls_set(ca_certs=cert_path, tls_version=2)
            mqtt_client.tls_insecure_set(True)
            mqtt_client.connect(mqtt_broker_host, mqtt_port, keepalive=60)
            mqtt_client.loop_forever()  # Start networking daemon
        except Exception:
            logging.error("Unexpected error: %s", sys.exc_info()[0])
            logging.error("%s", traceback.format_exc())
            light.on = False

    except KeyboardInterrupt:
        try:
            logging.debug("Caught KeyboardInterrupt Exception")
            light.on = False
        except Exception:
            logging.critical("Unable to reset light")
            logging.critical("Terminating due to keyboard interrupt")
    except Exception:
        try:
            logging.debug("Caught Exception")
            light.on = False
        except Exception:
            logging.critical("Unable to reset light")
        logging.critical("Terminating due to unexpected error: %s", sys.exc_info()[0])
    finally:
        try:
            logging.debug("Caught finally")
            light.on = False
        except Exception:
            logging.critical("Terminating due to unexpected error: %s", sys.exc_info()[0])
