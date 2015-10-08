'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'NavbarCtrl', ($stateParams, $log, $cookies, IdentityService) ->
  @identity = {}

  @initialize = ->
    debugger
    @identity.key = $cookies.get('user_key')
    identityPromise = IdentityService.getIdentity()
    identityPromise.then (data) =>
      if data['is_logged_in']
        @identity.email = data['email']
        @identity.distributor = data['distributor']

  @
