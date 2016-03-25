from models import Tenant, TenantEntityGroup

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
#does a get on each tenant to verify it has at least a default proof_of_play_url
for tenant in tenants:
  print '{0}: {1}'.format(tenant.name, tenant.proof_of_play_url)
