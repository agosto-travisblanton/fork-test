(function () {


  let appModule = angular.module('skykitProvisioning');

  appModule.controller('TenantDetailsCtrl',
    function ($stateParams, TenantsService, DomainsService, TimezonesService, DistributorsService, $state, sweet,
              ProgressBarService, ToastsService, SessionsService, $scope, $location) {
      let vm = this;
      vm.gameStopServer = $location.host().indexOf('provisioning-gamestop') > -1;
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
        proof_of_play_url: undefined,
        active: true
      };
      vm.selectedDomain = undefined;
      vm.distributorDomains = [];
      vm.timezones = [];
      vm.selectedTimezone = 'America/Chicago';
      vm.editMode = !!$stateParams.tenantKey;

      if (vm.editMode) {
        let tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey);
        tenantPromise.then(function (tenant) {
          vm.currentTenant = tenant;
          return vm.onSuccessResolvingTenant(tenant);
        });
      }

      vm.initialize = function () {
        let timezonePromise = TimezonesService.getCustomTimezones();
        timezonePromise.then(data => vm.timezones = data);
        vm.currentDistributorKey = SessionsService.getCurrentDistributorKey();
        let distributorDomainPromise = DistributorsService.getDomainsByKey(vm.currentDistributorKey);
        return distributorDomainPromise.then(domains => vm.distributorDomains = domains);
      };

      vm.onSuccessResolvingTenant = function (tenant) {
        vm.selectedTimezone = tenant.default_timezone;
        let domainPromise = DomainsService.getDomainByKey(tenant.domain_key);
        return domainPromise.then(data => vm.selectedDomain = data);
      };

      vm.onClickSaveButton = function () {
        ProgressBarService.start();
        vm.currentTenant.default_timezone = vm.selectedTimezone;
        vm.currentTenant.domain_key = vm.selectedDomain.key;
        let promise = TenantsService.save(vm.currentTenant);
        return promise.then(vm.onSuccessTenantSave, vm.onFailureTenantSave);
      };

      vm.onSuccessTenantSave = function () {
        ProgressBarService.complete();
        return ToastsService.showSuccessToast('We saved your tenant information.');
      };

      vm.onFailureTenantSave = function (errorObject) {
        ProgressBarService.complete();
        if (errorObject.status === 409) {
          return sweet.show('Oops...',
            'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.', 'error');
        } else {
          return sweet.show('Oops...', 'Unable to save the tenant.', 'error');
        }
      };

      vm.editItem = item => $state.go('editDevice', {deviceKey: item.key, tenantKey: $stateParams.tenantKey});

      vm.autoGenerateTenantCode = function () {
        if (!vm.currentTenant.key) {
          let newTenantCode = '';
          if (vm.currentTenant.name) {
            newTenantCode = vm.currentTenant.name.toLowerCase();
            newTenantCode = newTenantCode.replace(/\s+/g, '_');
            newTenantCode = newTenantCode.replace(/\W+/g, '');
          }
          return vm.currentTenant.tenant_code = newTenantCode;
        }
      };

      $scope.tabIndex = 0;

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
          }
        }
      });

      return vm;
    });

})
();
