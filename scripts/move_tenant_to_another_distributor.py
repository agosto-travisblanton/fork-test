# Script for moving a tenant from one distributor to another
__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

from model_entities.distributor_and_user_model import Distributor
from model_entities.chrome_os_device_model_and_overlays import Tenant, ChromeOsDevice
from model_entities.domain_model import Domain

TENANT_CODE = 'qaskyauto'
OLD_DISTRIBUTOR_NAME = 'Agosto'
NEW_DISTRIBUTOR_NAME = 'AcmeDistributor'
NEW_DOMAIN_NAME = 'devqa.bogus.com'

old_distributor = Distributor.query(Distributor.name == OLD_DISTRIBUTOR_NAME).get()
if None == old_distributor:
    print 'OLD Distributor ' + old_distributor.name + ' not found'
else:
    print 'OLD Distributor ' + old_distributor.name + ' exists with domains:'
    old_distributor_domains = Domain.query(Domain.distributor_key == old_distributor.key, True == Domain.active).fetch(100)
    if len(old_distributor_domains) > 0:
        for domain in old_distributor_domains:
            print '*' + domain.name
    else:
        print '*None'
print '=========================================================='

new_distributor = Distributor.query(Distributor.name == NEW_DISTRIBUTOR_NAME).get()
if None == new_distributor:
    print 'NEW Distributor ' + new_distributor.name + ' not found'
else:
    print 'NEW Distributor ' + new_distributor.name + ' exists with domains:'
    new_distributor_domains = Domain.query(Domain.distributor_key == new_distributor.key, True == Domain.active).fetch(100)
    if len(new_distributor_domains) > 0:
        for domain in new_distributor_domains:
            print '*' + domain.name
    else:
        print '*None'
print '=========================================================='

tenant = Tenant.query(Tenant.name == TENANT_CODE).get()
if None == tenant:
    print 'tenant ' + tenant.name + ' not found'
else:
    print 'tenant ' + tenant.name + ' exists.'
    domain_key = tenant.domain_key
    domain = domain_key.get()
    print 'tenant domain is ' + domain.name + '.'
print '=========================================================='

tenant_devices = ChromeOsDevice.query(ChromeOsDevice.tenant_key == tenant.key).fetch()
count = len(tenant_devices)
print tenant.name + ' has ' + str(count) + ' devices:'

if count > 0:
    for device in tenant_devices:
        print '*' + device.serial_number + ', archived=' + str(device.archived) + ', unmanaged=' + str(device.is_unmanaged_device)
else:
    print '*None'
print '=========================================================='
print '=========================================================='

print 'new_distributor_domains[0].name=' + new_distributor_domains[0].name
print 'old_distributor_domains[0].name=' + old_distributor_domains[0].name

new_domain = Domain.query(Domain.distributor_key == new_distributor.key, True == Domain.active, Domain.name ==NEW_DOMAIN_NAME).get()
print 'new_domain=' + new_domain.name

domain_key = tenant.domain_key
domain = domain_key.get()
print 'BEFORE: tenant \'' + tenant.name + '\' domain is ' + domain.name + '.'

tenant.domain_key = new_domain.key
tenant.put()

domain_key = tenant.domain_key
domain = domain_key.get()
print 'AFTER: tenant \'' + tenant.name + '\' domain is ' + domain.name + '.'

# TO REVERT TO ORIGINAL DISTRIBUTOR:
# tenant.domain_key = old_distributor_domains[0].key
# tenant.put()
# domain_key = tenant.domain_key
# domain = domain_key.get()
# print 'RESTORED: tenant \'' + tenant.name + '\' domain is ' + domain.name + '.'

