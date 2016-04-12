'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state, $cookies, ProgressBarService, sweet) ->
  @distributorKey = undefined

  #####################################
  # Managed
  #####################################
  @devices = []
  @devicesPrev = null
  @devicesNext = null
  @selectedButton = "Serial Number"
  @serialDevices = {}
  @disabled = true
  @macDevices = {}

  #####################################
  # Unmanaged
  #####################################
  @unmanagedSelectedButton = "MAC"
  @unmanagedSerialDevices = {}
  @unmanagedDisabled = true
  @unmanagedDevicesPrev = null
  @unmanagedDevicesNext = null
  @unmanagedDevices = []
  @unmanagedMacDevices = {}

  @changeRadio = (unmanaged) ->
    if unmanaged
      @unmanagedSearchText = ''
      @unmanagedDisabled = true
      @unmanagedSerialDevices = {}
      @unmanagedMacDevices = {}

    else
      @searchText = ''
      @disabled = true
      @serialDevices = {}
      @macDevices = {}

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


  @controlOpenButton = (unmanaged, isMatch) =>
    if not unmanaged
      @disabled = !isMatch

    else
      @unmanagedDisabled = !isMatch

  @isResourceValid = (unmanaged, resource) ->
    if resource
      if resource.length > 2
        if unmanaged then mac = @unmanagedSelectedButton == "MAC" else mac = @selectedButton == "MAC"

        if mac
          DevicesService.matchDevicesByFullMac(@distributorKey, resource, unmanaged)
          .then (res) =>
            @controlOpenButton(unmanaged, res["is_match"])

        else
          DevicesService.matchDevicesByFullSerial(@distributorKey, resource, unmanaged)
          .then (res) =>
            @controlOpenButton(unmanaged, res["is_match"])

      else
        @controlOpenButton(unmanaged, false)

    else
      @controlOpenButton(unmanaged, false)


  @searchDevices = (unmanaged, partial) =>
    if partial
      if partial.length > 2
        if unmanaged then button = @unmanagedSelectedButton else button = @selectedButton

        if button == "Serial Number"
          DevicesService.searchDevicesByPartialSerial(@distributorKey, partial, unmanaged)
          .then (res) =>
            result = res["serial_number_matches"]

            if unmanaged
              @unmanagedSerialDevices = @convertArrayToDictionary(result, false)
            else
              @serialDevices = @convertArrayToDictionary(result, false)

            return [each.serial for each in result][0]

        else
          DevicesService.searchDevicesByPartialMac(@distributorKey, partial, unmanaged)
          .then (res) =>
            result = res["mac_matches"]

            if unmanaged
              @unmanagedMacDevices = @convertArrayToDictionary(result, true)
            else
              @macDevices = @convertArrayToDictionary(result, true)

            return [each.mac for each in result][0]


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

  @initialize = () ->
    @distributorKey = $cookies.get('currentDistributorKey')
    @getManagedDevices(@distributorKey, @devicesPrev, @devicesNext)
    @getUnmanagedDevices(@distributorKey, @unmanagedDevicesPrev, @unmanagedDevicesNext)

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
