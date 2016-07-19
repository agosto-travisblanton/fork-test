from app_config import config
from models import ChromeOsDevice, DeviceIssueLog

query = ChromeOsDevice.query().order(ChromeOsDevice.created)
devices = query.fetch(100)
print 'Device count = ' + str(len(devices))
for device in devices:
    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                  up=False,
                                  storage_utilization=50,
                                  memory_utilization=50,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  playlist='Some Playlist',
                                  playlist_id='Playlist Id #1234',
                                  last_error=None,
                                  resolved=False)
    issue.put()
    print 'Added ' + config.DEVICE_ISSUE_PLAYER_DOWN + ' issue to ' + device.key.urlsafe()

    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_STORAGE_LOW,
                                  up=True,
                                  storage_utilization=92,
                                  memory_utilization=50,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  playlist='Some Playlist',
                                  playlist_id='Playlist Id #1234',
                                  last_error=None,
                                  resolved=False)
    issue.put()
    print 'Added ' + config.DEVICE_ISSUE_STORAGE_LOW + ' issue to ' + device.key.urlsafe()

    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                  up=True,
                                  storage_utilization=50,
                                  memory_utilization=93,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  playlist='Some Playlist',
                                  playlist_id='Playlist Id #1234',
                                  last_error=None,
                                  resolved=False)
    issue.put()
    print 'Added ' + config.DEVICE_ISSUE_MEMORY_HIGH + ' issue to ' + device.key.urlsafe()

    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_PLAYER_UP,
                                  up=True,
                                  storage_utilization=44,
                                  memory_utilization=53,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  playlist='Some Playlist',
                                  playlist_id='Playlist Id #1234',
                                  last_error=None,
                                  resolved=True)
    issue.put()
    print 'Added ' + config.DEVICE_ISSUE_PLAYER_UP + ' issue to ' + device.key.urlsafe()

    issue = DeviceIssueLog.create(device_key=device.key,
                                  category=config.DEVICE_ISSUE_MEMORY_NORMAL,
                                  up=True,
                                  storage_utilization=44,
                                  memory_utilization=40,
                                  program='Test Content',
                                  program_id='Program Id #1213',
                                  playlist='Some Playlist',
                                  playlist_id='Playlist Id #1234',
                                  last_error=None,
                                  resolved=True)
    issue.put()
    print 'Added ' + config.DEVICE_ISSUE_MEMORY_NORMAL + ' issue to ' + device.key.urlsafe()