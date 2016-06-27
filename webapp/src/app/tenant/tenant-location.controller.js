let appModule = angular.module('skykitProvisioning');

appModule.controller('TenantLocationCtrl',
  function($stateParams, TenantsService, LocationsService, $state, sweet, ProgressBarService, ToastsService) {
    let vm = this;
    vm.location = {
      key: undefined
    };
    vm.tenantKey = $stateParams.tenantKey;
    vm.editMode = !!$stateParams.locationKey;
    if (vm.editMode) {
      let locationPromise = LocationsService.getLocationByKey($stateParams.locationKey);
      locationPromise.then(function(data) {
        vm.location = data;
        vm.tenantKey = data.tenantKey;
        vm.locationName = data.customerLocationName;
        return vm.fetchTenantName(vm.tenantKey);
      });
    }

    vm.initialize = function() {
      if (!vm.editMode) {
        vm.fetchTenantName(vm.tenantKey);
        return vm.location = {
          tenantKey: vm.tenantKey,
          active: true
        };
      }
    };

    vm.onClickSaveButton = function() {
      ProgressBarService.start();
      let promise = LocationsService.save(vm.location);
      if (vm.editMode) {
        return promise.then(vm.onSuccessUpdatingLocation(vm.tenantKey), vm.onFailureSavingLocation);
      } else {
        return promise.then(vm.onSuccessSavingLocation, vm.onFailureSavingLocation);
      }
    };

    vm.onSuccessSavingLocation = function(){
      ProgressBarService.complete();
      ToastsService.showSuccessToast('We saved your location.');
      return setTimeout((function() {
        $state.go('tenantLocations', {tenantKey: $stateParams.tenantKey});
        return;
      }), 1000);
    };

    vm.onSuccessUpdatingLocation = function(tenant_key){
      ProgressBarService.complete();
      ToastsService.showSuccessToast('We updated your location.');
      return setTimeout((function() {
        $state.go('tenantLocations', {tenantKey: tenant_key});
        return;
      }), 1000);
    };

    vm.onFailureSavingLocation = function(response) {
      ProgressBarService.complete();
      if (response.status === 409) {
        ToastsService.showErrorToast('Location code conflict. Unable to save your location.');
        return sweet.show('Oops...',
          'Please change your customer location name. Location name must generate a unique location code.',
          'error');
      } else {
        return ToastsService.showErrorToast('Unable to save your location.');
      }
    };

    vm.fetchTenantName = function(tenantKey) {
      let tenantPromise = TenantsService.getTenantByKey(tenantKey);
      return tenantPromise.then(tenant => vm.tenantName = tenant.name);
    };

    vm.autoGenerateCustomerLocationCode = function() {
      if (!vm.location.key) {
        let newCustomerLocationCode = '';
        if (vm.location.customerLocationName) {
          newCustomerLocationCode = vm.location.customerLocationName.toLowerCase();
          newCustomerLocationCode = newCustomerLocationCode.replace(/\s+/g, '_');
          newCustomerLocationCode = newCustomerLocationCode.replace(/\W+/g, '');
        }
        return vm.location.customerLocationCode = newCustomerLocationCode;
      }
    };

    return vm;
  });

