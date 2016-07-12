angular.module('skykitProvisioning').factory('DevicesService', function ($log, Restangular, $q, CacheFactory, $http) {
  var url;
  var url;
  return new class DevicesService {

    constructor() {
      this.SERVICE_NAME = 'devices';
      this.uriBase = 'v1/devices';
      if (!CacheFactory.get('deviceCache')) {
        this.deviceCache = CacheFactory('deviceCache', {
            maxAge: 60 * 60 * 1000,
            deleteOnExpire: 'aggressive',
            storageMode: 'localStorage',
            onExpire: (key, value) => {
              $http.get(key).success(data => {
                this.deviceCache.put(key, data);
                return;
              });
              return;
            }
          }
        );
      }

      if (!CacheFactory.get('deviceByTenantCache')) {
        this.deviceByTenantCache = CacheFactory('deviceByTenantCache', {
            maxAge: 60 * 60 * 1000,
            deleteOnExpire: 'aggressive',
            storageMode: 'localStorage',
            onExpire: (key, value) => {
              $http.get(key).success(data => {
                this.deviceByTenantCache.put(key, data);
                return;
              });
              return;
            }
          }
        );
      }
    }

    getDeviceByMacAddress(macAddress) {
      let url = `api/v1/devices?mac_address=${macAddress}`;
      return Restangular.oneUrl('api/v1/devices', url).get();
    }

    getDeviceByKey(deviceKey) {
      let url = `api/v1/devices/${deviceKey}`;
      let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }

    getIssuesByKey(deviceKey, startEpoch, endEpoch, prev, next) {
      prev = prev === undefined || null ? null : prev;
      next = next === undefined || null ? null : next;
      let url = `/api/v1/devices/${prev}/${next}/${deviceKey}/issues?start=${startEpoch}&end=${endEpoch}`;
      let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }

    getCommandEventsByKey(deviceKey, prev, next) {
      prev = prev === undefined || null ? null : prev;
      next = next === undefined || null ? null : next;
      let url = `/api/v1/player-command-events/${prev}/${next}/${deviceKey}`;
      let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }

//#######################################################################
// TENANT VIEW
//#######################################################################
    getDevicesByTenant(tenantKey, prev, next) {
      if (tenantKey !== undefined) {
        let deferred = $q.defer();
        let url = this.makeDevicesByTenantURL(tenantKey, prev, next, false);
        if (!this.deviceByTenantCache.get(url)) {
          let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
          promise.then(data => {
            this.deviceByTenantCache.put(url, data);
            return deferred.resolve(data);
          });
        } else {
          deferred.resolve(this.deviceByTenantCache.get(url));
        }

        return deferred.promise;
      }
    }

    getUnmanagedDevicesByTenant(tenantKey, prev, next) {
      if (tenantKey !== undefined) {
        let deferred = $q.defer();
        let url = this.makeDevicesByTenantURL(tenantKey, prev, next, true);
        if (!this.deviceByTenantCache.get(url)) {
          let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
          promise.then(data => {
            this.deviceByTenantCache.put(url, data);
            return deferred.resolve(data);
          });
        } else {
          deferred.resolve(this.deviceByTenantCache.get(url));
        }

        return deferred.promise;
      }
    }


    searchDevicesByPartialSerialByTenant(tenantKey, partial_serial, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `api/v1/tenants/search/serial/${tenantKey}/${partial_serial}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    searchDevicesByPartialMacByTenant(tenantKey, partial_mac, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `api/v1/tenants/search/mac/${tenantKey}/${partial_mac}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullSerialByTenant(tenantKey, full_serial, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `api/v1/tenants/match/serial/${tenantKey}/${full_serial}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullMacByTenant(tenantKey, full_mac, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `api/v1/tenants/match/mac/${tenantKey}/${full_mac}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

//#######################################################################
// DEVICES VIEW
//#######################################################################
    searchDevicesByPartialSerial(distributorKey, partial_serial, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `api/v1/distributors/search/serial/${distributorKey}/${partial_serial}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    searchDevicesByPartialMac(distributorKey, partial_mac, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `api/v1/distributors/search/mac/${distributorKey}/${partial_mac}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    searchDistributorDevicesByPartialGCMid(distributorKey, partial_gcmid, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/search/gcmid/${distributorKey}/devices?unmanaged=${unmanaged}&partial_gcmid=${partial_gcmid}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullSerial(distributorKey, full_serial, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `api/v1/distributors/match/serial/${distributorKey}/${full_serial}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullMac(distributorKey, full_mac, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `api/v1/distributors/match/mac/${distributorKey}/${full_mac}/${unmanaged}/devices`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullGCMid(distributorKey, full_gcmid, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/match/gcmid/${distributorKey}/devices?unmanaged=${unmanaged}&full_gcmid=${full_gcmid}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    getDevicesByDistributor(distributorKey, prev, next) {
      if (distributorKey !== undefined) {
        let deferred = $q.defer();
        let url = this.makeDevicesByDistributorURL(distributorKey, prev, next, false);
        if (!this.deviceCache.get(url)) {
          let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
          promise.then(data => {
            this.deviceCache.put(url, data);
            return deferred.resolve(data);
          });
        } else {
          deferred.resolve(this.deviceCache.get(url));
        }

        return deferred.promise;
      }
    }

    getUnmanagedDevicesByDistributor(distributorKey, prev, next) {
      if (distributorKey !== undefined) {
        let deferred = $q.defer();
        let url = this.makeDevicesByDistributorURL(distributorKey, prev, next, true);
        if (!this.deviceCache.get(url)) {
          let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
          promise.then(data => {
            this.deviceCache.put(url, data);
            return deferred.resolve(data);
          });
        } else {
          deferred.resolve(this.deviceCache.get(url));
        }

        return deferred.promise;
      }
    }

    getDevices() {
      let promise = Restangular.all(this.SERVICE_NAME).getList();
      return promise;
    }

    save(device) {
      if (device.key !== undefined) {
        var promise = device.put();
      } else {
        var promise = Restangular.service('devices').post(device);
      }
      return promise;
    }

    delete(deviceKey) {
      let promise = Restangular.one(this.SERVICE_NAME, deviceKey).remove();
      return promise;
    }

    getPanelModels() {
      return [
        {
          'id': 'None',
          'displayName': 'None'
        },
        {
          'id': 'Sony-FXD40LX2F',
          'displayName': 'Sony FXD40LX2F'
        },
        {
          'id': 'NEC-LCD4215',
          'displayName': 'NEC LCD4215'
        },
        {
          'id': 'Phillips-BDL5560EL',
          'displayName': 'Phillips BDL5560EL'
        },
        {
          'id': 'Panasonic-TH55LF6U',
          'displayName': 'Panasonic TH55LF6U'
        },
        {
          'id': 'Sharp-PNE521',
          'displayName': 'Sharp PNE521'
        }
      ];
    }

    getPanelInputs() {
      return [
        {
          'id': 'None',
          'parentId': 'None'
        },
        {
          'id': 'HDMI1',
          'parentId': 'Sony-FXD40LX2F'
        },
        {
          'id': 'HDMI2',
          'parentId': 'Sony-FXD40LX2F'
        },
        {
          'id': 'HDMI1',
          'parentId': 'Phillips-BDL5560EL'
        },
        {
          'id': 'HDMI2',
          'parentId': 'Phillips-BDL5560EL'
        },
        {
          'id': 'DVI',
          'parentId': 'Phillips-BDL5560EL'
        },
        {
          'id': 'HDMI1',
          'parentId': 'Panasonic-TH55LF6U'
        },
        {
          'id': 'HDMI2',
          'parentId': 'Panasonic-TH55LF6U'
        },
        {
          'id': 'DVI',
          'parentId': 'Panasonic-TH55LF6U'
        },
        {
          'id': 'HDMI1',
          'parentId': 'Sharp-PNE521'
        },
        {
          'id': 'HDMI2',
          'parentId': 'Sharp-PNE521'
        },
        {
          'id': 'DVI',
          'parentId': 'Sharp-PNE521'
        },
        {
          'id': 'VGA',
          'parentId': 'NEC-LCD4215'
        },
        {
          'id': 'DVI1',
          'parentId': 'NEC-LCD4215'
        }
      ];
    }

    makeDevicesByDistributorURL(distributorKey, prev, next, unmanaged) {
      return url = `/api/v1/distributors/${prev}/${next}/${distributorKey}/devices?unmanaged=${unmanaged}`;
    }

    makeDevicesByTenantURL(tenantKey, prev, next, unmanaged) {
      return url = `/api/v1/tenants/${prev}/${next}/${tenantKey}/devices?unmanaged=${unmanaged}`;
    }
  }();
});

