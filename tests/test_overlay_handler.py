import json
from models import Image, Overlay, ChromeOsDevice
from routes import application
from webtest import AppError

from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class OverlayHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(OverlayHandlerTest, self).setUp()
        self.svg_rep = "ffdkfdkfsklfsljkflksfjlkfsa"

    def test_post_overlay_fails_without_associated_image_key(self):
        uri = application.router.build(None, 'post-overlay', None, {})
        request_parameters = {
            "device_urlsafe_key": self.device_key.urlsafe(),
            "position": "TOP_LEFT",
            "overlay_type": "LOGO",
            "associated_image": None
        }
        with self.assertRaises(AppError) as cm:
            response = self.app.post_json(uri, params=request_parameters)
            self.assertEqual(response.status_int, 400)

    def _create_image(self):
        request_parameters = {'svg_rep': self.svg_rep}
        uri = application.router.build(None, 'post-image', None, {})
        response = self.app.post_json(uri, params=request_parameters)
        json_response = json.loads(response.body)
        return json_response["key"]

    def test_post_overlay_succeeds_with_associated_image_key(self):
        key = self._create_image()

        uri = application.router.build(None, 'post-overlay', None, {})
        request_parameters = {
            "device_urlsafe_key": self.device_key.urlsafe(),
            "position": "TOP_LEFT",
            "overlay_type": "LOGO",
            "associated_image": key
        }

        response = self.app.post_json(uri, params=request_parameters)
        self.assertEqual(response.status_int, 200)

        # enable overlays for device so that the posted overlay will be serialized
        self.device.enable_overlays()

        # check if device get returns newly created overlay

        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)

        self.assertTrue(response_json["overlays"])
        self.assertFalse(response_json["overlays"])


a = {u'macAddress': u'bladfkdkddkdkd', u'heartbeatInterval': 2, u'apiKey': u'2e95bdd9c2074e5295724a64cbefeaf3',
     u'lastSync': None, u'playlistId': u'****initial playlist id****',
     u'proofOfPlayUrl': u'https://skykit-display-device-int.appspot.com/proofplay/api/v1/post_new_program_play',
     u'updated': u'2016-08-03 21:24:42', u'customerLocationCode': None, u'panelModel': None, u'checkContentInterval': 1,
     u'gcmRegistrationId': u'3k3k3k3k3k3kdldldldld', u'isUnmanagedDevice': False, u'timezone': u'America/Chicago',
     u'customerDisplayCode': None, u'overlays': [{u'position': u'TOP_LEFT', u'type': u'LOGO', u'image_key': {}}],
     u'panelInput': None, u'firmwareVersion': None, u'customerLocationName': None,
     u'playlist': u'****initial playlist****', u'annotatedAssetId': None, u'bootMode': None, u'connectionType': None,
     u'proofOfPlayEditable': False, u'panelSleep': False, u'etag': None,
     u'tenantKey': u'agx0ZXN0YmVkLXRlc3RyNAsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYDgw',
     u'latitude': None, u'chromeDeviceDomain': u'default.agosto.com', u'orgUnitPath': None, u'status': None,
     u'locationKey': None, u'program': u'****initial****', u'customerDisplayName': None, u'tenantCode': u'foobar',
     u'lastEnrollmentTime': None, u'ethernetMacAddress': None, u'archived': False, u'annotatedUser': None,
     u'programId': u'****initial****', u'contentManagerLocationDescription': None,
     u'deviceId': u'232jmkskkk34k42k3l423k2', u'key': u'agx0ZXN0YmVkLXRlc3RyFAsSDkNocm9tZU9zRGV2aWNlGA8M',
     u'platformVersion': None, u'contentManagerDisplayName': None, u'osVersion': None, u'logglyLink': None,
     u'annotatedLocation': None, u'kind': None, u'proofOfPlayLogging': False, u'name': u'None None',
     u'created': u'2016-08-03 21:24:42', u'registrationCorrelationIdentifier': None, u'notes': None,
     u'serialNumber': None, u'up': True, u'longitude': None, u'pairingCode': None, u'tenantName': u'Foobar',
     u'timezoneOffset': -5, u'contentServerUrl': u'https://www.content.com', u'model': None, u'lastError': None}
