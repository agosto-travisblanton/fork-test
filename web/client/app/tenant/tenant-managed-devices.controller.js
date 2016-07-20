function TenantManagedDevicesCtrl($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) {
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

  vm.editItem = (item) => DevicesService.editItem(item)

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
    return DevicesService.searchDevices(partial, button, byTenant, tenantKey, vm.distributorKey, unmanaged)
      .then(function (response) {
        if (response.success) {
          let devices = response.devices
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
        } else {
          return []
        }
      })
  };

  vm.paginateCall = function (forward) {
    if (forward) {
      return vm.getManagedDevices(vm.tenantKey, null, vm.devicesNext);

    } else {
      return vm.getManagedDevices(vm.tenantKey, vm.devicesPrev, null);
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
    return vm.loadingDisabled = false;
  };

  vm.isResourceValid = function (resource) {
    let unmanaged = false;
    let byTenant = true;
    return DevicesService.isResourceValid(resource, vm.selectedButton, byTenant, vm.tenantKey, vm.distributorKey, unmanaged)
      .then(res => vm.controlOpenButton(res["is_match"]));
  };

  return vm;
}
export {TenantManagedDevicesCtrl}
