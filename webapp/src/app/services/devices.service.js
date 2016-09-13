import 'restangular';

export default class DevicesService {
  constructor($log, Restangular, $q, $http, $state) {
    'ngInject';
    this.$log = $log
    this.Restangular = Restangular
    this.$q = $q
    this.$http = $http
    this.$state = $state
    this.SERVICE_NAME = 'devices';
    this.uriBase = 'v1/devices';
  }

  adjustControlsMode(deviceKey, controlsMode) {
    let payload = {
      controlsMode
    };

    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `/api/v1/devices/${deviceKey}/controls-mode`).customPUT(payload);
    return promise;
  }

  getDeviceByMacAddress(macAddress) {
    let url = `api/v1/devices?mac_address=${macAddress}`;
    return this.Restangular.oneUrl('api/v1/devices', url).get();
  }

  getDeviceByKey(deviceKey) {
    let url = `api/v1/devices/${deviceKey}`;
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
    return promise;
  }

  retriveFilteredDictionaryValue(dictionary, value) {
    let results = []
    for (let i = 0; i < dictionary.length; i++) {
      let each = dictionary[i];
      results.push(each[value]);
    }
    return results
  }

  executeSearchingPartialSerialByTenant(tenantKey, partialSearch, unmanaged) {
    return this.searchDevicesByPartialSerialByTenant(tenantKey, partialSearch, unmanaged)
      .then((res) => {
        let result = res["matches"];
        let isMac = false
        let isGCMid = false
        let serialDevicesDict = this.convertDevicesArrayToDictionaryObj(result, isMac, isGCMid);
        let deviceSerialsOnly = this.retriveFilteredDictionaryValue(result, "serial");
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
        let serialDevicesOnly = this.retriveFilteredDictionaryValue(result, "serial");
        return [serialDevicesOnly, serialDevicesDict];
      });
  }

  executeSearchingPartialMacByTenant(tenantKey, partialSearch, unmanaged) {
    return this.searchDevicesByPartialMacByTenant(tenantKey, partialSearch, unmanaged)
      .then((res) => {
        let result = res["matches"];
        let macDevicesDict = this.convertDevicesArrayToDictionaryObj(result, true);
        let deviceMacsOnly = this.retriveFilteredDictionaryValue(result, "mac");
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
        let macDevices = this.retriveFilteredDictionaryValue(result, "mac")
        return [macDevices, macDevicesDict];
      });

  }

  executeSearchingPartialGCMidByTenant(tenantKey, partialSearch, unmanaged) {
    return this.searchDistributorDevicesByPartialGCMidByTenant(tenantKey, partialSearch, unmanaged)
      .then((res) => {
        let result = res["matches"];
        let gcmidDevicesDict = this.convertDevicesArrayToDictionaryObj(result, false, true);
        let gcmidDevicesOnly = this.retriveFilteredDictionaryValue(result, "gcmid")
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
        let gcmidDevicesOnly = this.retriveFilteredDictionaryValue(result, "gcmid")
        return [gcmidDevicesOnly, GCMidDevicesDict];
      });
  }

  rejectedPromise() {
    let deviceDeferred = this.$q.defer();
    deviceDeferred.reject()
    return deviceDeferred.promise
  };


  searchDevices(partialSearch, button, byTenant, tenantKey, distributorKey, unmanaged) {
    let deferred = this.$q.defer();
    let devicesPromise;
    if (partialSearch) {
      if (partialSearch.length > 2) {
        if (button === "Serial Number") {
          if (byTenant) {
            devicesPromise = this.executeSearchingPartialSerialByTenant(tenantKey, partialSearch, unmanaged)
          } else {
            devicesPromise = this.executeSearchingPartialSerialByDistributor(distributorKey, partialSearch, unmanaged)
          }
        } else if (button === "MAC") {
          if (byTenant) {
            devicesPromise = this.executeSearchingPartialMacByTenant(tenantKey, partialSearch, unmanaged)
          } else {
            devicesPromise = this.executeSearchingPartialMacByDistributor(distributorKey, partialSearch, unmanaged)
          }
        } else {
          if (byTenant) {
            devicesPromise = this.executeSearchingPartialGCMidByTenant(tenantKey, partialSearch, unmanaged)
          } else {
            devicesPromise = this.executeSearchingPartialGCMidByDistributor(distributorKey, partialSearch, unmanaged)
          }
        }
      } else {
        devicesPromise = this.rejectedPromise()
      }
    } else {
      devicesPromise = this.rejectedPromise()
    }

    devicesPromise.then(function (devicesResult) {
      deferred.resolve({
        "success": true,
        "devices": devicesResult
      })
    })

    devicesPromise.catch(function (devicesResult) {
      deferred.resolve({
        "success": false,
        "devices": []
      })
    })

    return deferred.promise
  }

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
  };

  editItem(item, fromDevices) {
    if (!fromDevices) {
      fromDevices = false
    }
    this.$state.go('editDevice', {
      deviceKey: item.key,
      tenantKey: item.tenantKey,
      fromDevices: fromDevices
    });
  }

  preprateForEditView(button, tenantKey, searchText, macDevices, serialDevices, gcmidDevices) {
    let mac, serial, gcmid;

    mac = button === "MAC";
    serial = button === "Serial Number";
    gcmid = button === "GCM ID"

    if (mac) {
      return this.editItem(macDevices[searchText]);
    } else if (serial) {
      return this.editItem(serialDevices[searchText]);
    } else {
      return this.editItem(gcmidDevices[searchText])
    }

  }

  getIssuesByKey(deviceKey, startEpoch, endEpoch, prev, next) {
    prev = prev === undefined || null ? null : prev;
    next = next === undefined || null ? null : next;
    let url = `/api/v1/devices/${prev}/${next}/${deviceKey}/issues?start=${startEpoch}&end=${endEpoch}`;
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
    return promise;
  }

  getCommandEventsByKey(deviceKey, prev, next) {
    prev = prev === undefined || null ? null : prev;
    next = next === undefined || null ? null : next;
    let url = `/api/v1/player-command-events/${prev}/${next}/${deviceKey}`;
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
    return promise;
  }

  /////////////////////////////////////////////////////////////////////////
  // TENANT VIEW
  /////////////////////////////////////////////////////////////////////////
  getDevicesByTenant(tenantKey, prev, next) {
    if (tenantKey !== undefined) {
      let url = this.makeDevicesByTenantURL(tenantKey, prev, next, false);
      return this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
    }
  }

  getUnmanagedDevicesByTenant(tenantKey, prev, next) {
    if (tenantKey !== undefined) {
      let deferred = this.$q.defer();
      let url = this.makeDevicesByTenantURL(tenantKey, prev, next, true);
      return this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
    }
  }

  searchDevicesByPartialSerialByTenant(tenantKey, partial_serial, unmanaged) {
    if (tenantKey !== undefined) {
      let url = `/api/v1/tenants/search/${tenantKey}/devices?unmanaged=${unmanaged}&partial_serial=${partial_serial}`;
      let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }
  }

  searchDevicesByPartialMacByTenant(tenantKey, partial_mac, unmanaged) {
    if (tenantKey !== undefined) {
      let url = `/api/v1/tenants/search/${tenantKey}/devices?unmanaged=${unmanaged}&partial_mac=${partial_mac}`;
      let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }
  }

  searchDistributorDevicesByPartialGCMidByTenant(tenantKey, partial_gcmid, unmanaged) {
    if (tenantKey !== undefined) {
      let url = `/api/v1/tenants/search/${tenantKey}/devices?unmanaged=${unmanaged}&partial_gcmid=${partial_gcmid}`;
      let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }
  }


  /////////////////////////////////////////////////////////////////////////
  // DEVICES VIEW
  /////////////////////////////////////////////////////////////////////////
  searchDevicesByPartialSerial(distributorKey, partial_serial, unmanaged) {
    if (distributorKey !== undefined) {
      let url = `/api/v1/distributors/search/${distributorKey}/devices?unmanaged=${unmanaged}&partial_serial=${partial_serial}`;
      let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }
  }

  searchDevicesByPartialMac(distributorKey, partial_mac, unmanaged) {
    if (distributorKey !== undefined) {
      let url = `/api/v1/distributors/search/${distributorKey}/devices?unmanaged=${unmanaged}&partial_mac=${partial_mac}`;
      let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }
  }

  searchDistributorDevicesByPartialGCMid(distributorKey, partial_gcmid, unmanaged) {
    if (distributorKey !== undefined) {
      let url = `/api/v1/distributors/search/${distributorKey}/devices?unmanaged=${unmanaged}&partial_gcmid=${partial_gcmid}`;
      let promise = this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
      return promise;
    }
  }

  getDevicesByDistributor(distributorKey, prev, next) {
    if (distributorKey !== undefined) {
      let url = this.makeDevicesByDistributorURL(distributorKey, prev, next, false);
      return this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
    }
  }

  getUnmanagedDevicesByDistributor(distributorKey, prev, next) {
    if (distributorKey !== undefined) {
      let url = this.makeDevicesByDistributorURL(distributorKey, prev, next, true);
      return this.Restangular.oneUrl(this.SERVICE_NAME, url).get();
    }
  }

  getDevices() {
    let promise = this.Restangular.all(this.SERVICE_NAME).getList();
    return promise;
  }

  save(device) {
    if (device.key !== undefined) {
      var promise = device.put();
    } else {
      var promise = this.Restangular.service('devices').post(device);
    }
    return promise;
  }

  saveOverlaySettings(device_urlsafe_key, bottom_left, bottom_right, top_right, top_left) {
    let payload = {
      bottom_left,
      bottom_right,
      top_right,
      top_left,
    }

    return this.Restangular.oneUrl('overlay', `/api/v1/overlay/device/${device_urlsafe_key}`).customPOST(payload);
  }

  delete(deviceKey) {
    let promise = this.Restangular.one(this.SERVICE_NAME, deviceKey).remove();
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
}
