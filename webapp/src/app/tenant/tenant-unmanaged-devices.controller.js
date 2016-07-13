(function () {


  let appModule = angular.module('skykitProvisioning');

  appModule.controller('TenantUnmanagedDevicesCtrl',
    function ($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) {
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
      vm.gcmidDevices = [];
      vm.tenantDevices = [];
      vm.devicesPrev = null;
      vm.devicesNext = null;
      vm.selectedButton = "MAC";
      vm.serialDevices = {};
      vm.disabled = true;
      vm.macDevices = {};
      vm.editMode = !!$stateParams.tenantKey;
      vm.tenantKey = $stateParams.tenantKey;

      $scope.tabIndex = 2;

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

      vm.editItem = (item, tenantKey) => DevicesService.editItem(item, tenantKey)

      vm.getUnmanagedDevices = function (tenantKey, prev_cursor, next_cursor) {
        ProgressBarService.start();
        let devicesPromise = DevicesService.getUnmanagedDevicesByTenant(tenantKey, prev_cursor, next_cursor);
        return devicesPromise.then(function (data) {
          vm.devicesPrev = data["prev_cursor"];
          vm.devicesNext = data["next_cursor"];
          vm.tenantDevices = data["devices"];
          return ProgressBarService.complete();
        });
      };

      if (vm.editMode) {
        let tenantPromise = TenantsService.getTenantByKey(vm.tenantKey);
        tenantPromise.then(tenant => vm.currentTenant = tenant);
        vm.getUnmanagedDevices(vm.tenantKey, null, null);
      }

      vm.refreshDevices = function () {
        vm.devicesPrev = null;
        vm.devicesNext = null;
        vm.tenantDevices = null;
        return vm.getUnmanagedDevices(vm.tenantKey, vm.devicesPrev, vm.devicesNext);
      };

      vm.changeRadio = function () {
        vm.searchText = '';
        vm.disabled = true;
        vm.serialDevices = {};
        return vm.macDevices = {};
      };

      vm.searchDevices = function (partial) {
        let unmanaged = true;
        let button = vm.selectedButton;
        let byTenant = true;
        let tenantKey = vm.tenantKey;

        if (partial) {
          if (partial.length > 2) {
            DevicesService.searchDevices(partial, button, byTenant, tenantKey, vm.distributorKey, unmanaged)
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
          return vm.getUnmanagedDevices(vm.tenantKey, null, vm.devicesNext);
        } else {
          return vm.getUnmanagedDevices(vm.tenantKey, vm.devicesPrev, null);
        }
      };

      vm.prepareForEditView = function (searchText) {
        let mac, serial, gcmid;

        mac = vm.selectedButton === "MAC";
        serial = vm.selectedButton === "Serial Number";
        gcmid = vm.selectedButton === "GCM ID"

        if (mac) {
          return DevicesService.editItem(vm.macDevices[searchText], vm.tenantKey);
        } else if (serial) {
          return DevicesService.editItem(vm.serialDevices[searchText], vm.tenantKey);
        } else {
          return DevicesService.editItem(vm.gcmidDevices[searchText], vm.tenantKey)
        }

      };

      vm.controlOpenButton = function (isMatch) {
        vm.disabled = !isMatch;
        return vm.loadingDisabled = false;
      };

      vm.isResourceValid = function (resource) {
        let unmanaged = true;
        let byTenant = true;
        DevicesService.isResourceValid(resource, vm.selectedButton, byTenant, vm.tenantKey, vm.distributorKey, unmanaged)
          .then(res => vm.controlOpenButton(res["is_match"]));
      };

      return vm;
    });


})
();
