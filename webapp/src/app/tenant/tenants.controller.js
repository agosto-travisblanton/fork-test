function TenantsCtrl($state, $log, TenantsService, ProgressBarService, sweet) {
  "ngInject";

  let vm = this;

  // Paginated Tenants
  vm.tenants = [];
  // Current Search of Tenants Results
  vm.searchedTenants = [];
  vm.searchMatch = null;
  vm.searchDisabled = true;

  vm.getTenantsPaginated = function (page_size, offset) {
    vm.offset = offset;
    vm.loading = true;
    ProgressBarService.start();
    let promise = TenantsService.fetchAllTenantsPaginated(page_size, offset);
    return promise.then((response => vm.getFetchSuccess(response)), response => vm.getFetchFailure(response));
  };

  vm.getFetchSuccess = function (response) {
    vm.tenants = response.tenants;
    vm.total = response.total;
    vm.is_first_page = response.is_first_page;
    vm.is_last_page = response.is_last_page;
    ProgressBarService.complete();
    return vm.loading = false;
  };

  vm.getFetchFailure = function (response) {
    ProgressBarService.complete();
    let errorMessage = `Unable to fetch tenants. Error: ${response.status} ${response.statusText}.`;
    return sweet.show('Oops...', errorMessage, 'error');
  };


  vm.initialize = function () {
    vm.offset = 0;
    vm.searchAllTenantsByName('my')
    return vm.getTenantsPaginated(100, vm.offset);
  };

  vm.searchAllTenantsByName = function (tenant_name) {
    if (!tenant_name || tenant_name.length < 3) {
      return []
    }
    return TenantsService.searchAllTenantsByName(tenant_name)
      .then((response) => {
        vm.searchedTenants = response["matches"]
        return vm.searchedTenants.map((i) => i.name)
      })
      .catch((response) => {
        let errorMessage = `Unable to fetch tenants. Error: ${response.status}`;
        return sweet.show('Oops...', errorMessage, 'error');
      })
  }

  vm.isTenantValid = (tenant_name) => {
    if (!tenant_name || tenant_name.length < 3) {
      return []
    }
    TenantsService.searchAllTenantsByName(tenant_name)
      .then((response) => {
        let match = response["matches"][0]
        if (match) {
          vm.searchMatch = match
          vm.searchDisabled = !(tenant_name === match.name)
        } else {
          vm.searchDisabled = true;
        }
      })
  }

  vm.editItem = item => $state.go('tenantDetails', {tenantKey: item.key});

  vm.deleteItem = function (item) {
    let callback = function () {
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
}
export {TenantsCtrl}
