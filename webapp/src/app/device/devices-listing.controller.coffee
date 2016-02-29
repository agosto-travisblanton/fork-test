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
    $state.go 'editDevice', {
      deviceKey: item.key,
      tenantKey: item.tenantKey,
      fromDevices: true}

  @
