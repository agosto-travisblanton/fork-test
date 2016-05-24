'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller 'AppController', ($mdSidenav, $state, $window, SessionsService) ->
  @identity = {}
  
  @currentDistributerInDistributerAdminList = () ->
  currentDistributorName = SessionsService.getCurrentDistributorName()
  distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()
  _.contains(distributorsAsAdmin, currentDistributorName)

  @getIdentity = () =>
    @identity = {
      key: SessionsService.getUserKey()
      email: SessionsService.getUserEmail()
      admin: SessionsService.getIsAdmin()
      distributor_admin: SessionsService.getDistributorsAsAdmin()
      admin_of_current_distributor: @currentDistributerInDistributerAdminList()
      distributorKey: SessionsService.getCurrentDistributorKey()
      distributorName: SessionsService.getCurrentDistributorName()
    }
    @identity  


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
