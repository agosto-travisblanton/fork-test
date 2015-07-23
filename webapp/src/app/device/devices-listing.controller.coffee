'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DevicesListingCtrl', ($stateParams, DevicesService) ->

  @devices = []

  devicesPromise = DevicesService.getDevices()
  devicesPromise.then (data) =>
    @devices = data

  initialize: ->


  @
