'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'NavbarCtrl', ($cookies) ->
  @identity = {}

  @initialize = ->
    @identity.key = $cookies.get('userKey')
    @identity.email = $cookies.get('userEmail')
    @identity.distributor = $cookies.get('currentDistributorName')

  @
