angular.module('skykitProvisioning').factory('DevicesService', function ($log, Restangular, $q, CacheFactory, $http, $state) {
  var url;
  var url;
  return new class DevicesService {

    constructor() {
      this.SERVICE_NAME = 'devices';
      this.uriBase = 'v1/devices';
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

    executeSearchingPartialSerialByTenant(tenantKey, partialSearch, unmanaged) {
      return this.searchDevicesByPartialSerialByTenant(tenantKey, partialSearch, unmanaged)
        .then((res) => {
          let result = res["matches"];
          let isMac = false
          let isGCMid = false
          let serialDevicesDict = this.convertDevicesArrayToDictionaryObj(result, isMac, isGCMid);
          let deviceSerialsOnly = [];
          for (let i = 0; i < result.length; i++) {
            let each = result[i];
            deviceSerialsOnly.push(each.serial);
          }
          return [deviceSerialsOnly, serialDevicesDict];
        });
    }

    executeSearchingPartialSerialByDistributor(distributorKey, partialSearch, unmanaged) {
      return this.searchDevicesByPartialSerial(distributorKey, partialSearch, unmanaged)
        .then((res) => {
          let result = res["matches"];
          let serialDevicesDict;
          let isMac = false
          let isGCMid = false
          if (unmanaged) {
            serialDevicesDict = this.convertDevicesArrayToDictionaryObj(result, isMac, isGCMid);
          } else {
            serialDevicesDict = this.convertDevicesArrayToDictionaryObj(result, isMac, isGCMid);
          }
          let serialDevicesOnly = [];
          for (let i = 0; i < result.length; i++) {
            let each = result[i];
            serialDevicesOnly.push(each.serial);
          }
          return [serialDevicesOnly, serialDevicesDict];
        });
    }

    executeSearchingPartialMacByTenant(tenantKey, partialSearch, unmanaged) {
      return this.searchDevicesByPartialMacByTenant(tenantKey, partialSearch, unmanaged)
        .then((res) => {
          let result = res["matches"];
          let macDevicesDict = this.convertDevicesArrayToDictionaryObj(result, true);
          let deviceMacsOnly = [];
          for (let i = 0; i < result.length; i++) {
            let each = result[i];
            deviceMacsOnly.push(each.mac);
          }
          return [deviceMacsOnly, macDevicesDict];
        })
    }

    executeSearchingPartialMacByDistributor(distributorKey, partialSearch, unmanaged) {
      return this.searchDevicesByPartialMac(distributorKey, partialSearch, unmanaged)
        .then((res) => {
          let result = res["matches"];
          let macDevicesDict;
          let isMac = true;
          let isGCMid = false;
          if (unmanaged) {
            macDevicesDict = this.convertDevicesArrayToDictionaryObj(result, isMac, isGCMid);
          } else {
            macDevicesDict = this.convertDevicesArrayToDictionaryObj(result, isMac, isGCMid);
          }
          let macDevices = [];
          for (let i = 0; i < result.length; i++) {
            let each = result[i];
            macDevices.push(each.mac);
          }
          return [macDevices, macDevicesDict];
        });

    }

    executeSearchingPartialGCMidByTenant(tenantKey, partialSearch, unmanaged) {
      return this.searchDistributorDevicesByPartialGCMidByTenant(tenantKey, partialSearch, unmanaged)
        .then((res) => {
          let result = res["matches"];
          let gcmidDevicesDict = this.convertDevicesArrayToDictionaryObj(result, false, true);
          let gcmidDevicesOnly = [];
          for (let i = 0; i < result.length; i++) {
            let each = result[i];
            gcmidDevicesOnly.push(each.gcmid);
          }
          return [gcmidDevicesOnly, gcmidDevicesDict];
        });
    }

    executeSearchingPartialGCMidByDistributor(distributorKey, partialSearch, unmanaged) {
      return this.searchDistributorDevicesByPartialGCMid(distributorKey, partialSearch, unmanaged)
        .then((res) => {
          let result = res["matches"];
          let GCMidDevicesDict;
          if (unmanaged) {
            GCMidDevicesDict = this.convertDevicesArrayToDictionaryObj(result, false, true);
          } else {
            GCMidDevicesDict = this.convertDevicesArrayToDictionaryObj(result, false, true);
          }
          let gcmidDevicesOnly = [];
          for (let i = 0; i < result.length; i++) {
            let each = result[i];
            gcmidDevicesOnly.push(each.gcmid);
          }
          return [gcmidDevicesOnly, GCMidDevicesDict];
        });
    }


    searchDevices(partialSearch, button, byTenant, tenantKey, distributorKey, unmanaged) {
      if (button === "Serial Number") {
        if (byTenant) {
          return this.executeSearchingPartialSerialByTenant(tenantKey, partialSearch, unmanaged)
        } else {
          return this.executeSearchingPartialSerialByDistributor(distributorKey, partialSearch, unmanaged)
        }
      } else if (button === "MAC") {
        if (byTenant) {
          return this.executeSearchingPartialMacByTenant(tenantKey, partialSearch, unmanaged)
        } else {
          return this.executeSearchingPartialMacByDistributor(distributorKey, partialSearch, unmanaged)
        }
      } else {
        if (byTenant) {
          return this.executeSearchingPartialGCMidByTenant(tenantKey, partialSearch, unmanaged)
        } else {
          return this.executeSearchingPartialGCMidByDistributor(distributorKey, partialSearch, unmanaged)
        }
      }
    }

    isResourceValid(resource, button, byTenant, tenantKey, distributorKey, unmanaged) {
      let mac, serial, gcmid;
      let deferred = $q.defer();
      if (resource) {
        if (resource.length > 2) {
          mac = button === "MAC";
          serial = button === "Serial Number";
          gcmid = button === "GCM ID";

          if (byTenant) {

            if (mac) {
              deferred.resolve(this.matchDevicesByFullMacByTenant(tenantKey, resource, unmanaged))
            } else if (serial) {
              deferred.resolve(this.matchDevicesByFullSerialByTenant(tenantKey, resource, unmanaged))
            } else {
              deferred.resolve(this.matchDevicesByFullGCMidByTenant(tenantKey, resource, unmanaged))
            }
          } else {
            if (mac) {
              deferred.resolve(this.matchDevicesByFullMac(distributorKey, resource, unmanaged))
            } else if (serial) {
              deferred.resolve(this.matchDevicesByFullSerial(distributorKey, resource, unmanaged))
            } else {
              deferred.resolve(this.matchDevicesByFullGCMid(distributorKey, resource, unmanaged))
            }
          }

        } else {
          deferred.resolve({"is_match": false})
        }

      } else {
        deferred.resolve({"is_match": false})
      }
      return deferred.promise

    };

    convertDevicesArrayToDictionaryObj(theArray, mac, gcm) {
      /** Converts array to dictionary with mac, gcmid, or serial as the key **/
      let devices = {};
      for (let i = 0; i < theArray.length; i++) {
        let item = theArray[i];
        if (mac) {
          devices[item.mac] = item;
        } else if (gcm) {
          devices[item.gcmid] = item;
        } else {
          devices[item.serial] = item;
        }
      }
      return devices;
    }
    ;

    editItem(item, tenantKey) {
      $state.go('editDevice', {
        deviceKey: item.key,
        tenantKey: tenantKey,
        fromDevices: false
      });
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

    /////////////////////////////////////////////////////////////////////////
    // TENANT VIEW
    /////////////////////////////////////////////////////////////////////////
    getDevicesByTenant(tenantKey, prev, next) {
      if (tenantKey !== undefined) {
        let url = this.makeDevicesByTenantURL(tenantKey, prev, next, false);
        return Restangular.oneUrl(this.SERVICE_NAME, url).get();
      }
    }

    getUnmanagedDevicesByTenant(tenantKey, prev, next) {
      if (tenantKey !== undefined) {
        let deferred = $q.defer();
        let url = this.makeDevicesByTenantURL(tenantKey, prev, next, true);
        return Restangular.oneUrl(this.SERVICE_NAME, url).get();
      }
    }

    searchDevicesByPartialSerialByTenant(tenantKey, partial_serial, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `/api/v1/tenants/search/${tenantKey}/devices?unmanaged=${unmanaged}&partial_serial=${partial_serial}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    searchDevicesByPartialMacByTenant(tenantKey, partial_mac, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `/api/v1/tenants/search/${tenantKey}/devices?unmanaged=${unmanaged}&partial_mac=${partial_mac}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    searchDistributorDevicesByPartialGCMidByTenant(tenantKey, partial_gcmid, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `/api/v1/tenants/search/${tenantKey}/devices?unmanaged=${unmanaged}&partial_gcmid=${partial_gcmid}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }


    matchDevicesByFullSerialByTenant(tenantKey, full_serial, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `/api/v1/tenants/match/${tenantKey}/devices?unmanaged=${unmanaged}&full_serial=${full_serial}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullMacByTenant(tenantKey, full_mac, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `/api/v1/tenants/match/${tenantKey}/devices?unmanaged=${unmanaged}&full_mac=${full_mac}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullGCMidByTenant(tenantKey, full_gcmid, unmanaged) {
      if (tenantKey !== undefined) {
        let url = `/api/v1/tenants/match/${tenantKey}/devices?unmanaged=${unmanaged}&full_gcmid=${full_gcmid}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    /////////////////////////////////////////////////////////////////////////
    // DEVICES VIEW
    /////////////////////////////////////////////////////////////////////////
    searchDevicesByPartialSerial(distributorKey, partial_serial, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/search/${distributorKey}/devices?unmanaged=${unmanaged}&partial_serial=${partial_serial}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    searchDevicesByPartialMac(distributorKey, partial_mac, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/search/${distributorKey}/devices?unmanaged=${unmanaged}&partial_mac=${partial_mac}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    searchDistributorDevicesByPartialGCMid(distributorKey, partial_gcmid, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/search/${distributorKey}/devices?unmanaged=${unmanaged}&partial_gcmid=${partial_gcmid}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullSerial(distributorKey, full_serial, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/match/${distributorKey}/devices?unmanaged=${unmanaged}&full_serial=${full_serial}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullMac(distributorKey, full_mac, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/match/${distributorKey}/devices?unmanaged=${unmanaged}&full_mac=${full_mac}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    matchDevicesByFullGCMid(distributorKey, full_gcmid, unmanaged) {
      if (distributorKey !== undefined) {
        let url = `/api/v1/distributors/match/${distributorKey}/devices?unmanaged=${unmanaged}&full_gcmid=${full_gcmid}`;
        let promise = Restangular.oneUrl(this.SERVICE_NAME, url).get();
        return promise;
      }
    }

    getDevicesByDistributor(distributorKey, prev, next) {
      if (distributorKey !== undefined) {
        let url = this.makeDevicesByDistributorURL(distributorKey, prev, next, false);
        return Restangular.oneUrl(this.SERVICE_NAME, url).get();
      }
    }

    getUnmanagedDevicesByDistributor(distributorKey, prev, next) {
      if (distributorKey !== undefined) {
        let url = this.makeDevicesByDistributorURL(distributorKey, prev, next, true);
        return Restangular.oneUrl(this.SERVICE_NAME, url).get();
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
      let url = `/api/v1/distributors/${distributorKey}/devices?unmanaged=${unmanaged}&next_cursor=${next}&prev_cursor=${prev}`;
      return url
    }

    makeDevicesByTenantURL(tenantKey, prev, next, unmanaged) {
      let url = `/api/v1/tenants/${tenantKey}/devices?unmanaged=${unmanaged}&next_cursor=${next}&prev_cursor=${prev}`;
      return url
    }
  }();
})
;
