export default class TenantsService {

  constructor(Restangular, SessionsService) {
    'ngInject';
    this.Restangular = Restangular;
    this.SessionsService = SessionsService;
  }

  save(tenant) {
    if (tenant.key !== undefined) {
      var promise = tenant.put();
    } else {
      var promise = this.Restangular.service('tenants').post(tenant);
    }
    return promise;
  }

  saveOverlaySettings(tenant_urlsafe_key, bottom_left, bottom_right, top_right, top_left) {
    let payload = {
      bottom_left,
      bottom_right,
      top_right,
      top_left,
    }
    return this.Restangular.oneUrl('overlay', `/internal/v1/overlay/tenant/${tenant_urlsafe_key}`).customPOST(payload);
  }

  overlayApplyTenant(tenant_urlsafe_key) {
    return this.Restangular.oneUrl('overlay', `/internal/v1/overlay/tenant/${tenant_urlsafe_key}/apply`).post();
  }

  searchAllTenantsByName(tenant_name, allDistributors) {
    let promise = this.Restangular.all('tenants').customGETLIST("", {
      tenant_name: tenant_name, allDistributors: allDistributors
    })
    return promise;
  }

  fetchAllTenants() {
    let promise = this.Restangular.all('tenants').getList();
    return promise;
  }

  fetchAllTenantsPaginated(page_size, offset) {
    let url = `internal/v1/tenants/paginated/${page_size}/${offset}`;
    let promise = this.Restangular.oneUrl('tenants', url).get();
    return promise;
  }

  getTenantByKey(tenantKey) {
    let url = `internal/v1/tenants/${tenantKey}`;
    let promise = this.Restangular.oneUrl('tenants', url).get();
    return promise;
  }

  delete(tenant) {
    if (tenant.key !== undefined) {
      let promise = this.Restangular.one("tenants", tenant.key).remove();
      return promise;
    }
  }
}

