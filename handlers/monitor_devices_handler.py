from webapp2 import RequestHandler

from decorators import requires_api_token
from device_monitoring import device_heartbeat_sweep, device_threshold_sweep

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class MonitorDevicesHandler(RequestHandler):
    @requires_api_token
    def last_contact_check(self):
        device_heartbeat_sweep()
        device_threshold_sweep()
        self.response.set_status(202, 'Accepted')
