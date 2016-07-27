function DomainDetailsCtrl($log,
                           $stateParams,
                           DistributorsService,
                           DomainsService,
                           $state,
                           sweet,
                           ProgressBarService,
                           ToastsService,
                           SessionsService) {
  "ngInject";

  let vm = this;
  vm.currentDomain = {
    key: undefined,
    name: undefined,
    impersonation_admin_email_address: undefined,
    distributor_key: undefined,
    active: true
  };
  vm.currentDomains = [];
  vm.editMode = !!$stateParams.domainKey;

  if (vm.editMode) {
    let domainPromise = DomainsService.getDomainByKey($stateParams.domainKey);
    domainPromise.then(data => vm.currentDomain = data);
  } else {
    vm.currentDomain.distributor_key = SessionsService.getCurrentDistributorKey();
  }

  vm.onSaveDomain = function () {
    ProgressBarService.start();
    let promise = DomainsService.save(vm.currentDomain);
    return promise.then(vm.onSuccessSaveDomain, vm.onFailureSaveDomain);
  };

  vm.onSuccessSaveDomain = function () {
    ProgressBarService.complete();
    return ToastsService.showSuccessToast('We saved your update.');
  };

  vm.onFailureSaveDomain = function (error) {
    ProgressBarService.complete();
    if (error.status === 409) {
      $log.info(`Failure saving domain. Domain already exists: ${error.status} ${error.statusText}`);
      return sweet.show('Oops...', 'This domain name already exist. Please enter a unique domain name.', 'error');
    } else {
      $log.error(`Failure saving domain: ${error.status } ${error.statusText}`);
      return ToastsService.showErrorToast('Oops. We were unable to save your updates at this time.');
    }
  };

  vm.editItem = item => $state.go('editDomain', {domainKey: item.key});


  return vm;
}

export {DomainDetailsCtrl}