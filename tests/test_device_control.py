from env_setup import setup_test_paths; setup_test_paths()

from agar.test import BaseTest, WebTest
from mock import patch
from models import ChromeOsDevice
from routes import application


class TestDeviceCommandsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceCommandsHandler, self).setUp()
        self.device_id = '132e235a-b346-4a37-a100-de49fa753a2a'
        self.chrome_os_device = ChromeOsDevice(device_id=self.device_id,
                                               gcm_registration_id='d23784972038845ab3963412')
        self.chrome_os_device.put()
        # self.patched_device_commands_processor = patch('device_commands_processor.DeviceCommandsProcessor')
        # self.addCleanup(self.patched_device_commands_processor.stop)

    # def testGet_ReturnsOKStatus(self):
    #     patched_device_commands_processor = patch('device_commands_processor.DeviceCommandsProcessor')
    #     self.addCleanup(patched_device_commands_processor.stop)
    #     device_commands_processor_mock = patched_device_commands_processor.start()
    #     request_parameters = {}
    #     uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
    #     response = self.app.get(uri, params=request_parameters)
    #     self.assertOK(response)
    #
    # def testPost_ReturnsOKStatus(self):
    #     patched_device_commands_processor = patch('device_commands_processor.DeviceCommandsProcessor')
    #     self.addCleanup(patched_device_commands_processor.stop)
    #     device_commands_processor_mock = patched_device_commands_processor.start()
    #     device_commands_processor_mock_instance = device_commands_processor_mock.return_value
    #     device_commands_processor_mock_instance.execute.return_value = None
    #     request_parameters = {'command': 'reset', 'payload': {}}
    #     uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
    #     response = self.app.post_json(uri, params=request_parameters)
    #     self.assertOK(response)

    # def testPost_CommandProcessorException_ReturnsUnprocessibleEntityStatus(self):
    #     patched_device_commands_processor = patch('device_commands_processor.DeviceCommandsProcessor')
        # self.addCleanup(patched_device_commands_processor.stop)
        # device_commands_processor_mock = patched_device_commands_processor.start()
        # device_commands_processor_mock_instance = device_commands_processor_mock.return_value
        # device_commands_processor_mock_instance.execute.side_effect = Exception('KABOOOOOOMMM!')
        # request_parameters = {'command': 'reset', 'payload': {}}
        # uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
        # with patch.object('device_commands_processor.DeviceCommandsProcessor',
        #            'execute',
        #            side_effect=Exception('KABOOOOOOMMM!')):
        #     resp = self.app.post_json(uri, params=request_parameters)

    # def testPut_ReturnsOKStatus(self):
    #     patched_device_commands_processor = patch('device_commands_processor.DeviceCommandsProcessor')
    #     self.addCleanup(patched_device_commands_processor.stop)
    #     device_commands_processor_mock = patched_device_commands_processor.start()
    #     request_parameters = {}
    #     uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
    #     response = self.app.put(uri, params=request_parameters)
    #     self.assertOK(response)
    #
    # def testDelete_ReturnsOKStatus(self):
    #     patched_device_commands_processor = patch('device_commands_processor.DeviceCommandsProcessor')
    #     self.addCleanup(patched_device_commands_processor.stop)
    #     device_commands_processor_mock = patched_device_commands_processor.start()
    #     uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
    #     response = self.app.delete(uri)
    #     self.assertOK(response)


