import logging
from datetime import datetime

from google.appengine.ext.deferred import deferred

from app_config import config
from models import ChromeOsDevice, DeviceIssueLog

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def device_heartbeat_sweep():
    query = ChromeOsDevice.query(ChromeOsDevice.up == True)
    devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE)
    current_time = datetime.utcnow()
    deferred.defer(sweep_devices_for_responsiveness, devices=devices, current_time=current_time, _queue='device-monitor', _countdown=5)
    while more is True:
        devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE, start_cursor=cursor)
        deferred.defer(sweep_devices_for_responsiveness, devices=devices, current_time=current_time, _queue='device-monitor',
                       _countdown=5)
    logging.info("Heartbeat sweep run at {0}".format(current_time))


def device_threshold_sweep():
    query = ChromeOsDevice.query(ChromeOsDevice.up == True)
    devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE)
    current_time = datetime.utcnow()
    deferred.defer(sweep_devices_for_exceeding_thresholds, devices=devices, current_time=current_time, _queue='device-monitor', _countdown=5)
    while more is True:
        devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE, start_cursor=cursor)
        deferred.defer(sweep_devices_for_exceeding_thresholds, devices=devices, current_time=current_time, _queue='device-monitor',
                       _countdown=5)
    logging.info("Threshold sweep run at {0}".format(current_time))


def sweep_devices_for_responsiveness(devices, current_time):
    for device in devices:
        seconds = (current_time - device.heartbeat_updated).seconds
        if seconds > config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD:
            device.up = False
            device.put()
            if DeviceIssueLog.no_matching_issues(device_key=device.key,
                                                 category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                                 up=False,
                                                 storage_utilization=device.storage_utilization,
                                                 memory_utilization=device.memory_utilization,
                                                 program=device.program):
                issue = DeviceIssueLog.create(device_key=device.key,
                                              category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                              up=False,
                                              storage_utilization=device.storage_utilization,
                                              memory_utilization=device.memory_utilization,
                                              program=device.program,
                                              program_id=device.program_id,
                                              last_error=device.last_error,
                                              resolved=False)
                issue.put()


def sweep_devices_for_exceeding_thresholds(devices, current_time):
    for device in devices:
        if device.storage_utilization > config.STORAGE_UTILIZATION_THRESHOLD:
            if DeviceIssueLog.no_matching_issues(device_key=device.key,
                                                 category=config.DEVICE_ISSUE_STORAGE_LOW,
                                                 up=True,
                                                 storage_utilization=device.storage_utilization,
                                                 memory_utilization=device.memory_utilization,
                                                 program=device.program):
                issue = DeviceIssueLog.create(device_key=device.key,
                                              category=config.DEVICE_ISSUE_STORAGE_LOW,
                                              up=True,
                                              storage_utilization=device.storage_utilization,
                                              memory_utilization=device.memory_utilization,
                                              program=device.program,
                                              program_id=device.program_id,
                                              last_error=device.last_error,
                                              resolved=False)
                issue.put()
        if device.memory_utilization > config.MEMORY_UTILIZATION_THRESHOLD:
            if DeviceIssueLog.no_matching_issues(device_key=device.key,
                                                 category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                                 up=True,
                                                 storage_utilization=device.storage_utilization,
                                                 memory_utilization=device.memory_utilization,
                                                 program=device.program):
                issue = DeviceIssueLog.create(device_key=device.key,
                                              category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                              up=True,
                                              storage_utilization=device.storage_utilization,
                                              memory_utilization=device.memory_utilization,
                                              program=device.program,
                                              program_id=device.program_id,
                                              last_error=device.last_error,
                                              resolved=False)
                issue.put()
