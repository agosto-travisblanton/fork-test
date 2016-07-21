function DistributorSelectorCtrl($state,
                                 DistributorsService,
                                 SessionsService) {
  "ngInject";
  let vm = this;
  vm.distributors = [];
  vm.currentDistributor = undefined;
  vm.loading = true;

  vm.initialize = function () {
    vm.loeading = true;
    let distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.getUserKey());
    return distributorsPromise.then(function (data) {
      vm.distributors = data;
      if (vm.distributors.length === 1) {
        return vm.selectDistributor(vm.distributors[0]);
      } else {
        return vm.loading = false;
      }
    });
  };


  vm.selectDistributor = (distributor) => DistributorsService.switchDistributor(distributor);

  return vm;
}

export {DistributorSelectorCtrl}
