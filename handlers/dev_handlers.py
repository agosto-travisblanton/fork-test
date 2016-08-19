from webapp2 import RequestHandler
from google.appengine.ext.deferred import deferred
from app_config import config
from models import User, Distributor, Domain, Tenant, ChromeOsDevice, PlayerCommandEvent, TenantEntityGroup, \
    DeviceIssueLog, Location, IntegrationEventLog
import random
from datetime import datetime, timedelta

USER_EMAIL = 'daniel.ternyak@agosto.com'
DISTRIBUTOR_NAME = 'Dunder'
SECOND_DISTRIBUTOR = "Mifflin"
THIRD_DISTRIBUTOR = "Scranton"
DOMAIN = 'local.skykit.com'
TENANT_NAME = 'Acme, Inc.'
TENANT_CODE = 'acme_inc'
TENANT_ADMIN_EMAIL = 'admin@acme.com'
SECOND_TENANT_NAME = 'DaveDistribution'
SECOND_TENANT_CODE = 'davedistribution'
SECOND_TENANT_ADMIN_EMAIL = 'dave@dave.com'
DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
MAC_ADDRESS = '54271e619346'
UNMANAGED_MAC_ADDRESS = '04271e61934b'
UNMANAGED_GCM_REGISTRATION_ID = '3c70a8d70a6dfa6df76dfas2'
SERIAL_NUMBER = 'E6MSCX057790'
array_of_devices_with_values = []

##################################################################
# ENROLLMENT
##################################################################
REGISTRATION = 'Registration'
PLAYER = 'Player'
PROVISIONING = 'Provisioning'
DIRECTORY_API = 'Chrome Directory API'
CONTENT_MANAGER = 'Content Manager'
CORRELATION_IDENTIFIER = '0779aec7ae3040dcb8a3a572c356df66'
GCM_REGISTRATION_ID = 'APA91bGl7nxmJ9JXF0_9e8zEuXIMBxX0S0o9bmmMMkqxZTjjN4hoPsweooggycp1rJonDbszrTIioEI'
REGISTRATION_WORKFLOW_STEP_1 = 'Request from Player to create a managed device'
REGISTRATION_WORKFLOW_STEP_2 = 'Response to Player after creating a managed device'
REGISTRATION_WORKFLOW_STEP_3_REQUEST = 'Request for device information'
REGISTRATION_WORKFLOW_STEP_3_RESPONSE = 'Response for device information request'
REGISTRATION_WORKFLOW_NO_DEVICE_INFO = 'Requested device not found'
REGISTRATION_WORKFLOW_STEP_4_REQUEST = 'Request for device information'
REGISTRATION_WORKFLOW_STEP_4_RESPONSE = 'Response for device information request'
REGISTRATION_WORKFLOW_STEP_5_REQUEST = 'Request to Content Manager for a create_device'
REGISTRATION_WORKFLOW_STEP_5_RESPONSE = 'Response from Content Manager for a create_device'
timestamp = datetime.utcnow()


##################################################################

def create_integration_events_for_device(DEVICE_KEY):
    #######################################
    # INTEGRATION EVENTS / ENROLLMENT
    #######################################
    registration_event_1 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=PLAYER,
        workflow_step=REGISTRATION_WORKFLOW_STEP_1,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=1),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
        details=
        'register_device with device key ahVzfnNreWtpdC1wcm92aXNpb25pbmdyGwsSDkNocm9tZU9zRGV2aWNlGICAgOCZsP0JDA.'
    )
    registration_event_1.put()

    registration_event_2 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=PROVISIONING,
        workflow_step=REGISTRATION_WORKFLOW_STEP_2,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=2),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
        details=
        'Device resource uri '
        '/api/v1/devices/ahVzfnNreWtpdC1wcm92aXNpb25pbmdyGwsSDkNocm9tZU9zRGV2aWNlGICAgOCZsP0JDA returned '
        'in response Location header.'
    )
    registration_event_2.put()

    registration_event_3 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=DIRECTORY_API,
        workflow_step=REGISTRATION_WORKFLOW_STEP_3_REQUEST,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=3),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
    )
    registration_event_3.put()

    registration_event_4 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=DIRECTORY_API,
        workflow_step=REGISTRATION_WORKFLOW_STEP_3_RESPONSE,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=4),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
    )
    registration_event_4.put()

    registration_event_5 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=DIRECTORY_API,
        workflow_step=REGISTRATION_WORKFLOW_NO_DEVICE_INFO,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=5),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
    )
    registration_event_5.put()

    registration_event_6 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=DIRECTORY_API,
        workflow_step=REGISTRATION_WORKFLOW_STEP_4_REQUEST,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=6),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
    )
    registration_event_6.put()

    registration_event_7 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=DIRECTORY_API,
        workflow_step=REGISTRATION_WORKFLOW_STEP_4_RESPONSE,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=7),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
        details='Chrome Directory API call success! Notifying Content Manager.'
    )
    registration_event_7.put()

    registration_event_8 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=CONTENT_MANAGER,
        workflow_step=REGISTRATION_WORKFLOW_STEP_5_REQUEST,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=8),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
        details=
        'Request url: https://skykit-contentmanager.appspot.com/provisioning/v1/displays for call to CM.'
    )
    registration_event_8.put()

    registration_event_9 = IntegrationEventLog.create(
        event_category=REGISTRATION,
        component_name=CONTENT_MANAGER,
        workflow_step=REGISTRATION_WORKFLOW_STEP_5_RESPONSE,
        correlation_identifier=CORRELATION_IDENTIFIER,
        utc_timestamp=timestamp + timedelta(seconds=9),
        gcm_registration_id=GCM_REGISTRATION_ID,
        device_urlsafe_key=DEVICE_KEY,
        details=
        'ContentManagerApi.create_device: http_status=201, '
        'url=https://skykit-contentmanager.appspot.com/provisioning/v1/displays, '
        'device_key=ahVzfnNreWtpdC1wcm92aXNpb25pbmdyGwsSDkNocm9tZU9zRGV2aWNlGICAgOCZsP0JDA, '
        'api_key=6c522ae93b7b481c9f0485a419194ad4, tenant_code=agosto, SN=FBMACX001373. Success!'
    )
    registration_event_9.put()

    registration_event_10 = IntegrationEventLog.create(
        event_category='Other',
        component_name='Foobar1',
        workflow_step='Nothing',
        gcm_registration_id='jdalskdjfa'
    )
    registration_event_10.put()

    registration_event_11 = IntegrationEventLog.create(
        event_category='Other',
        component_name='Foobar2',
        workflow_step='Nothing'
    )
    registration_event_11.put()

    registration_event_12 = IntegrationEventLog.create(
        event_category='Other',
        component_name='Foobar3',
        workflow_step='Nothing'
    )
    registration_event_12.put()


def create_email(first, last):
    return first + "." + last + "@agosto.com"


class SeedScript(RequestHandler):
    def get(self, user_first, user_last):
        deferred.defer(kick_off, user_first, user_last)
        self.response.out.write(
            "A SEED SCRIPT HAS BEEN KICKED OFF FOR {}. PLEASE WATCH FOR A COMPLETE STATEMENT IN THE TERMINAL".format(
                create_email(user_first, user_last))
        )


def kick_off(user_first, user_last):
    global USER_EMAIL
    USER_EMAIL = create_email(user_first, user_last)
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++    SEED SCRIPT HAS BEGUN    ++++++++++++++++++++++++++"
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "+++++++++++++++++++++++++  CREATE DATA FOR DATASTORE  +++++++++++++++++++++++++"
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    make_data_for_a_distributor()
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++ COMPLETED SEED SCRIPT ++++++++++++++++++++++++++++"
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++ DEVICES WITH EVENTS AND COMMANDS +++++++++++++++++++++"
    print "+++ YOU WILL WANT TO RECORD THESE TO VIEW DEVICES WITH EVENTS OR COMMANDS +++++"
    global array_of_devices_with_values
    print array_of_devices_with_values
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"


def make_data_for_a_distributor():
    ##########################################################################################
    # DISTRIBUTORS
    ##########################################################################################
    distributor = Distributor.query(Distributor.name == DISTRIBUTOR_NAME).get()
    if not distributor:
        distributor = Distributor.create(name=DISTRIBUTOR_NAME)
        distributor.put()
        print 'Distributor ' + distributor.name + ' created'
    else:
        print 'Distributor ' + distributor.name + ' already exists, so did not create'

    second_distributor = Distributor.query(Distributor.name == SECOND_DISTRIBUTOR).get()
    if not second_distributor:
        second_distributor = Distributor.create(name=SECOND_DISTRIBUTOR)
        second_distributor.put()
        print 'Distributor ' + second_distributor.name + ' created'
    else:
        print 'Distributor ' + second_distributor.name + ' already exists, so did not create'

    third_distributor = Distributor.query(Distributor.name == THIRD_DISTRIBUTOR).get()
    if not third_distributor:
        third_distributor = Distributor.create(name=THIRD_DISTRIBUTOR)
        third_distributor.put()
        print 'Distributor ' + third_distributor.name + ' created'
    else:
        print 'Distributor ' + third_distributor.name + ' already exists, so did not create'

    ##########################################################################################
    # USERS
    ##########################################################################################
    default_users_to_add = ["a@gmail.com", "b@gmail.com", "c@gmail.com"]
    for item in default_users_to_add:
        u = User.get_or_insert_by_email(email=item)
        u.add_distributor(distributor.key)
        u.add_distributor(second_distributor.key)

    user = User.get_or_insert_by_email(email=USER_EMAIL)
    if not distributor:
        print 'Distributor ' + DISTRIBUTOR_NAME + ' not found'
        print 'Could not add ' + USER_EMAIL + ' to ' + DISTRIBUTOR_NAME
    else:
        if not user:
            print 'User with email ' + USER_EMAIL + ' not found. Could not add ' + USER_EMAIL + ' to ' + DISTRIBUTOR_NAME
        else:
            user.add_distributor(distributor.key, role=1)
            print 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name
            user.add_distributor(second_distributor.key)
            print 'SUCCESS! ' + user.email + ' is linked to ' + second_distributor.name
    ##########################################################################################
    # DOMAINS
    ##########################################################################################
    domain = Domain.query(Domain.name == DOMAIN).get()
    if not domain:
        domain = Domain.create(name=DOMAIN,
                               distributor_key=distributor.key,
                               impersonation_admin_email_address='test@skykit.com',
                               active=True)
        domain.put()
        print 'Domain ' + domain.name + ' created'
    else:
        print 'Domain ' + domain.name + ' already exists, so did not creat'

    ##########################################################################################
    # CREATE TENANTS
    ##########################################################################################
    for i in range(1, 101):
        tenant_code = "my_tenant" + str(i)
        tenant_code = tenant_code.lower()
        tenant_code_datastore = Tenant.find_by_tenant_code(tenant_code)
        if not tenant_code_datastore:
            tenant = Tenant.create(tenant_code=tenant_code,
                                   name="my_tenant" + str(i),
                                   admin_email=TENANT_ADMIN_EMAIL,
                                   content_server_url='https://skykit-contentmanager-int.appspot.com',
                                   content_manager_base_url='https://skykit-contentmanager-int.appspot.com/content',
                                   domain_key=domain.key,
                                   active=True)
            tenant.put()
            print 'Tenant ' + tenant.name + ' created'
    else:
        print 'Tenant ' + tenant.name + ' already exists, so did not create'

    ##########################################################################################
    tenant = Tenant.find_by_tenant_code(SECOND_TENANT_CODE)
    if not tenant:
        tenant = Tenant.create(tenant_code=SECOND_TENANT_CODE,
                               name=SECOND_TENANT_NAME,
                               admin_email=SECOND_TENANT_ADMIN_EMAIL,
                               content_server_url='https://skykit-contentmanager-int.appspot.com',
                               content_manager_base_url='https://skykit-contentmanager-int.appspot.com/content',
                               domain_key=domain.key,
                               active=True)
        tenant.put()
        print 'Tenant ' + tenant.name + ' created'

    ##########################################################################################
    tenant = Tenant.find_by_tenant_code(TENANT_CODE)
    if not tenant:
        tenant = Tenant.create(tenant_code=TENANT_CODE,
                               name=TENANT_NAME,
                               admin_email=TENANT_ADMIN_EMAIL,
                               content_server_url='https://skykit-contentmanager-int.appspot.com',
                               content_manager_base_url='https://skykit-contentmanager-int.appspot.com/content',
                               domain_key=domain.key,
                               active=True)
        tenant.put()
        print 'Tenant ' + tenant.name + ' created'

    ##########################################################################################
    # CREATE LOCATIONS
    ##########################################################################################
    for i in range(1, 103):
        if Location.is_customer_location_code_unique("my_location" + str(i), tenant.key):
            location = Location.create(tenant_key=tenant.key,
                                       customer_location_name="my_location" + str(i),
                                       customer_location_code="my_location" + str(i))
            location.address = None
            location.city = None
            location.state = None
            location.postal_code = None
            location.dma = None
            location.active = True
            location.put()

    ##########################################################################################
    # UNMANAGED DEVICES
    ##########################################################################################
    unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_mac_address(UNMANAGED_MAC_ADDRESS)
    if not unmanaged_device:

        unmanaged_device = ChromeOsDevice.create_unmanaged(
            gcm_registration_id=UNMANAGED_GCM_REGISTRATION_ID,
            mac_address=UNMANAGED_MAC_ADDRESS)
        unmanaged_device.tenant_key = tenant.key
        unmanaged_device.put()
        print 'Unmanaged device created with MAC ' + UNMANAGED_MAC_ADDRESS
    else:
        print 'Unmanaged device with MAC ' + unmanaged_device.mac_address + ' already exists, so did not create'

    ##########################################################################################
    # MANAGED DEVICES
    ##########################################################################################
    for i in range(1, 101):
        managed_device = ChromeOsDevice.get_by_device_id(DEVICE_ID + str(i))
        if not managed_device:
            managed_device = ChromeOsDevice.create_managed(
                tenant_key=tenant.key,
                gcm_registration_id=GCM_REGISTRATION_ID + str(i),
                device_id=DEVICE_ID + str(i),
                mac_address=str(i) + MAC_ADDRESS,
                ethernet_mac_address=str(i) + "ether" + MAC_ADDRESS
            )
            managed_device.serial_number = SERIAL_NUMBER + str(i)
            managed_device.put()
            print 'Managed device created with MAC ' + str(i) + MAC_ADDRESS

            if random.randint(1, 10) == 1:
                global array_of_devices_with_values
                array_of_devices_with_values.append(str(managed_device.serial_number))

                create_integration_events_for_device(managed_device.key.urlsafe())

                for z in range(1, 78):
                    issue = DeviceIssueLog.create(device_key=managed_device.key,
                                                  category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                                  up=False,
                                                  storage_utilization=random.randint(1, 100),
                                                  memory_utilization=random.randint(1, 100),
                                                  program=str(random.randint(1, 100)),
                                                  program_id=managed_device.program_id,
                                                  last_error=managed_device.last_error,
                                                  )
                    issue.put()

                    payload = 'reset content'.format(i)
                    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
                    event = PlayerCommandEvent.create(device_urlsafe_key=managed_device.key.urlsafe(),
                                                      payload=payload, gcm_registration_id=gcm_registration_id)

                    event.put()
                    print 'Added ' + payload + ' event to ' + managed_device.key.urlsafe()
                    payload = 'reset player'.format(i)
                    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
                    event = PlayerCommandEvent.create(device_urlsafe_key=managed_device.key.urlsafe(),
                                                      payload=payload, gcm_registration_id=gcm_registration_id)
                    event.player_has_confirmed = True
                    event.put()
                    print 'Added ' + payload + ' event to ' + managed_device.key.urlsafe()
                    payload = 'panel on'.format(i)
                    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
                    event = PlayerCommandEvent.create(device_urlsafe_key=managed_device.key.urlsafe(),
                                                      payload=payload, gcm_registration_id=gcm_registration_id)

                    event.player_has_confirmed = True
                    event.put()
                    print 'Added ' + payload + ' event to ' + managed_device.key.urlsafe()

        else:
            print 'Managed device with Device ID ' + managed_device.device_id + ' already exists, so did not create'

    ##########################################################################################
    # PROOF OF PLAY
    #########################################################################################
    tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
    for tenant in tenants:
        if tenant.proof_of_play_url is None:
            tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
            tenant.put()
        print '{0}: {1}'.format(tenant.name, tenant.proof_of_play_url)
