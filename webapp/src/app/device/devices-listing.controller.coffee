'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state, $cookies, ProgressBarService,
  sweet) ->
  @devices = []
  @unmanagedDevices = []
  @distributorKey = undefined

  @initialize = () ->
    @distributorKey = $cookies.get('currentDistributorKey')
    unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByDistributor @distributorKey
    unmanagedDevicesPromise.then (response) =>
      @unmanagedDevices = response
    ProgressBarService.start()
    devicesPromise = DevicesService.getDevicesByDistributor @distributorKey
    devicesPromise.then ((response) =>
      @getFetchSuccess(response)
      return
    ), (response) =>
      @getFetchFailure(response)
      return

  @getFetchSuccess = (response) ->
    @devices = response
    ProgressBarService.complete()

  @getFetchFailure = (response) ->
    ProgressBarService.complete()
    errorMessage = "Unable to fetch devices. Error: #{response.status} #{response.statusText}."
    sweet.show('Oops...', errorMessage, 'error')

  @editItem = (item) ->
    $state.go 'editDevice', {
      deviceKey: item.key,
      tenantKey: item.tenantKey,
      fromDevices: true
    }

  @
