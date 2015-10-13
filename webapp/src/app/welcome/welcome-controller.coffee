'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "WelcomeCtrl", ($cookies) ->
  @identity = {}

  @initialize = ->
    @identity = {
      key:  $cookies.get('userKey')
      email:  $cookies.get('userEmail')
      distributorKey: $cookies.get('currentDistributorKey')
      distributorName: $cookies.get('currentDistributorName')
    }

  @
