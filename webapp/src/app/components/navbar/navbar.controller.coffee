'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'NavbarCtrl', ($log,
                                    $stateParams,
                                    $state,
                                    SessionsService, IdentityService) ->

  @identity = {
    distributor: undefined
    email: undefined
  }

  identityPromise = IdentityService.getIdentity()
  identityPromise.then (data) =>
    if data['is_logged_in']
      @identity = data
      @identity.key = 'foo'
  debugger

@
