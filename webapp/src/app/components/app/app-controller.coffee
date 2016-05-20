'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller 'AppController', ($mdSidenav, $state, StorageService, $window, SessionsService) ->
  vm = @

  vm.identity = {}

  @getIdentity = () ->
    vm.identity = {
      key: StorageService.get('userKey')
      email: StorageService.get('userEmail')
      admin: SessionsService.getIsAdmin()
      distributor_admin: SessionsService.getDistributorsAsAdmin()
      distributorKey: StorageService.get('currentDistributorKey')
      distributorName: StorageService.get('currentDistributorName')
    }


  @isCurrentURLDistributorSelector = () ->
    test = $window.location.href.search /distributor_selection/
    result = test >= 0

  vm.initialize = ->
    @getIdentity()

  vm.toggleSidenav = ->
    $mdSidenav('left').toggle()

  vm.goTo = (stateName, id) ->
    $state.go stateName, {id: id}
    $mdSidenav('left').close() if $mdSidenav('left').isOpen()

  vm
