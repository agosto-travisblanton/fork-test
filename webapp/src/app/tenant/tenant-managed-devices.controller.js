(function () {


  let appModule = angular.module('skykitProvisioning');

  appModule.controller('TenantManagedDevicesCtrl', function ($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) {
    let vm = this;
    vm.currentTenant = {
      key: undefined,
      name: undefined,
      tenant_code: undefined,
      admin_email: undefined,
      content_server_url: undefined,
      content_manager_base_url: undefined,
      domain_key: undefined,
      notification_emails: undefined,
      proof_of_play_logging: false,
      active: true
    };
    vm.tenantDevices = [];
    vm.devicesPrev = null;
    vm.devicesNext = null;
    vm.selectedButton = "Serial Number";
    vm.serialDevices = {};
    vm.disabled = true;
    vm.macDevices = {};
    vm.editMode = !!$stateParams.tenantKey;
    vm.tenantKey = $stateParams.tenantKey;

    vm.getManagedDevices = function (tenantKey, prev_cursor, next_cursor) {
      ProgressBarService.start();
      let devicesPromise = DevicesService.getDevicesByTenant(tenantKey, prev_cursor, next_cursor);
      return devicesPromise.then(function (data) {
        vm.devicesPrev = data["prev_cursor"];
        vm.devicesNext = data["next_cursor"];
        vm.tenantDevices = data["devices"];
        return ProgressBarService.complete();
      });
    };

    vm.editItem = (item, tenantKey) => DevicesService.editItem(item, tenantKey)

    vm.refreshDevices = function () {
      vm.devicesPrev = null;
      vm.devicesNext = null;
      vm.tenantDevices = null;
      return vm.getManagedDevices(vm.tenantKey, vm.devicesPrev, vm.devicesNext);
    };

    if (vm.editMode) {
      let tenantPromise = TenantsService.getTenantByKey(vm.tenantKey);
      tenantPromise.then(tenant => vm.currentTenant = tenant);
      vm.getManagedDevices(vm.tenantKey, null, null);
    }

    $scope.tabIndex = 1;

    $scope.$watch('tabIndex', function (toTab, fromTab) {
      if (toTab !== undefined) {
        switch (toTab) {
          case 0:
            return $state.go('tenantDetails', {tenantKey: vm.tenantKey});
          case 1:
            return $state.go('tenantManagedDevices', {tenantKey: vm.tenantKey});
          case 2:
            return $state.go('tenantUnmanagedDevices', {tenantKey: vm.tenantKey});
          case 3:
            return $state.go('tenantLocations', {tenantKey: vm.tenantKey});
        }
      }
    });


    DevicesService.convertDevicesArrayToDictionaryObj = function (theArray, mac) {
      let Devices = {};
      for (let i = 0; i < theArray.length; i++) {
        let item = theArray[i];
        if (mac) {
          Devices[item.mac] = item;
        } else {
          Devices[item.serial] = item;
        }
      }
      return Devices;
    };

    vm.changeRadio = function () {
      vm.searchText = '';
      vm.disabled = true;
      vm.serialDevices = {};
      return vm.macDevices = {};
    };


    vm.searchDevices = function (partial) {
      let unmanaged = false;
      let button = vm.selectedButton;
      let byTenant = true;
      let tenantKey = vm.tenantKey;

      if (partial) {
        if (partial.length > 2) {
          return DevicesService.searchDevices(partial, button, byTenant, tenantKey, vm.distributorKey, unmanaged)
            .then(function (devices) {
              if (button === "Serial Number") {
                vm.serialDevices = devices[1]
                return devices[0]
              } else if (button === "MAC") {
                vm.macDevices = devices[1]
                return devices[0]
              } else {
                vm.gcmidDevices = devices[1]
                return devices[0]
              }
            })
        } else {
          return [];
        }
      } else {
        return [];
      }
    };

    vm.paginateCall = function (forward) {
      if (forward) {
        return vm.getManagedDevices(vm.tenantKey, null, vm.devicesNext);

      } else {
        return vm.getManagedDevices(vm.tenantKey, vm.devicesPrev, null);
      }
    };


    vm.prepareForEditView = function (searchText) {
      let mac = vm.selectedButton === "MAC";
      if (mac) {
        return DevicesService.editItem(vm.macDevices[searchText], vm.tenantKey);
      } else {
        return DevicesService.editItem(vm.serialDevices[searchText], vm.tenantKey);
      }
    };


    vm.controlOpenButton = function (isMatch) {
      vm.disabled = !isMatch;
      return vm.loadingDisabled = false;
    };


    vm.isResourceValid = function (resource) {
      if (resource) {
        if (resource.length > 2) {
          let mac = vm.selectedButton === "MAC";
          vm.loadingDisabled = true;

          if (mac) {
            return DevicesService.matchDevicesByFullMacByTenant(vm.tenantKey, resource, false)
              .then(res => vm.controlOpenButton(res["is_match"]));

          } else {
            return DevicesService.matchDevicesByFullSerialByTenant(vm.tenantKey, resource, false)
              .then(res => vm.controlOpenButton(res["is_match"]));
          }

        } else {
          return vm.controlOpenButton(false);
        }

      } else {
        return vm.controlOpenButton(false);
      }
    };

    return vm;
  });
})
();
