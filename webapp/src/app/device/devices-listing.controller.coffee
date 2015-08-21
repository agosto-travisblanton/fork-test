'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DevicesListingCtrl', ($stateParams, DevicesService, $state) ->
  @devices = []

  devicesPromise = DevicesService.getDevices()
  devicesPromise.then (data) =>
    @devices = data

  initialize: ->

  @editItem = (item) ->
    $state.go 'editDevice', {deviceKey: item.key, tenantContext: ''}


  @
