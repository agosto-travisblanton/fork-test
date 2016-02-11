'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller 'AppController', ($mdSidenav, $state, $cookies) ->
  vm = @

  vm.identity = {}

  vm.initialize = ->
    vm.identity = {
      key:  $cookies.get('userKey')
      email:  $cookies.get('userEmail')
      distributorKey: $cookies.get('currentDistributorKey')
      distributorName: $cookies.get('currentDistributorName')
    }

  vm.toggleSidenav = ->
    $mdSidenav('left').toggle()

  vm.goTo = (stateName, id) ->
    $state.go stateName, {id: id}
    $mdSidenav('left').close() if $mdSidenav('left').isOpen()

  vm
