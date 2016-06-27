(function () {

let appModule = angular.module('skykitProvisioning');
appModule.controller("WelcomeCtrl", function(VersionsService, $state, DistributorsService, SessionsService) {
  let vm = this;
  vm.version_data = [];
  vm.loading = true;

  vm.proceedToSignIn = () => $state.go('sign_in');

  vm.capitalizeFirstLetter = string => string.charAt(0).toUpperCase() + string.slice(1);

  vm.giveOptionToChangeDistributor = function() {
    let distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.getUserKey());
    return distributorsPromise.then(function(data) {
      vm.has_multiple_distributors = data.length > 1;
      return vm.loading = false;
    });
  };

  vm.changeDistributor = () => $state.go('distributor_selection');

  vm.getVersion = function() {
    let promise = VersionsService.getVersions();
    return promise.then(data => vm.version_data = data);
  };

  vm.initialize = function() {
    vm.identity = {
      key: SessionsService.getUserKey(),
      email: SessionsService.getUserEmail(),
      distributorKey: SessionsService.getCurrentDistributorKey(),
      distributorName: SessionsService.getCurrentDistributorName()
    };

    vm.giveOptionToChangeDistributor();

    if (!vm.identity.email) {
      return $state.go("sign_in");

    } else {
      return vm.getVersion();
    }
  };
  return vm;
});
})
();