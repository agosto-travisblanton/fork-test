let appModule = angular.module('skykitProvisioning');

appModule.controller('AppController', function($mdSidenav, $state, $window, SessionsService) {
  let vm = this;
  
  vm.identity = {};
  
  vm.currentDistributerInDistributerAdminList = function() {
    let currentDistributorName = SessionsService.getCurrentDistributorName();
    let distributorsAsAdmin = SessionsService.getDistributorsAsAdmin();
    return _.contains(distributorsAsAdmin, currentDistributorName);
  };

  vm.getIdentity = () =>
    vm.identity = {
      key: SessionsService.getUserKey(),
      email: SessionsService.getUserEmail(),
      admin: SessionsService.getIsAdmin(),
      distributor_admin: SessionsService.getDistributorsAsAdmin(),
      admin_of_current_distributor: vm.currentDistributerInDistributerAdminList(),
      distributorKey: SessionsService.getCurrentDistributorKey(),
      distributorName: SessionsService.getCurrentDistributorName()
    }
  ;

  vm.isCurrentURLDistributorSelector = function() {
    let result;
    let test = $window.location.href.search(/distributor_selection/);
    return result = test >= 0;
  };

  vm.initialize = () => vm.getIdentity();

  vm.toggleSidenav = () => $mdSidenav('left').toggle();

  vm.goTo = function(stateName, id) {
    $state.go(stateName, {id});
    if ($mdSidenav('left').isOpen()) { return $mdSidenav('left').close(); }
  };

  return vm;
});