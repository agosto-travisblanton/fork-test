from google.appengine.ext import ndb

from models import Domain, Tenant, TenantEntityGroup
def get_tenant_list_from_distributor_key(distributor_key):
    distributor = ndb.Key(urlsafe=distributor_key)
    domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
    tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
    tenant_list = filter(lambda x: x.active, tenant_list)
    result = filter(lambda x: x.domain_key in domain_keys, tenant_list)
    sorted_result = sorted(result, key=lambda k: k.tenant_code)
    return sorted_result


def get_tenant_names_for_distributor(distributor_key):
    return [
        result.tenant_code.encode('ascii', 'ignore')
        for result in
        get_tenant_list_from_distributor_key(distributor_key)
        ]
