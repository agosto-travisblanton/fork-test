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

  getLocationsByTenantKey(tenantKey) {
    let promise = this.Restangular.oneUrl('tenants', `api/v1/tenants/${tenantKey}/locations`).get();
    return promise;
  }

  getLocationsByTenantKeyPaginated(tenantKey, prev, next) {
    prev = prev === undefined || null ? null : prev;
    next = next === undefined || null ? null : next;
    let promise = this.Restangular.oneUrl('tenants', `api/v1/tenants/${tenantKey}/${prev}/${next}/locations`).get();
    return promise;
  }

  getLocationByKey(locationKey) {
    let promise = this.Restangular.oneUrl('locations', `api/v1/locations/${locationKey}`).get();
    return promise;
  }
}
