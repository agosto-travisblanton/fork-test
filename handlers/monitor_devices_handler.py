from webapp2 import RequestHandler

from device_monitoring import device_heartbeat_sweep, device_threshold_sweep

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'
from extended_session_request_handler import ExtendedSessionRequestHandler


class MonitorDevicesHandler(ExtendedSessionRequestHandler):
    def last_contact_check(self):
        device_heartbeat_sweep()
        device_threshold_sweep()
        self.response.set_status(202, 'Accepted')
