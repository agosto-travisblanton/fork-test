(function () {

let appModule = angular.module('skykitProvisioning');

appModule.controller('TenantAddCtrl',
  function($log, $location, TenantsService, DistributorsService, TimezonesService, $state, sweet, ProgressBarService,
    SessionsService) {
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

    vm.initialize = function() {
      let timezonePromise = TimezonesService.getCustomTimezones();
      timezonePromise.then(data => vm.timezones = data);
      vm.currentDistributorKey = SessionsService.getCurrentDistributorKey();
      let distributorPromise = DistributorsService.getByKey(vm.currentDistributorKey);
      distributorPromise.then(function(data) {
        vm.currentTenant.content_manager_base_url = data.content_manager_url;
        return vm.currentTenant.content_server_url = data.player_content_url;
      });
      let distributorDomainPromise = DistributorsService.getDomainsByKey(vm.currentDistributorKey);
      return distributorDomainPromise.then(domains => vm.distributorDomains = domains);
    };

    vm.onClickSaveButton = function() {
      ProgressBarService.start();
      vm.currentTenant.default_timezone = vm.selectedTimezone;
      vm.currentTenant.domain_key = vm.selectedDomain.key;
      let promise = TenantsService.save(vm.currentTenant);
      return promise.then(vm.onSuccessTenantSave, vm.onFailureTenantSave);
    };

    vm.onSuccessTenantSave = function() {
      ProgressBarService.complete();
      return $state.go('tenants');
    };

    vm.onFailureTenantSave = function(errorObject) {
      ProgressBarService.complete();
      if (errorObject.status === 409) {
        return sweet.show('Oops...',
          'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.', 'error');
      } else {
        $log.error(errorObject);
        return sweet.show('Oops...', 'Unable to save the tenant.', 'error');
      }
    };

    vm.autoGenerateTenantCode = function() {
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

    return vm;
  });
})
();