'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller 'AppController', ($mdSidenav, $state, $window, SessionsService) ->
  @identity = {}

  @getIdentity = () =>
    @identity = {
      key: SessionsService.getUserKey()
      email: SessionsService.getUserEmail()
      admin: SessionsService.getIsAdmin()
      distributor_admin: SessionsService.getDistributorsAsAdmin()
      distributorKey: SessionsService.getCurrentDistributorKey()
      distributorName: SessionsService.getCurrentDistributorName()
    }

  @isCurrentURLDistributorSelector = () ->
    test = $window.location.href.search /distributor_selection/
    result = test >= 0

  @initialize = =>
    @getIdentity()

  @toggleSidenav = ->
    $mdSidenav('left').toggle()

  @goTo = (stateName, id) ->
    $state.go stateName, {id: id}
    $mdSidenav('left').close() if $mdSidenav('left').isOpen()

  @
