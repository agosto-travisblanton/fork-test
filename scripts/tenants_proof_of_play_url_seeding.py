from app_config import config
from models import Tenant, TenantEntityGroup

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
for tenant in tenants:
  if tenant.proof_of_play_url is None:
    tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
    tenant.put()
  print '{0}: {1}'.format(tenant.name, tenant.proof_of_play_url)
