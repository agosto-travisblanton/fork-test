'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller 'AppController', ($mdSidenav, $state, $window, SessionsService) ->
  vm = @
  
  vm.identity = {}
  
  vm.currentDistributerInDistributerAdminList = () ->
  currentDistributorName = SessionsService.getCurrentDistributorName()
  distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()
  _.contains(distributorsAsAdmin, currentDistributorName)

  vm.getIdentity = () ->
    vm.identity = {
      key: SessionsService.getUserKey()
      email: SessionsService.getUserEmail()
      admin: SessionsService.getIsAdmin()
      distributor_admin: SessionsService.getDistributorsAsAdmin()
      admin_of_current_distributor: vm.currentDistributerInDistributerAdminList()
      distributorKey: SessionsService.getCurrentDistributorKey()
      distributorName: SessionsService.getCurrentDistributorName()
    }
    vm.identity  


  vm.isCurrentURLDistributorSelector = () ->
    test = $window.location.href.search /distributor_selection/
    result = test >= 0

  vm.initialize = ->
    vm.getIdentity()

  vm.toggleSidenav = ->
    $mdSidenav('left').toggle()

  vm.goTo = (stateName, id) ->
    $state.go stateName, {id: id}
    $mdSidenav('left').close() if $mdSidenav('left').isOpen()

  vm