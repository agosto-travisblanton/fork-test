(function () {

  let appModule = angular.module('skykitProvisioning');

  appModule.controller("DistributorSelectorCtrl", function ($log,
                                                            $state,
                                                            DistributorsService,
                                                            SessionsService) {
    let vm = this;
    vm.distributors = [];
    vm.currentDistributor = undefined;
    vm.loading = true;

    vm.initialize = function () {
      vm.loading = true;
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


    vm.selectDistributor = distributor => DistributorsService.switchDistributor(distributor);

    return vm;
  });

})
();
