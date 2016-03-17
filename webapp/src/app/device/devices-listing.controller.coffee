'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state, $cookies, ProgressBarService, sweet) ->
  @devices = []
  @unmanagedDevices = []
  @distributorKey = undefined
  @devicesPrev = null
  @devicesNext = null
  @unmanagedDevicesPrev = null
  @unmanagedDevicesNext = null
  @selectedButton = "Serial Number"

  @searchDevices = (partial_serial) ->
    if partial_serial
      DevicesService.searchDevicesByPartialSerial(@distributorKey, partial_serial, false)
      .then (res) ->
        res["serial_number_matches"] or []


  @getManagedDevices = (key, prev, next) ->
    devicesPromise = DevicesService.getDevicesByDistributor key, prev, next
    ProgressBarService.start()
    devicesPromise.then ((response) =>
      @devices = response.devices
      @devicesNext = response.next_cursor
      @devicesPrev = response.prev_cursor
      @getFetchSuccess()
    ), (response) =>
      @getFetchFailure(response)


  @getUnmanagedDevices = (key, prev, next) ->
    unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByDistributor key, prev, next
    ProgressBarService.start()
    unmanagedDevicesPromise.then ((response) =>
      @unmanagedDevices = response.devices
      @unmanagedDevicesPrev = response.prev_cursor
      @unmanagedDevicesNext = response.next_cursor
      @getFetchSuccess()
    ), (response) =>
      @getFetchFailure(response)

  @getManagedAndUnmanagedDevices = () ->
    @getManagedDevices(@distributorKey, @devicesPrev, @devicesNext)
    @getUnmanagedDevices(@distributorKey, @unmanagedDevicesPrev, @unmanagedDevicesNext)


  @initialize = () ->
    @distributorKey = $cookies.get('currentDistributorKey')
    @getManagedAndUnmanagedDevices()

  @getFetchSuccess = () ->
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

  @paginateCall = (forward, managed) ->
    if forward
      if managed
        @getManagedDevices @distributorKey, null, @devicesNext

      if not managed
        @getUnmanagedDevices @distributorKey, null, @unmanagedDevicesNext

    if not forward
      if managed
        @getManagedDevices @distributorKey, @devicesPrev, null

      if not managed
        @getUnmanagedDevices @distributorKey, @unmanagedDevicesPrev, null
  @
