from models import User, Distributor, Domain, Tenant, ChromeOsDevice

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

USER_EMAIL = 'daniel.ternyak@agosto.com'
DISTRIBUTOR_NAME = 'Agosto'
DOMAIN = 'local.skykit.com'
TENANT_NAME = 'Acme, Inc.'
TENANT_CODE = 'acme_inc'
TENANT_ADMIN_EMAIL = 'admin@acme.com'
DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
MAC_ADDRESS = '54271e619346'
UNMANAGED_MAC_ADDRESS = '04271e61934b'
UNMANAGED_GCM_REGISTRATION_ID = '3c70a8d70a6dfa6df76dfas2'
SERIAL_NUMBER = 'E6MSCX057790'

distributor = Distributor.query(Distributor.name == DISTRIBUTOR_NAME).get()
user = User.get_or_insert_by_email(email=USER_EMAIL)
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

tenant = Tenant.find_by_tenant_code(TENANT_CODE)

for i in range(0, 5001):
    managed_device = ChromeOsDevice.get_by_device_id(DEVICE_ID + str(i))
    if not managed_device:
        managed_device = ChromeOsDevice.create_managed(
            tenant_key=tenant.key,
            gcm_registration_id=GCM_REGISTRATION_ID + str(i),
            device_id=DEVICE_ID + str(i),
            mac_address=str(i) + MAC_ADDRESS)
        managed_device.serial_number = SERIAL_NUMBER + str(i)
        managed_device.put()
        print 'Managed device created with MAC ' + str(i) + MAC_ADDRESS
    else:
        print 'Managed device with Device ID ' + managed_device.device_id + ' already exists, so did not create'
