'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state, $cookies, ProgressBarService, sweet) ->
  @distributorKey = undefined

  # Managed
  @devices = []
  @devicesPrev = null
  @devicesNext = null
  @selectedButton = "Serial Number"
  @validSerials = []
  @serialDevices = {}
  @disabled = true
  @macDevices = {}
  @validMacs = []

  # Unmanaged
  @unmanagedSelectedButton = "MAC"
  @unmanagedValidSerials = []
  @unmanagedSerialDevices = {}
  @unmanagedDisabled = true
  @unmanagedDevicesPrev = null
  @unmanagedDevicesNext = null
  @unmanagedDevices = []
  @unmanagedMacDevices = {}
  @unmanagedValidMacs = []

  @changeRadio = (unmanaged) ->
    if unmanaged
      @unmanagedSearchText = ''
      @unmanagedDisabled = true

      @unmanagedValidSerials = []
      @unmanagedSerialDevices = {}

      @unmanagedMacDevices = {}
      @unmanagedValidMacs = []

    else
      @searchText = ''
      @disabled = true

      @serialDevices = {}
      @validSerials = []

      @macDevices = {}
      @validMacs = []

  @convertArrayToDictionary = (theArray, mac) ->
    Devices = {}
    for item in theArray
      if mac
        Devices[item.mac] = item
      else
        Devices[item.serial] = item

    return Devices

  @prepareForEditView = (unmanaged, searchText) ->
    if unmanaged
      mac = @unmanagedSelectedButton == "MAC"
      if mac
        @editItem @unmanagedMacDevices[searchText]
      else
        @editItem @unmanagedSerialDevices[searchText]

    else
      mac = @selectedButton == "MAC"
      if mac
        @editItem @macDevices[searchText]
      else
        @editItem @serialDevices[searchText]

  @isResourceValid = (unmanaged, resource) ->
    if unmanaged
      mac = @unmanagedSelectedButton == "MAC"

    else
      mac = @selectedButton == "MAC"


    if not unmanaged and not mac
      the_type = @validSerials

    if unmanaged and not mac
      the_type = @unmanagedValidSerials

    if not unmanaged and mac
      the_type = @validMacs

    if unmanaged and mac
      the_type = @unmanagedValidMacs

    if not unmanaged
      if resource in the_type
        @disabled = false

      else
        @disabled = true

    else
      if resource in the_type
        @unmanagedDisabled = false

      else
        @unmanagedDisabled = true


  @searchDevices = (unmanaged, partial) =>
    if unmanaged
      if partial
        if @unmanagedSelectedButton == "Serial Number"
          DevicesService.searchDevicesByPartialSerial(@distributorKey, partial, unmanaged)
          .then (res) =>
            result = res["serial_number_matches"]

            @unmanagedSerialDevices = @convertArrayToDictionary(result, false)
            @unmanagedValidSerials = [each.serial for each in result][0]
        else
          DevicesService.searchDevicesByPartialMac(@distributorKey, partial, unmanaged)
          .then (res) =>
            result = res["mac_matches"]

            @unmanagedMacDevices = @convertArrayToDictionary(result, true)
            @unmanagedValidMacs = [each.mac for each in result][0]

    else
      if partial
        if @selectedButton == "Serial Number"
          DevicesService.searchDevicesByPartialSerial(@distributorKey, partial, unmanaged)
          .then (res) =>
            result = res["serial_number_matches"]

            @serialDevices = @convertArrayToDictionary(result, false)
            @validSerials = [each.serial for each in result][0]

        else
          DevicesService.searchDevicesByPartialMac(@distributorKey, partial, unmanaged)
          .then (res) =>
            result = res["mac_matches"]

            @macDevices = @convertArrayToDictionary(result, true)
            @validMacs = [each.mac for each in result][0]


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
