'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller 'AppController', ($mdSidenav, $state, $cookies, $window, SessionsService) ->
  vm = @

  vm.identity = {}

  @getIdentity = () ->
    vm.identity = {
      key: Lockr.get('userKey')
      email: Lockr.get('userEmail')
      admin: SessionsService.getIsAdmin()
      distributor_admin: SessionsService.getDistributorsAsAdmin()
      distributorKey: Lockr.get('currentDistributorKey')
      distributorName: Lockr.get('currentDistributorName')
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
