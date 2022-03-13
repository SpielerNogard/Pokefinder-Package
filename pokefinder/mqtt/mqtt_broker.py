"""Class to create an MQTT Broker"""
import os
import json
import paho.mqtt.client as mqtt
from pokefinder.logging.get_logger import get_logger

class MQTTBroker:
    """Class to create an MQTT Broker.

    Parameters
    ----------
    topic: str
        topic to subscribe to.

    """
    def __init__(self, topic:str):
        # create a logger
        self._logger = get_logger('info')
        # get all needed inforamtion to interact with mqtt
        self._broker_adress = os.environ.get('broker_adress')
        self._port = int(os.environ.get('broker_port'))
        self._topic = topic
        self._messages = []

    def on_connect(self,client, userdata, flags, rc):
        """Method that is called when the broker connects to server."""
        self._logger.info(f"Connected to MQTT Broker: {self._broker_adress}")
        client.subscribe(self._topic)

    def run(self):
        """Method to run the broker."""
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self._broker_adress, self._port)
        client.loop_forever()

    def on_message(self,client, userdata, message):
        """Method that is called whenever a new message is published in the topic"""
        msg = str(message.payload.decode("utf-8"))
        try:
            msg_object = json.loads(msg)
            self._messages.append(msg_object)
        except Exception as exc:
            self._logger.error(f'{self._topic}: Error while converting: {msg}')

    def next_message(self):
        """Method to get the next message in the queue."""
        if len(self._messages) >= 1:
            return self._messages.pop(0)
        return None
