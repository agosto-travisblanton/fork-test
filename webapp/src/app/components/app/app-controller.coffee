'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller 'AppController', ($mdSidenav, $state, $cookies) ->
  vm = @

  vm.identity = {}

  @getIdentity = () ->
    vm.identity = {
      key: $cookies.get('userKey')
      email: $cookies.get('userEmail')
      distributorKey: $cookies.get('currentDistributorKey')
      distributorName: $cookies.get('currentDistributorName')
    }
    return vm.identity

  vm.initialize = ->
    @getIdentity()

  vm.toggleSidenav = ->
    $mdSidenav('left').toggle()

  vm.goTo = (stateName, id) ->
    $state.go stateName, {id: id}
    $mdSidenav('left').close() if $mdSidenav('left').isOpen()

  vm
