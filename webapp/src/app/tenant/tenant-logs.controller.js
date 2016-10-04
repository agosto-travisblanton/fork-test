import naturalSort from 'javascript-natural-sort';


function TenantLogsCtrl($stateParams,
                        TenantsService,
                        $state,
                        ProgressBarService,
                        ToastsService,
                        $scope,
                        ImageService,
                        $timeout,
                        $mdDialog) {
  "ngInject";

  let vm = this;
  $scope.tabIndex = 5;
  vm.tenantKey = $stateParams.tenantKey;
  let tenantPromise = TenantsService.getTenantByKey(vm.tenantKey);
  tenantPromise.then(data => {
    vm.currentTenant = data
  });


  //////////////////////////////////////////////////////////////
  // Setup
  //////////////////////////////////////////////////////////////
  vm.onSuccessResolvingTenant = function (tenant) {
    vm.currentTenant = tenant;
    vm.currentTenantCopy = angular.copy(vm.currentTenant);
    vm.selectedTimezone = tenant.default_timezone;

  };

  vm.getTenant = () => {
    let tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey);
    tenantPromise.then(function (tenant) {
      vm.currentTenant = tenant;
      if (vm.currentTenant.overlaysUpdateInProgress) {
        vm.loading = true;
        $timeout(vm.getTenant, 3000);
      } else {
        vm.loading = false;
      }
      vm.currentTenantCopy = angular.copy(vm.currentTenant);
    })
    return tenantPromise
  }

  vm.initialize = () => {
    // vm.getTenantImages()
    vm.getTenant()
  }

  $scope.$watch('tabIndex', function (toTab, fromTab) {
    if (toTab !== undefined) {
      switch (toTab) {
        case 0:
          return $state.go('tenantDetails', {tenantKey: $stateParams.tenantKey});
        case 1:
          return $state.go('tenantManagedDevices', {tenantKey: $stateParams.tenantKey});
        case 2:
          return $state.go('tenantUnmanagedDevices', {tenantKey: $stateParams.tenantKey});
        case 3:
          return $state.go('tenantLocations', {tenantKey: $stateParams.tenantKey});
        case 4:
          return $state.go('tenantOverlays', {tenantKey: $stateParams.tenantKey});
        case 5:
          return $state.go('tenantLogs', {tenantKey: $stateParams.tenantKey});
      }
    }
  });

  return vm;
}

export {TenantLogsCtrl}
