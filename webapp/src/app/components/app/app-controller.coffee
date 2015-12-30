'use strict;'

app = angular.module 'skykitProvisioning'

app.controller 'AppController', ($mdSidenav, $state) ->
  vm = @

  vm.toggleSidenav = ->
    $mdSidenav('left').toggle()

  vm.goTo = (stateName, id) ->
    $state.go stateName, {id: id}
    $mdSidenav('left').close() if $mdSidenav('left').isOpen()

  vm
