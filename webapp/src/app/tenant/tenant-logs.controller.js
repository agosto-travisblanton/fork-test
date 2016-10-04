import naturalSort from 'javascript-natural-sort';


function TenantLogsCtrl($stateParams,
                        TenantsService,
                        $state,
                        ProgressBarService,
                        IntegrationEvents,
                        $scope,
                        DateManipulationService) {
  "ngInject";

  let vm = this;
  $scope.tabIndex = 5;
  vm.tenantKey = $stateParams.tenantKey;
  let tenantPromise = TenantsService.getTenantByKey(vm.tenantKey);
  tenantPromise.then(data => {
    vm.currentTenant = data
  });

  vm.localFromUtc = function (events) {
    for (let i = 0; i < events.length; i++) {
      let each = events[i];
      if (each.utcTimestamp) {
        each.utcTimestamp = DateManipulationService.generateLocalFromUTC(each.utcTimestamp);
      }
    }
    return;
  };

  vm.getTenantCreateEvents = function () {
    ProgressBarService.start();
    let enrollmentEventsPromise = IntegrationEvents.getTenantCreateEvents(vm.tenantKey);
    return enrollmentEventsPromise.then(function (data) {
      vm.tenantCreateEvents = data;
      vm.localFromUtc(data);
      return ProgressBarService.complete();
    });
  };


  //////////////////////////////////////////////////////////////
  // Setup
  //////////////////////////////////////////////////////////////

  vm.initialize = () => {
    vm.getTenantCreateEvents()
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
