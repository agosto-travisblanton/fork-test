import contains from 'lodash.contains';

function AppController($mdSidenav, $state, $window, SessionsService) {
  "ngInject";

  let vm = this;
  
  console.log("@@@@@@@@@@@@@@@@@")

  vm.identity = {};

  vm.currentDistributerInDistributerAdminList = function () {
    let currentDistributorName = SessionsService.getCurrentDistributorName();
    let distributorsAsAdmin = SessionsService.getDistributorsAsAdmin();
    return contains(distributorsAsAdmin, currentDistributorName);
  };
  
  vm.identity = {
    key: SessionsService.getUserKey(),
    email: SessionsService.getUserEmail(),
    admin: SessionsService.getIsAdmin(),
    distributor_admin: SessionsService.getDistributorsAsAdmin(),
    admin_of_current_distributor: vm.currentDistributerInDistributerAdminList(),
    distributorKey: SessionsService.getCurrentDistributorKey(),
    distributorName: SessionsService.getCurrentDistributorName()
  }

  vm.getIdentity = () => {
    return vm.identity
  };

  vm.isCurrentURLDistributorSelector = function () {
    let test = $window.location.href.search(/distributor_selection/);
    let result = test >= 0;
    return result
  };

  vm.initialize = () => vm.getIdentity();

  vm.toggleSidenav = () => $mdSidenav('left').toggle();

  vm.goTo = function (stateName, id) {
    $state.go(stateName, {id});
    if ($mdSidenav('left').isOpen()) {
      return $mdSidenav('left').close();
    }
  };

  return vm;
}

export {AppController}
