'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DevicesListingCtrl', ($stateParams, $log, DevicesService, $state, SessionsService, ProgressBarService, sweet) ->
  vm = @
  vm.distributorKey = undefined
  #####################################
  # Managed
  #####################################
  vm.devices = []
  vm.devicesPrev = null
  vm.devicesNext = null
  vm.selectedButton = "Serial Number"
  vm.serialDevices = {}
  vm.disabled = true
  vm.macDevices = {}

  #####################################
  # Unmanaged
  #####################################
  vm.unmanagedSelectedButton = "MAC"
  vm.unmanagedSerialDevices = {}
  vm.unmanagedDisabled = true
  vm.unmanagedDevicesPrev = null
  vm.unmanagedDevicesNext = null
  vm.unmanagedDevices = []
  vm.unmanagedMacDevices = {}

  vm.refreshManagedDevices = () ->
    vm.devicesPrev = null
    vm.devicesNext = null
    DevicesService.deviceCache.removeAll()
    vm.getManagedDevices(vm.distributorKey, vm.devicesPrev, vm.devicesNext)

  vm.refreshUnmanagedDevices = () ->
    vm.unmanagedDevicesPrev = null
    vm.unmanagedDevicesNext = null
    DevicesService.deviceCache.removeAll()
    vm.getUnmanagedDevices(vm.distributorKey, vm.unmanagedDevicesPrev, vm.unmanagedDevicesNext)

  vm.changeRadio = (unmanaged) ->
    if unmanaged
      vm.unmanagedSearchText = ''
      vm.unmanagedDisabled = true
      vm.unmanagedSerialDevices = {}
      vm.unmanagedMacDevices = {}

    else
      vm.searchText = ''
      vm.disabled = true
      vm.serialDevices = {}
      vm.macDevices = {}

  vm.convertArrayToDictionary = (theArray, mac) ->
    devices = {}
    for item in theArray
      if mac
        devices[item.mac] = item
      else
        devices[item.serial] = item

    return devices

  vm.prepareForEditView = (unmanaged, searchText) ->
    if unmanaged
      mac = vm.unmanagedSelectedButton == "MAC"
      if mac
        vm.editItem vm.unmanagedMacDevices[searchText]
      else
        vm.editItem vm.unmanagedSerialDevices[searchText]

    else
      mac = vm.selectedButton == "MAC"
      if mac
        vm.editItem vm.macDevices[searchText]
      else
        vm.editItem vm.serialDevices[searchText]


  vm.controlOpenButton = (unmanaged, isMatch) ->
    if not unmanaged
      vm.disabled = !isMatch
      vm.disabledButtonLoading = false

    else
      vm.unmanagedDisabled = !isMatch
      vm.unmanagedDisabledButtonLoading = false

  vm.isResourceValid = (unmanaged, resource) ->
    if resource
      if resource.length > 2
        if unmanaged
          mac = vm.unmanagedSelectedButton == "MAC"
          vm.unmanagedDisabledButtonLoading = true

        else
          mac = vm.selectedButton == "MAC"
          vm.disabledButtonLoading = true

        if mac
          DevicesService.matchDevicesByFullMac(vm.distributorKey, resource, unmanaged)
          .then (res) ->
            vm.controlOpenButton(unmanaged, res["is_match"])

        else
          DevicesService.matchDevicesByFullSerial(vm.distributorKey, resource, unmanaged)
          .then (res) ->
            vm.controlOpenButton(unmanaged, res["is_match"])

      else
        vm.controlOpenButton(unmanaged, false)

    else
      vm.controlOpenButton(unmanaged, false)


  vm.searchDevices = (unmanaged, partial) ->
    if partial
      if partial.length > 2
        if unmanaged then button = vm.unmanagedSelectedButton else button = vm.selectedButton

        if button == "Serial Number"
          DevicesService.searchDevicesByPartialSerial(vm.distributorKey, partial, unmanaged)
          .then (res) ->
            result = res["serial_number_matches"]
            if unmanaged
              vm.unmanagedSerialDevices = vm.convertArrayToDictionary(result, false)
            else
              vm.serialDevices = vm.convertArrayToDictionary(result, false)
              
            serialsOfMatchedDevices = []
            for each in result
              serialsOfMatchedDevices.push each.serial
              
            return serialsOfMatchedDevices

        else
          DevicesService.searchDevicesByPartialMac(vm.distributorKey, partial, unmanaged)
          .then (res) ->
            result = res["mac_matches"]

            if unmanaged
              vm.unmanagedMacDevices = vm.convertArrayToDictionary(result, true)
            else
              vm.macDevices = vm.convertArrayToDictionary(result, true)

            macMatchesMacAddresses = []
            for each in result
              macMatchesMacAddresses.push each.mac

            return macMatchesMacAddresses

      else
        return []
    else
      return []


  vm.getManagedDevices = (key, prev, next) ->
    ProgressBarService.start()
    devicesPromise = DevicesService.getDevicesByDistributor key, prev, next
    devicesPromise.then ((response) ->
      vm.devices = response.devices
      vm.devicesNext = response.next_cursor
      vm.devicesPrev = response.prev_cursor
      vm.getFetchSuccess()
    ), (response) ->
      vm.getFetchFailure(response)


  vm.getUnmanagedDevices = (key, prev, next) ->
    ProgressBarService.start()
    unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByDistributor key, prev, next
    unmanagedDevicesPromise.then ((response) ->
      vm.unmanagedDevices = response.devices
      vm.unmanagedDevicesPrev = response.prev_cursor
      vm.unmanagedDevicesNext = response.next_cursor
      vm.getFetchSuccess()
    ), (response) ->
      vm.getFetchFailure(response)

  vm.initialize = () ->
    vm.distributorKey = SessionsService.getCurrentDistributorKey()
    vm.getManagedDevices(vm.distributorKey, vm.devicesPrev, vm.devicesNext)
    vm.getUnmanagedDevices(vm.distributorKey, vm.unmanagedDevicesPrev, vm.unmanagedDevicesNext)

  vm.getFetchSuccess = () ->
    ProgressBarService.complete()

  vm.getFetchFailure = (response) ->
    ProgressBarService.complete()
    errorMessage = "Unable to fetch devices. Error: #{response.status} #{response.statusText}."
    sweet.show('Oops...', errorMessage, 'error')

  vm.editItem = (item) ->
    $state.go 'editDevice', {
      deviceKey: item.key,
      tenantKey: item.tenantKey,
      fromDevices: true
    }

  vm.paginateCall = (forward, managed) ->
    if forward
      if managed
        vm.getManagedDevices vm.distributorKey, null, vm.devicesNext

      if not managed
        vm.getUnmanagedDevices vm.distributorKey, null, vm.unmanagedDevicesNext

    if not forward
      if managed
        vm.getManagedDevices vm.distributorKey, vm.devicesPrev, null

      if not managed
        vm.getUnmanagedDevices vm.distributorKey, vm.unmanagedDevicesPrev, null

  vm
