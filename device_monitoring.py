import logging
from datetime import datetime

from app_config import config
from models import ChromeOsDevice

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def device_heartbeat_status_task():
    devices = ChromeOsDevice.query().fetch()
    current_time = datetime.utcnow()
    for device in devices:
        seconds = (current_time - device.heartbeat_updated).seconds
        if seconds > config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD:
            device.up = False
            device.put()
            logging.info("{0} seconds down for {1}.".format(seconds, device.key.urlsafe()))
        pass
    logging.info("Device heartbeat status task run at {0}".format(current_time))
