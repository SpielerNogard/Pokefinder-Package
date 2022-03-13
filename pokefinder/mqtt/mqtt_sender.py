"""class to create an mqtt sender for a specific topic"""
import os
import json
import paho.mqtt.client as mqtt
from pokefinder.logging.get_logger import get_logger


class MQTTSender:
    """class to create a nmqtt sender for a specific topic.

    Parameters
    ----------
    topic: str
        topic to subscribe to.
    """
    def __init__(self,topic):
        self._logger = get_logger('info')
        self._topic = topic

        self._client = mqtt.Client()
        self._qos = int(os.environ.get('broker_qos'))
        self._broker_adress = os.environ.get('broker_adress')
        self._port = int(os.environ.get('broker_port'))
        self._client.connect(self._broker_adress, self._port)
        self._logger.info(f"Connected to MQTT Broker: {self._broker_adress}")

    def send_message(self,message:dict):
        """Method to send a message to topic.
        Parameters
        ----------
        message: dict
            message to send to mqtt server
        """
        self._client.publish(self._topic, json.dumps(message), qos=self._qos)
        self._client.loop()
        self._logger.info(f"{message} sended to {self._topic}")

