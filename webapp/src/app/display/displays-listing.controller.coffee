'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DisplaysListingCtrl', ($stateParams, DevicesService) ->

  @displays = []

  displaysPromise = DevicesService.getDevices()
  displaysPromise.then (data) =>
    @displays = data

  initialize: ->


  @
