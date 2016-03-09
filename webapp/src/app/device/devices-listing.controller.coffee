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

  @getManagedDevices = (key, prev, next) ->
    devicesPromise = DevicesService.getDevicesByDistributor key, prev, next
    devicesPromise.then ((response) =>
      console.log(response)
      @devices = response.devices
      @devicesNext = response.next_cursor
      @devicesPrev = response.prev_cursor
      console.log(@devicesNext)
      console.log(@devicesPrev)
      @getFetchSuccess(response)
    ), (response) =>
      @getFetchFailure(response)


  @getUnmanagedDevices = (key, prev, next) ->
    unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByDistributor key, prev, next
    unmanagedDevicesPromise.then (response) =>
      @unmanagedDevices = response.devices
      @unmanagedDevicesPrev = response.prev_cursor
      @unmanagedDevicesNext = response.next_cursor
      console.log(@unmanagedDevicesPrev)
      console.log(@unmanagedDevicesNext)

  @getManagedAndUnmanagedDevices = () ->
    @distributorKey = $cookies.get('currentDistributorKey')
    ProgressBarService.start()
    @getManagedDevices(@distributorKey, @devicesPrev, @devicesNext)
    @getUnmanagedDevices(@distributorKey, @unmanagedDevicesPrev, @unmanagedDevicesNext)


  @initialize = () ->
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
        console.log("going forward")
        console.log("going unmanaged")
        console.log("cursor is", cursor)

    if not forward
      if managed
        @getManagedDevices @distributorKey, @devicesPrev, null

      if not managed
        console.log("goign back")
  @
