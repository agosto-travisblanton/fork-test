function TenantUnmanagedDevicesCtrl($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) {
  "ngInject";

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
  vm.devicesToMatchOn = [];
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

  vm.editItem = (item) => DevicesService.editItem(item)

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
    vm.macDevices = {};
    vm.devicesToMatchOn = [];
  };

  vm.searchDevices = function (partial) {
    let unmanaged = true;
    let byTenant = true;
    return DevicesService.searchDevices(partial, vm.selectedButton, byTenant, vm.tenantKey, vm.distributorKey, unmanaged)
      .then(function (response) {
        let devicesToReturn;
        if (response.success) {
          let devices = response.devices
          if (vm.selectedButton === "Serial Number") {
            vm.serialDevices = devices[1]
            devicesToReturn = devices[0]
          } else if (vm.selectedButton === "MAC") {
            vm.macDevices = devices[1]
            devicesToReturn = devices[0]
          } else {
            vm.gcmidDevices = devices[1]
            devicesToReturn = devices[0]
          }
          vm.devicesToMatchOn = devicesToReturn
          return devicesToReturn
        } else {
          return []
        }
      })

  };

  vm.paginateCall = function (forward) {
    if (forward) {
      return vm.getUnmanagedDevices(vm.tenantKey, null, vm.devicesNext);
    } else {
      return vm.getUnmanagedDevices(vm.tenantKey, vm.devicesPrev, null);
    }
  };

  vm.prepareForEditView = (searchText) => DevicesService.preprateForEditView(
    vm.selectedButton,
    vm.tenantKey,
    searchText,
    vm.macDevices,
    vm.serialDevices,
    vm.gcmidDevices
  )

  vm.controlOpenButton = function (isMatch) {
    vm.disabled = !isMatch;
    vm.loadingDisabled = false;
  };

  vm.isResourceValid = function (resource) {
    let foundMatch = false;
    for (let item of vm.devicesToMatchOn) {
      if (resource === item) {
        foundMatch = true;
      }
    }
    vm.controlOpenButton(foundMatch)
    return foundMatch
  };

  return vm;
}
export {TenantUnmanagedDevicesCtrl}
