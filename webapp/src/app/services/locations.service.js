angular.module('skykitProvisioning').factory('LocationsService', function (Restangular) {
    class LocationsService {

        constructor() {
        }

        save(location) {
            if (location.key !== undefined) {
                var promise = location.put();
            } else {
                var promise = Restangular.service('locations').post(location);
            }
            return promise;
        }

        getLocationsByTenantKey(tenantKey) {
            let promise = Restangular.oneUrl('tenants', `api/v1/tenants/${tenantKey}/locations`).get();
            return promise;
        }

        getLocationsByTenantKeyPaginated(tenantKey, prev, next) {
            prev = prev === undefined || null ? null : prev;
            next = next === undefined || null ? null : next;
            let promise = Restangular.oneUrl('tenants', `api/v1/tenants/${tenantKey}/${prev}/${next}/locations`).get();
            return promise;
        }

        getLocationByKey(locationKey) {
            let promise = Restangular.oneUrl('locations', `api/v1/locations/${locationKey}`).get();
            return promise;
        }
    }

    return new LocationsService();
});
