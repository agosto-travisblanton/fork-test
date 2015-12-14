from app_config import config
from models import ChromeOsDevice, DeviceIssueLog

query = ChromeOsDevice.query().order(ChromeOsDevice.created)
devices = query.fetch(5)
print 'Device count = ' + str(len(devices))
for device in devices:
    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                  up=False,
                                  storage_utilization=50,
                                  memory_utilization=50,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  last_error=None,
                                  resolved=False)
    issue.put()
    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_STORAGE_LOW,
                                  up=False,
                                  storage_utilization=92,
                                  memory_utilization=50,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  last_error=None,
                                  resolved=False)
    issue.put()
    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                  up=False,
                                  storage_utilization=50,
                                  memory_utilization=93,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  last_error=None,
                                  resolved=False)
    issue.put()
