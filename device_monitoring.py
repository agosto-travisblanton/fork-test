import logging
from datetime import datetime

from app_config import config
from models import ChromeOsDevice, DeviceIssueLog

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def device_heartbeat_status_sweep():
    devices = ChromeOsDevice.query().fetch()
    current_time = datetime.utcnow()
    for device in devices:
        seconds = (current_time - device.heartbeat_updated).seconds
        if seconds > config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD:
            device.up = False
            device.put()
            issue = DeviceIssueLog.create(device_key=device.key,
                                          category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                          up=False,
                                          disk_utilization=device.disk_utilization,
                                          memory_utilization=device.memory_utilization,
                                          program=device.program,
                                          program_id=device.program_id,
                                          last_error=device.last_error)
            issue.put()
            logging.info("Down {0} seconds. device key = {1} and issue key = {2}.".format(seconds, device.key.urlsafe(),
                                                                                          issue.key.urlsafe()))
    logging.info("device_heartbeat_status_sweep run at {0}".format(current_time))
