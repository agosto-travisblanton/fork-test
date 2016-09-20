function TenantOverlaysCtrl($stateParams, TenantsService, DomainsService, TimezonesService, DistributorsService, $state, sweet,
                            ProgressBarService, ToastsService, SessionsService, $scope, $location) {
  "ngInject";

  let vm = this;

  $scope.tabIndex = 4;
  vm.editMode = !!$stateParams.tenantKey;

  vm.onSuccessResolvingTenant = function (tenant) {
    vm.selectedTimezone = tenant.default_timezone;
    let domainPromise = DomainsService.getDomainByKey(tenant.domain_key);
    return domainPromise.then(data => vm.selectedDomain = data);
  };

  if (vm.editMode) {
    let tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey);
    tenantPromise.then(function (tenant) {
      vm.currentTenant = tenant;
      return vm.onSuccessResolvingTenant(tenant);
    });
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

      }
    }
  });

  return vm;
}
export {TenantOverlaysCtrl}
