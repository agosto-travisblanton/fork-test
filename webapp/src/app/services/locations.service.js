export default class LocationsService {

  constructor(Restangular) {
    'ngInject';
    this.Restangular = Restangular;
  }

  save(location) {
    if (location.key !== undefined) {
      var promise = location.put();
    } else {
      var promise = this.Restangular.service('locations').post(location);
    }
    return promise;
  }

  searchAllTenantLocationsByName(tenantKey, customer_location_name) {
    let promise = this.Restangular.all('tenants').customGETLIST(tenantKey + "/locations", {customer_location_name: customer_location_name})
    return promise;
  }

  getLocationsByTenantKey(tenantKey) {
    let promise = this.Restangular.oneUrl('tenants', `internal/v1/tenants/${tenantKey}/locations`).get();
    return promise;
  }

  getLocationsByTenantKeyPaginated(tenantKey, prev, next) {
    prev = prev === undefined || null ? null : prev;
    next = next === undefined || null ? null : next;
    let promise = this.Restangular.oneUrl('tenants', `internal/v1/tenants/${tenantKey}/${prev}/${next}/locations`).get();
    return promise;
  }

  getLocationByKey(locationKey) {
    let promise = this.Restangular.oneUrl('locations', `internal/v1/locations/${locationKey}`).get();
    return promise;
  }
}
