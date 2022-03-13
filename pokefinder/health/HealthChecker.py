"""Class to create an Health Sender Thread"""
import datetime
import time
from threading import Thread
from pokefinder.logging.get_logger import get_logger
from pokefinder.mqtt.mqtt_sender import MQTTSender

class HealthChecker:
    """Class to create an HealthChecker. and send alive signals"""
    def __init__(self,module_name):
        self._name = module_name
        self._run = True
        self._sender = MQTTSender('healthcheck/in')
        self._logger = get_logger('INFO')

    def run(self):
        """Method to start sending health signals every 10 mins"""
        while self._run is True:
            now = datetime.datetime.now()
            message_info = {'message_type':'health_check',
                            'module':self._name,
                            'time':now.isoformat()}
            self._sender.send_message(message_info)
            self._logger.info(f'sending health for {self._name}')
            time.sleep(10*60)

def start_health_check(name):
    """Method to create a deamon thread to run the health check"""
    health = HealthChecker(name)

    def run_health_check():
        health.run()
    
    def start_health_thread():
        health_check = Thread(name='HealthChecker', target=run_health_check)
        health_check.daemon = True
        health_check.start()

    start_health_thread()
    