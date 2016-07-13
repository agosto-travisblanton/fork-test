(function () {


  let appModule = angular.module('skykitProvisioning');

  appModule.controller('DevicesListingCtrl', function ($stateParams, $log, DevicesService, $state, SessionsService, ProgressBarService, sweet) {
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

    vm.editItem = (item, tenantKey) => DevicesService.editItem(item, tenantKey)


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

    vm.prepareForEditView = function (unmanaged, searchText) {
      let button, macDevices, serialDevices, gcmidDevices;
      if (unmanaged) {
        button = vm.unmanagedSelectedButton;
        macDevices = vm.unmanagedMacDevices;
        serialDevices = vm.unmanagedSerialDevices;
        gcmidDevices = vm.unmanagedGCMidDevices;

      } else {
        button = vm.selectedButton;
        macDevices = vm.macDevices;
        serialDevices = vm.serialDevices;
        gcmidDevices = vm.gcmidDevices;
      }

      return DevicesService.preprateForEditView(
        button,
        vm.tenantKey,
        searchText,
        macDevices,
        serialDevices,
        gcmidDevices
      )
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

    vm.isResourceValid = function (resource) {
      let unmanaged = true;
      let button;
      if (unmanaged) {
        button = vm.unmanagedSelectedButton
      } else {
        button = vm.selectedButton;
      }

      return DevicesService.isResourceValid(resource, button, vm.tenantKey, unmanaged)
        .then(res => vm.controlOpenButton(res["is_match"]));
    };

    vm.isResourceValid = function (unmanaged, resource) {
      let byTenant = false;
      DevicesService.isResourceValid(resource, vm.selectedButton, byTenant, vm.tenantKey, vm.distributorKey, unmanaged)
        .then(res => vm.controlOpenButton(unmanaged, res["is_match"]));
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
  });
})
();
