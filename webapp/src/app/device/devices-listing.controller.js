(function () {

let appModule = angular.module('skykitProvisioning');

appModule.controller('DevicesListingCtrl', function($stateParams, $log, DevicesService, $state, SessionsService, ProgressBarService, sweet) {
  let vm = this;
  vm.distributorKey = undefined;
  //####################################
  // Managed
  //####################################
  vm.devices = [];
  vm.devicesPrev = null;
  vm.devicesNext = null;
  vm.selectedButton = "Serial Number";
  vm.serialDevices = {};
  vm.disabled = true;
  vm.macDevices = {};

  //####################################
  // Unmanaged
  //####################################
  vm.unmanagedSelectedButton = "MAC";
  vm.unmanagedSerialDevices = {};
  vm.unmanagedDisabled = true;
  vm.unmanagedDevicesPrev = null;
  vm.unmanagedDevicesNext = null;
  vm.unmanagedDevices = [];
  vm.unmanagedMacDevices = {};

  vm.refreshManagedDevices = function() {
    vm.devicesPrev = null;
    vm.devicesNext = null;
    DevicesService.deviceCache.removeAll();
    return vm.getManagedDevices(vm.distributorKey, vm.devicesPrev, vm.devicesNext);
  };

  vm.refreshUnmanagedDevices = function() {
    vm.unmanagedDevicesPrev = null;
    vm.unmanagedDevicesNext = null;
    DevicesService.deviceCache.removeAll();
    return vm.getUnmanagedDevices(vm.distributorKey, vm.unmanagedDevicesPrev, vm.unmanagedDevicesNext);
  };

  vm.changeRadio = function(unmanaged) {
    if (unmanaged) {
      vm.unmanagedSearchText = '';
      vm.unmanagedDisabled = true;
      vm.unmanagedSerialDevices = {};
      return vm.unmanagedMacDevices = {};

    } else {
      vm.searchText = '';
      vm.disabled = true;
      vm.serialDevices = {};
      return vm.macDevices = {};
    }
  };

  vm.convertArrayToDictionary = function(theArray, mac) {
    let devices = {};
    for (let i = 0; i < theArray.length; i++) {
      let item = theArray[i];
      if (mac) {
        devices[item.mac] = item;
      } else {
        devices[item.serial] = item;
      }
    }

    return devices;
  };

  vm.prepareForEditView = function(unmanaged, searchText) {
    if (unmanaged) {
      var mac = vm.unmanagedSelectedButton === "MAC";
      if (mac) {
        return vm.editItem(vm.unmanagedMacDevices[searchText]);
      } else {
        return vm.editItem(vm.unmanagedSerialDevices[searchText]);
      }

    } else {
      var mac = vm.selectedButton === "MAC";
      if (mac) {
        return vm.editItem(vm.macDevices[searchText]);
      } else {
        return vm.editItem(vm.serialDevices[searchText]);
      }
    }
  };


  vm.controlOpenButton = function(unmanaged, isMatch) {
    if (!unmanaged) {
      vm.disabled = !isMatch;
      return vm.disabledButtonLoading = false;

    } else {
      vm.unmanagedDisabled = !isMatch;
      return vm.unmanagedDisabledButtonLoading = false;
    }
  };

  vm.isResourceValid = function(unmanaged, resource) {
    if (resource) {
      if (resource.length > 2) {
        if (unmanaged) {
          var mac = vm.unmanagedSelectedButton === "MAC";
          vm.unmanagedDisabledButtonLoading = true;

        } else {
          var mac = vm.selectedButton === "MAC";
          vm.disabledButtonLoading = true;
        }

        if (mac) {
          return DevicesService.matchDevicesByFullMac(vm.distributorKey, resource, unmanaged)
          .then(res => vm.controlOpenButton(unmanaged, res["is_match"]));

        } else {
          return DevicesService.matchDevicesByFullSerial(vm.distributorKey, resource, unmanaged)
          .then(res => vm.controlOpenButton(unmanaged, res["is_match"]));
        }

      } else {
        return vm.controlOpenButton(unmanaged, false);
      }

    } else {
      return vm.controlOpenButton(unmanaged, false);
    }
  };


  vm.searchDevices = function(unmanaged, partial) {
    if (partial) {
      if (partial.length > 2) {
        if (unmanaged) { var button = vm.unmanagedSelectedButton; } else { var button = vm.selectedButton; }

        if (button === "Serial Number") {
          return DevicesService.searchDevicesByPartialSerial(vm.distributorKey, partial, unmanaged)
          .then(function(res) {
            let result = res["serial_number_matches"];
            if (unmanaged) {
              vm.unmanagedSerialDevices = vm.convertArrayToDictionary(result, false);
            } else {
              vm.serialDevices = vm.convertArrayToDictionary(result, false);
            }
              
            let serialsOfMatchedDevices = [];
            for (let i = 0; i < result.length; i++) {
              let each = result[i];
              serialsOfMatchedDevices.push(each.serial);
            }
              
            return serialsOfMatchedDevices;
          });

        } else {
          return DevicesService.searchDevicesByPartialMac(vm.distributorKey, partial, unmanaged)
          .then(function(res) {
            let result = res["mac_matches"];

            if (unmanaged) {
              vm.unmanagedMacDevices = vm.convertArrayToDictionary(result, true);
            } else {
              vm.macDevices = vm.convertArrayToDictionary(result, true);
            }

            let macMatchesMacAddresses = [];
            for (let i = 0; i < result.length; i++) {
              let each = result[i];
              macMatchesMacAddresses.push(each.mac);
            }

            return macMatchesMacAddresses;
          });
        }

      } else {
        return [];
      }
    } else {
      return [];
    }
  };


  vm.getManagedDevices = function(key, prev, next) {
    ProgressBarService.start();
    let devicesPromise = DevicesService.getDevicesByDistributor(key, prev, next);
    return devicesPromise.then((function(response) {
      vm.devices = response.devices;
      vm.devicesNext = response.next_cursor;
      vm.devicesPrev = response.prev_cursor;
      return vm.getFetchSuccess();
    }), response => vm.getFetchFailure(response));
  };


  vm.getUnmanagedDevices = function(key, prev, next) {
    ProgressBarService.start();
    let unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByDistributor(key, prev, next);
    return unmanagedDevicesPromise.then((function(response) {
      vm.unmanagedDevices = response.devices;
      vm.unmanagedDevicesPrev = response.prev_cursor;
      vm.unmanagedDevicesNext = response.next_cursor;
      return vm.getFetchSuccess();
    }), response => vm.getFetchFailure(response));
  };

  vm.initialize = function() {
    vm.distributorKey = SessionsService.getCurrentDistributorKey();
    vm.getManagedDevices(vm.distributorKey, vm.devicesPrev, vm.devicesNext);
    return vm.getUnmanagedDevices(vm.distributorKey, vm.unmanagedDevicesPrev, vm.unmanagedDevicesNext);
  };

  vm.getFetchSuccess = () => ProgressBarService.complete();

  vm.getFetchFailure = function(response) {
    ProgressBarService.complete();
    let errorMessage = `Unable to fetch devices. Error: ${response.status} ${response.statusText}.`;
    return sweet.show('Oops...', errorMessage, 'error');
  };

  vm.editItem = item =>
    $state.go('editDevice', {
      deviceKey: item.key,
      tenantKey: item.tenantKey,
      fromDevices: true
    })
  ;

  vm.paginateCall = function(forward, managed) {
    if (forward) {
      if (managed) {
        vm.getManagedDevices(vm.distributorKey, null, vm.devicesNext);
      }

      if (!managed) {
        vm.getUnmanagedDevices(vm.distributorKey, null, vm.unmanagedDevicesNext);
      }
    }

    if (!forward) {
      if (managed) {
        vm.getManagedDevices(vm.distributorKey, vm.devicesPrev, null);
      }

      if (!managed) {
        return vm.getUnmanagedDevices(vm.distributorKey, vm.unmanagedDevicesPrev, null);
      }
    }
  };

  return vm;
});
})
();