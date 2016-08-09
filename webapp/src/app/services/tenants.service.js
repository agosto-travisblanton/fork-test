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

  getImages(tenant_urlsafe_key) {
    return this.Restangular.oneUrl('image', `/api/v1/image/tenant/${tenant_urlsafe_key}`).getList()
  }

  saveImage(tenant_urlsafe_key, svg_rep, name) {
    let payload = {
      svg_rep,
      name
    }
    return this.Restangular.oneUrl('image', `/api/v1/image/tenant/${tenant_urlsafe_key}`).customPOST(payload);
  }


  searchAllTenantsByName(tenant_name) {
    let promise = this.Restangular.all('tenants').customGETLIST("", {tenant_name: tenant_name})
    return promise;
  }

  fetchAllTenants() {
    let promise = this.Restangular.all('tenants').getList();
    return promise;
  }

  fetchAllTenantsPaginated(page_size, offset) {
    let url = `api/v1/tenants/paginated/${page_size}/${offset}`;
    let promise = this.Restangular.oneUrl('tenants', url).get();
    return promise;
  }

  getTenantByKey(tenantKey) {
    let url = `api/v1/tenants/${tenantKey}`;
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

