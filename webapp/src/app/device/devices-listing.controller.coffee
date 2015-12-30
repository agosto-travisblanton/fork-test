'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state, $cookies) ->
  @devices = []
  @distributorKey = undefined

  @initialize = ->
    @distributorKey = $cookies.get('currentDistributorKey')
    devicesPromise = DevicesService.getDevicesByDistributor @distributorKey
    devicesPromise.then (data) =>
      @devices = data

  @editItem = (item) ->
    $state.go 'editDevice', {deviceKey: item.key, tenantKey: ''}

  @
