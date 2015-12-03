import logging
from datetime import datetime

from google.appengine.ext.deferred import deferred

from app_config import config
from models import ChromeOsDevice, DeviceIssueLog

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def device_heartbeat_status_sweep():
    query = ChromeOsDevice.query(ChromeOsDevice.up == True)
    devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE)
    current_time = datetime.utcnow()
    deferred.defer(__sweep_devices, devices=devices, current_time=current_time, _queue='device-monitor', _countdown=5)
    while more is True:
        devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE, start_cursor=cursor)
        deferred.defer(__sweep_devices, devices=devices, current_time=current_time, _queue='device-monitor',
                       _countdown=5)


def __sweep_devices(devices, current_time):
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
