import logging
from datetime import datetime

from google.appengine.ext import ndb
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
    logging.info("device_heartbeat_status_sweep run at {0}".format(current_time))


def device_threshold_sweep():
    query = ChromeOsDevice.query(ChromeOsDevice.up == True)
    devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE)
    current_time = datetime.utcnow()
    deferred.defer(sweep_devices_for_exceeding_thresholds, devices=devices, current_time=current_time, _queue='device-monitor', _countdown=5)
    while more is True:
        devices, cursor, more = query.fetch_page(page_size=config.DEVICE_SWEEP_PAGING_SIZE, start_cursor=cursor)
        deferred.defer(sweep_devices_for_exceeding_thresholds, devices=devices, current_time=current_time, _queue='device-monitor',
                       _countdown=5)
    logging.info("device_heartbeat_threshold_sweep run at {0}".format(current_time))


def sweep_devices_for_responsiveness(devices, current_time):
    for device in devices:
        seconds = (current_time - device.heartbeat_updated).seconds
        if seconds > config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD:
            device.up = False
            device.put()
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
            logging.info("Down {0} seconds. device key = {1} and issue key = {2}.".format(seconds, device.key.urlsafe(),
                                                                                          issue.key.urlsafe()))


def sweep_devices_for_exceeding_thresholds(devices, current_time):
    for device in devices:
        if device.storage_utilization > config.STORAGE_UTILIZATION_THREHSHOLD:
            memory_high_issue = DeviceIssueLog.query(
                ndb.AND(DeviceIssueLog.device_key == device.key,
                        DeviceIssueLog.category == config.DEVICE_ISSUE_MEMORY_HIGH)).get(keys_only=True)
            memory_normal_issue = DeviceIssueLog.query(
                ndb.AND(DeviceIssueLog.device_key == device.key,
                        DeviceIssueLog.category == config.DEVICE_ISSUE_MEMORY_NORMAL)).get(keys_only=True)
            if memory_high_issue is None and memory_normal_issue is None:
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
                logging.info("Disk utilization alert. device key = {0} and issue key = {1}. Storage @ {2}%".format(
                    device.key.urlsafe(), issue.key.urlsafe(), device.storage_utilization))
        if device.memory_utilization > config.MEMORY_UTILIZATION_THREHSHOLD:
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
            logging.info("Memory utilization alert. device key = {0} and issue key = {1}. Memory @ {2}%".format(
                device.key.urlsafe(), issue.key.urlsafe(), device.memory_utilization))
