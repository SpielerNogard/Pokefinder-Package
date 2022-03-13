"""class to create a Commander to check messages for commands."""
import os
import time
from threading import Thread
from dotenv import load_dotenv

from pokefinder.mqtt.mqtt_broker import MQTTBroker
from pokefinder.logging.get_logger import get_logger
from pokefinder.user.user_manager import UserManager
from pokefinder.health.health_checker import start_health_check

load_dotenv()
class Commander:
    """Class to create a Commander.
    the Commander checks all messages for commands.
    if a command can be found he will use the method
    defined for this command."""
    def __init__(self):
        self._broker =  MQTTBroker('messages/in')
        self.start_broker()
        self._run = True
        self._logger = get_logger('INFO')
        self._user_manager = UserManager()
        start_health_check('command-modul')


    def create_answer_broker(self):
        """method to start the broker."""
        self._broker.run()

    def start_broker(self):
        """Method to create a broker thread and start the broker."""
        message_in = Thread(name="PokemonBroker", target=self.create_answer_broker)
        message_in.daemon = True
        message_in.start()

    def run(self):
        """Method to start the Commander"""
        while self._run is True:
            message = self._broker.next_message()
            if message is None:
                pass 
            else:
                print(message)
                self._check_message(message)

    def _check_message(self, message):
        """Method to check for new messages."""
        commands = {'!register':self._register,}
        if message.get('content').startswith('!'):
            for key in commands.keys():
                if message.get('content').startswith(key):
                    commands[key](message)
        else:
            print('no command found')

    def _register(self, message):
        """Methdo to register a new user"""
        self._user_manager.register_new_user(message.get('user'), 'test_user')
        
if __name__ == "__main__":
    cmd = Commander()
    cmd.run()
