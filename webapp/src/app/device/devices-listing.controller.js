function DevicesListingCtrl($stateParams, $log, DevicesService, $state, SessionsService, ProgressBarService, sweet) {
  "ngInject";
  let vm = this;
  vm.distributorKey = undefined;
  ////////////////////////////////////////////////////////////////////////////
  // Managed
  ////////////////////////////////////////////////////////////////////////////
  vm.devices = [];
  vm.devicesPrev = null;
  vm.devicesNext = null;
  vm.selectedButton = "Serial Number";
  vm.serialDevices = {};
  vm.disabled = true;
  vm.macDevices = {};
  vm.gcmidDevices = {};

  ////////////////////////////////////////////////////////////////////////////
  // Unmanaged
  ////////////////////////////////////////////////////////////////////////////
  vm.unmanagedSelectedButton = "MAC";
  vm.unmanagedSerialDevices = {};
  vm.unmanagedDisabled = true;
  vm.unmanagedDevicesPrev = null;
  vm.unmanagedDevicesNext = null;
  vm.unmanagedDevices = [];
  vm.unmanagedMacDevices = {};
  vm.unmanagedGCMidDevices = {};

  vm.refreshManagedDevices = function () {
    vm.devicesPrev = null;
    vm.devicesNext = null;
    return vm.getManagedDevices(vm.distributorKey, vm.devicesPrev, vm.devicesNext);
  };

  vm.refreshUnmanagedDevices = function () {
    vm.unmanagedDevicesPrev = null;
    vm.unmanagedDevicesNext = null;
    return vm.getUnmanagedDevices(vm.distributorKey, vm.unmanagedDevicesPrev, vm.unmanagedDevicesNext);
  };

  vm.changeRadio = function (unmanaged) {
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

  vm.editItem = (item) => DevicesService.editItem(item, true)

  vm.prepareForEditView = function (unmanaged, searchText) {
    let mac, serial, gcmid;
    if (unmanaged) {
      mac = vm.unmanagedSelectedButton === "MAC";
      serial = vm.unmanagedSelectedButton === "Serial Number";
      gcmid = vm.unmanagedSelectedButton === "GCM ID"
      if (mac) {
        return vm.editItem(vm.unmanagedMacDevices[searchText]);
      } else if (serial) {
        return vm.editItem(vm.unmanagedSerialDevices[searchText]);
      } else {
        return vm.editItem(vm.unmanagedGCMidDevices[searchText])
      }

    } else {
      mac = vm.selectedButton === "MAC";
      serial = vm.selectedButton === "Serial Number";
      gcmid = vm.selectedButton === "GCM ID"
      if (mac) {
        return vm.editItem(vm.macDevices[searchText]);
      } else if (serial) {
        return vm.editItem(vm.serialDevices[searchText]);
      } else {
        return vm.editItem(vm.gcmidDevices[searchText])
      }
    }
  }


  vm.controlOpenButton = function (unmanaged, isMatch) {
    if (!unmanaged) {
      vm.disabled = !isMatch;
      return vm.disabledButtonLoading = false;
    } else {
      vm.unmanagedDisabled = !isMatch;
      return vm.unmanagedDisabledButtonLoading = false;
    }
  };


  vm.isResourceValid = function (unmanaged, resource) {
    let button;
    if (unmanaged) {
      button = vm.unmanagedSelectedButton;
    } else {
      button = vm.selectedButton;
    }

    let byTenant = false;
    let tenantKey = null;

    return DevicesService.searchDevices(resource, button, byTenant, tenantKey, vm.distributorKey, unmanaged)
      .then(function (response) {
        if (response.success) {
          let devices = response.devices[0];
          let foundMatch = false;
          for (let eachDevice of devices) {
            if (resource === eachDevice) {
              foundMatch = true;
            }
          }
          return vm.controlOpenButton(unmanaged, foundMatch)
        } else {
          return vm.controlOpenButton(unmanaged, false)
        }
      })
  };


  vm.searchDevices = function (unmanaged, partial) {
    let button;
    if (unmanaged) {
      button = vm.unmanagedSelectedButton;
    } else {
      button = vm.selectedButton;
    }

    let byTenant = false;
    let tenantKey = null;

    return DevicesService.searchDevices(partial, button, byTenant, tenantKey, vm.distributorKey, unmanaged)
      .then(function (response) {
        if (response.success) {
          let devices = response.devices;
          if (button === "Serial Number") {
            if (unmanaged) {
              vm.unmanagedSerialDevices = devices[1]
            } else {
              vm.serialDevices = devices[1]
            }
            return devices[0]
          } else if (button === "MAC") {
            if (unmanaged) {
              vm.unmanagedMacDevices = devices[1]
            } else {
              vm.macDevices = devices[1]
            }
            return devices[0]
          } else {
            if (unmanaged) {
              vm.unmanagedGCMidDevices = devices[1]
            } else {
              vm.gcmidDevices = devices[1]
            }
            return devices[0]
          }
        } else {
          return []
        }
      })
  };

  vm.getManagedDevices = function (key, prev, next) {
    ProgressBarService.start();
    let devicesPromise = DevicesService.getDevicesByDistributor(key, prev, next);
    return devicesPromise.then((function (response) {
      vm.devices = response.devices;
      vm.devicesNext = response.next_cursor;
      vm.devicesPrev = response.prev_cursor;
      return vm.getFetchSuccess();
    }), response => vm.getFetchFailure(response));
  };

  vm.getUnmanagedDevices = function (key, prev, next) {
    ProgressBarService.start();
    let unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByDistributor(key, prev, next);
    return unmanagedDevicesPromise.then((function (response) {
      vm.unmanagedDevices = response.devices;
      vm.unmanagedDevicesPrev = response.prev_cursor;
      vm.unmanagedDevicesNext = response.next_cursor;
      return vm.getFetchSuccess();
    }), response => vm.getFetchFailure(response));
  };

  vm.initialize = function () {
    vm.distributorKey = SessionsService.getCurrentDistributorKey();
    vm.getManagedDevices(vm.distributorKey, vm.devicesPrev, vm.devicesNext);
    return vm.getUnmanagedDevices(vm.distributorKey, vm.unmanagedDevicesPrev, vm.unmanagedDevicesNext);
  };

  vm.getFetchSuccess = () => ProgressBarService.complete();

  vm.getFetchFailure = function (response) {
    ProgressBarService.complete();
    let errorMessage = `Unable to fetch devices. Error: ${response.status} ${response.statusText}.`;
    return sweet.show('Oops...', errorMessage, 'error');
  };


  vm.paginateCall = function (forward, managed) {
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
}
export {DevicesListingCtrl}

