function TenantLocationsCtrl($scope, $stateParams, TenantsService, LocationsService, $state, ProgressBarService) {
  "ngInject";

  let vm = this;
  let {tenantKey} = $stateParams;
  $scope.tabIndex = 3;
  vm.locations = [];
  vm.searchDisabled = true;
  vm.tenantKey = $stateParams.tenantKey;

  let tenantPromise = TenantsService.getTenantByKey(tenantKey);
  tenantPromise.then(data => {
    vm.currentTenant = data
  });

  $scope.$watch('tabIndex', function (selectedIndex) {
    if (selectedIndex !== undefined) {
      switch (selectedIndex) {
        case 0:
          return $state.go('tenantDetails', {tenantKey});
        case 1:
          return $state.go('tenantManagedDevices', {tenantKey});
        case 2:
          return $state.go('tenantUnmanagedDevices', {tenantKey});
        case 3:
          return $state.go('tenantLocations', {tenantKey});
      }
    }
  });

  vm.getLocations = function (tenantKey, prev, next) {
    ProgressBarService.start();
    let locationsPromise = LocationsService.getLocationsByTenantKeyPaginated(tenantKey, prev, next);
    return locationsPromise.then(function (data) {
      vm.locations = data.locations;
      vm.next_cursor = data.next_cursor;
      vm.prev_cursor = data.prev_cursor;
      return ProgressBarService.complete();
    });
  };

  vm.searchAllTenantLocationsByName = (name) => {
    if (!name || name.length < 3) {
      return []
    }
    let promise = LocationsService.searchAllTenantLocationsByName(vm.tenantKey, name)
    return promise.then((response) => {
      vm.searchedTenantLocations = response
      if (vm.searchedTenantLocations) {
        return vm.searchedTenantLocations.map((i) => i.customerLocationName)
      } else {
        return []
      }
    })
    return promise.catch((response) => {
      let errorMessage = `Unable to fetch locations. Error: ${response.status}`;
      return sweet.show('Oops...', errorMessage, 'error');
    })
  };

  vm.isTenantLocationValid = (name) => {
    if (!name || name.length < 3) {
      return []
    }
    let promise = LocationsService.searchAllTenantLocationsByName(vm.tenantKey, name)
      .then((response) => {
        let match = response
        if (match) {
          for (let eachLocationName of match) {
            if (name === eachLocationName.customerLocationName) {
              vm.searchDisabled = false;
              vm.searchMatch = eachLocationName
              return;
            } else {
              vm.searchDisabled = true;
            }
          }
        } else {
          vm.searchDisabled = true;
        }
      })
  };

  vm.paginateCall = function (forward) {
    if (forward) {
      return vm.getLocations(tenantKey, null, vm.next_cursor);
    } else {
      return vm.getLocations(tenantKey, vm.prev_cursor, null);
    }
  };

  vm.initialize = function () {
    return vm.getLocations(tenantKey);
  };

  vm.editItem = item => $state.go('editLocation', {locationKey: item.key});


  return vm;
}

export {TenantLocationsCtrl}
