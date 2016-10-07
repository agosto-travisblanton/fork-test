import naturalSort from 'javascript-natural-sort';


function AdminCtrl(AdminService,
                   SessionsService,
                   DevicesService,
                   ToastsService,
                   $state,
                   $mdDialog,
                   TenantsService,
                   DistributorsService) {
  "ngInject";

  let vm = this;
  //////////////////////////////////////////
  // Device Search Variables
  //////////////////////////////////////////
  vm.selectedButton = "Serial Number";
  vm.unmanagedSelectedButton = "Managed"
  vm.serialDevices = {};
  vm.disabled = true;
  vm.macDevices = {};
  vm.gcmidDevices = {};
  vm.devicesToMatchOn = [];
  //////////////////////////////////////////
  // Tenant Search Variables
  //////////////////////////////////////////
  vm.searchedTenants = [];
  vm.tenantSearchMatch = null;
  vm.tenantSearchDisabled = true;

  //////////////////////////////////////////
  // Device Search
  //////////////////////////////////////////
  vm.controlOpenButton = function (isMatch) {
    vm.disabled = !isMatch;
    return vm.loadingDisabled = false;
  };

  vm.changeRadio = function () {
    vm.searchText = '';
    vm.disabled = true;
    vm.serialDevices = {};
    vm.macDevices = {};
    vm.devicesToMatchOn = [];
  };

  vm.isResourceValid = function (resource) {
    let foundMatch = false;
    for (let item of vm.devicesToMatchOn) {
      if (resource === item) {
        foundMatch = true;
      }
    }
    vm.controlOpenButton(foundMatch)
    return foundMatch
  };

  vm.searchDevices = function (unmanaged, partial) {
    let button = vm.selectedButton;
    let byTenant = false;
    let tenantKey = null;
    let distributor = null;
    let globally = true;

    return DevicesService.searchDevices(partial, button, byTenant, tenantKey, distributor, unmanaged, globally)
      .then(function (response) {
        console.log(response)
        let devicesToReturn;
        if (response.success) {
          let devices = response.devices;
          if (button === "Serial Number") {
            vm.serialDevices = devices[1]
            devicesToReturn = devices[0]
          } else if (button === "MAC") {
            vm.macDevices = devices[1]
            devicesToReturn = devices[0]
          } else {
            vm.gcmidDevices = devices[1]
            devicesToReturn = devices[0]
          }

          vm.devicesToMatchOn = devicesToReturn

          return devicesToReturn;
        } else {
          return []
        }
      })
  };


  //////////////////////////////////////////
  // Tenant Search
  //////////////////////////////////////////

  vm.searchAllTenantsByName = function (tenant_name) {
    if (!tenant_name || tenant_name.length < 3) {
      return []
    }
    let promise = TenantsService.searchAllTenantsByName(tenant_name, true)
    return promise.then((response) => {
      vm.searchedTenants = response
      if (vm.searchedTenants) {
        return vm.searchedTenants.map((i) => i.name).sort(naturalSort)
      } else {
        return []
      }
    })
    return promise.catch((response) => {
      let errorMessage = `Unable to fetch tenants. Error: ${response.status}`;
      return sweet.show('Oops...', errorMessage, 'error');
    })
  }


  vm.isTenantValid = (tenant_name) => {
    if (!tenant_name || tenant_name.length < 3) {
      return []
    }

    let match = vm.searchedTenants;
    if (match) {
      for (let eachName of match) {
        if (tenant_name === eachName.name) {
          vm.tenantSearchDisabled = false;
          vm.searchMatch = eachName
          return;
        } else {
          vm.tenantSearchDisabled = true;
        }
      }
    } else {
      vm.tenantSearchDisabled = true;
    }
  }

  //////////////////////////////////////////
  // Distributor Tab
  //////////////////////////////////////////

  vm.getAllDistributors = function () {
    vm.loadingAllDistributors = true;
    let getAllDistributorsPromise = AdminService.getAllDistributors();
    return getAllDistributorsPromise.then(function (data) {
      vm.loadingAllDistributors = false;
      return vm.allDistributors = data;
    });
  };

  vm.makeDistributor = function (ev, distributorName, adminEmail, form) {
    let confirm = $mdDialog.confirm(
      {
        title: 'Are you sure?',
        textContent: `If you proceed, ${distributorName} will be created.`,
        targetEvent: ev,
        ariaLabel: 'Lucky day',
        ok: 'Yeah!',
        cancel: 'Forget it.'
      }
    );
    return $mdDialog.show(confirm).then((function () {
      let makeDistributorPromise = AdminService.makeDistributor(distributorName, adminEmail);
      makeDistributorPromise.then(function (data) {
        vm.distributor = {};
        form.$setPristine();
        form.$setUntouched();
        ToastsService.showSuccessToast(data.message);
        return setTimeout((() => vm.allDistributors = vm.getAllDistributors()), 2000);
      });

      return makeDistributorPromise.catch(data => ToastsService.showErrorToast(data.data.message));
    }));
  };

  //////////////////////////////////////////
  // Users Tab
  //////////////////////////////////////////

  vm.addUserToDistributor = function (ev, userEmail, distributorAdmin, whichDistributor, form) {
    if (!distributorAdmin) {
      distributorAdmin = false;
    }
    let withOrWithout = distributorAdmin ? "with" : "without";

    // no option to select distributor is given when there is only one option
    if (!whichDistributor) {
      whichDistributor = vm.distributorsAsAdmin[0];
    }

    let confirm = $mdDialog.confirm(
      {
        title: 'Are you sure?',
        textContent: `${userEmail} will be added to ${whichDistributor}
        ${withOrWithout} administrator privileges`,
        targetEvent: ev,
        ok: 'Of course!',
        cancel: 'Oops, nevermind.'
      }
    );

    return $mdDialog.show(confirm).then(function () {
      let addUserToDistributorPromise = AdminService.addUserToDistributor(userEmail, whichDistributor, distributorAdmin);
      addUserToDistributorPromise.then(function (data) {
        ToastsService.showSuccessToast(data.message);
        vm.user = {};
        form.$setPristine();
        form.$setUntouched();
        return setTimeout((() => vm.getUsersOfDistributor()), 2000);
      });

      return addUserToDistributorPromise.catch(data => ToastsService.showErrorToast(data.data.message));
    });
  };

  vm.switchDistributor = function (distributor) {
    DistributorsService.switchDistributor(distributor);
    return ToastsService.showSuccessToast(`Distributor ${distributor.name} selected!`);
  };


  vm.getUsersOfDistributor = function () {
    vm.loadingUsersOfDistributor = true;
    let currentDistributorKey = SessionsService.getCurrentDistributorKey();
    let usersofDistributorPromise = AdminService.getUsersOfDistributor(currentDistributorKey);
    return usersofDistributorPromise.then(function (data) {
      vm.loadingUsersOfDistributor = false;
      return vm.usersOfDistributor = data;
    });
  };

  vm.initialize = function () {
    vm.getUsersOfDistributor();
    vm.getAllDistributors();
    vm.isAdmin = SessionsService.getIsAdmin();
    vm.distributorsAsAdmin = SessionsService.getDistributorsAsAdmin();
    vm.currentDistributorName = SessionsService.getCurrentDistributorName();

    if (vm.isAdmin) {
      return vm.getAllDistributors();
    }
  };

  vm.editTenant = item => $state.go('tenantDetails', {tenantKey: item.key});

  vm.editItem = (item) => DevicesService.editItem(item, true)


  return vm;
}

export {AdminCtrl}
