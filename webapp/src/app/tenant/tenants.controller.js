let appModule = angular.module('skykitProvisioning');

appModule.controller("TenantsCtrl", function($state, $log, TenantsService, ProgressBarService, sweet) {
  let vm = this;
  
  vm.tenants = [];

  vm.getTenants = function(page_size, offset) {
    vm.offset = offset;
    vm.loading = true;
    ProgressBarService.start();
    let promise = TenantsService.fetchAllTenantsPaginated(page_size, offset);
    return promise.then((response => vm.getFetchSuccess(response)), response => vm.getFetchFailure(response));
  };

  vm.initialize = function() {
    vm.offset = 0;
    return vm.getTenants(100, vm.offset);
  };

  vm.getFetchSuccess = function(response) {
    vm.tenants = response.tenants;
    vm.total = response.total;
    vm.is_first_page = response.is_first_page;
    vm.is_last_page = response.is_last_page;
    ProgressBarService.complete();
    return vm.loading = false;
  };

  vm.getFetchFailure = function(response) {
    ProgressBarService.complete();
    let errorMessage = `Unable to fetch tenants. Error: ${response.status} ${response.statusText}.`;
    return sweet.show('Oops...', errorMessage, 'error');
  };

  vm.editItem = item => $state.go('tenantDetails', {tenantKey: item.key});

  vm.deleteItem = function(item) {
    let callback = function() {
      let promise = TenantsService.delete(item);
      return promise.then(() => vm.initialize());
    };
    
    return sweet.show({
      title: "Are you sure?",
      text: "This will permanently remove the tenant from the system.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, remove the tenant!",
      closeOnConfirm: true
    }, callback);
  };

  return vm;
});