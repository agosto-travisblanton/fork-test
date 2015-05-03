'use strict'

angular.module "skykitDisplayDeviceManagement"
  .controller "MainCtrl", ($scope, $mdSidenav) ->
    $scope.toggleSidenav = (menuId) ->
      $mdSidenav(menuId).toggle()
