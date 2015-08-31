'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state) ->
  @devices = []

  @initialize = ->
    devicesPromise = DevicesService.getDevices()
    devicesPromise.then (data) =>
      @devices = data

  @editItem = (item) ->
    $state.go 'editDevice', {deviceKey: item.key, tenantKey: ''}

  @
