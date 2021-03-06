function DevicesListingCtrl($stateParams,
                            $q,
                            debounce,
                            $log,
                            DevicesService,
                            $state,
                            SessionsService,
                            ProgressBarService,
                            sweet) {
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
  vm.throttledSearch = null;

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
  vm.devicesToMatchOnUnmanaged = [];
  vm.devicesToMatchOnManaged = [];

  ////////////////////////////////////////////////////////////////////////////

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
      vm.unmanagedMacDevices = {};
      vm.devicesToMatchOnUnmanaged = [];
    } else {
      vm.searchText = '';
      vm.disabled = true;
      vm.serialDevices = {};
      vm.macDevices = {};
      vm.devicesToMatchOnManaged = [];
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
      vm.disabledButtonLoading = false;
    } else {
      vm.unmanagedDisabled = !isMatch;
      vm.unmanagedDisabledButtonLoading = false;
    }
  };


  vm.isResourceValid = function (unmanaged, resource) {
    let devicesToMatchOn = unmanaged ? vm.devicesToMatchOnUnmanaged : vm.devicesToMatchOnManaged
    let foundMatch = false;
    for (let item of devicesToMatchOn) {
      if (resource === item) {
        foundMatch = true;
      }
    }
    vm.controlOpenButton(unmanaged, foundMatch)
    return foundMatch
  };


  vm.searchDevices = function (unmanaged, partial) {
    let deferred = $q.defer()
    let button;
    if (unmanaged) {
      button = vm.unmanagedSelectedButton;
    } else {
      button = vm.selectedButton;
    }

    let byTenant = false;
    let tenantKey = null;

    if (vm.throttledSearch) {
      vm.throttledSearch.cancel();
    }

    vm.throttledSearch = debounce(750, function () {
      DevicesService.searchDevices(partial, button, byTenant, tenantKey, vm.distributorKey, unmanaged)
        .then(function (response) {
          let devicesToReturn;
          if (response.success) {
            let devices = response.devices;
            if (button === "Serial Number") {
              if (unmanaged) {
                vm.unmanagedSerialDevices = devices[1]
              } else {
                vm.serialDevices = devices[1]
              }
              devicesToReturn = devices[0]
            } else if (button === "MAC") {
              if (unmanaged) {
                vm.unmanagedMacDevices = devices[1]
              } else {
                vm.macDevices = devices[1]
              }
              devicesToReturn = devices[0]
            } else {
              if (unmanaged) {
                vm.unmanagedGCMidDevices = devices[1]
              } else {
                vm.gcmidDevices = devices[1]
              }
              devicesToReturn = devices[0]
            }
            if (unmanaged) {
              vm.devicesToMatchOnUnmanaged = devicesToReturn
            } else {
              vm.devicesToMatchOnManaged = devicesToReturn
            }
            deferred.resolve(devicesToReturn)
          } else {
            deferred.resolve([])
          }
        })
    })

    vm.throttledSearch();

    return deferred.promise

  }

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
    } else {
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

