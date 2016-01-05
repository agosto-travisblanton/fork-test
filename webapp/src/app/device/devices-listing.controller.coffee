'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state, $cookies, $mdDialog) ->
  @devices = []
  @unmanagedDevices = []
  @distributorKey = undefined

  @initialize = ->
    @distributorKey = $cookies.get('currentDistributorKey')
    devicesPromise = DevicesService.getDevicesByDistributor @distributorKey
    devicesPromise.then (data) =>
      @devices = data
    unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByDistributor @distributorKey
    unmanagedDevicesPromise.then (data) =>
      @unmanagedDevices = data

  @editItem = (item) ->
    $state.go 'editDevice', {deviceKey: item.key, tenantKey: ''}

  @showDeviceDetails = (item, event) ->
    apiKey = item.apiKey
    $mdDialog.show($mdDialog.alert()
    .title('Device Details')
    .textContent("API key: #{apiKey}")
    .ariaLabel('Device details')
    .ok('Close')
    .targetEvent(event))

  @
