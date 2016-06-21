'use strict'
appModule = angular.module('skykitProvisioning')
appModule.controller 'DeviceDetailsPropertiesCtrl', (
  $log,
  $stateParams,
  $state,
  SessionsService,
  DevicesService,
  LocationsService,
  CommandsService,
  TimezonesService,
  sweet,
  ProgressBarService,
  $mdDialog,
  ToastsService) ->
    vm = @
    vm.tenantKey = $stateParams.tenantKey
    vm.deviceKey = $stateParams.deviceKey
    vm.fromDevices = $stateParams.fromDevices is "true"
    vm.currentDevice = {}

    vm.initialize = () ->
      vm.panelModels = DevicesService.getPanelModels()
      vm.panelInputs = DevicesService.getPanelInputs()
      timezonePromise = TimezonesService.getCustomTimezones()
      timezonePromise.then (data) ->
        vm.timezones = data

      devicePromise = DevicesService.getDeviceByKey vm.deviceKey
      devicePromise.then ((response) ->
        vm.onGetDeviceSuccess(response)
      ), (response) ->
        vm.onGetDeviceFailure(response)

    vm.onGetDeviceSuccess = (response) ->
      vm.currentDevice = response
      vm.selectedTimezone = response.timezone if response.timezone != vm.selectedTimezone
      vm.tenantKey = vm.currentDevice.tenantKey if vm.tenantKey is undefined
      if $stateParams.fromDevices is "true"
        vm.backUrl = '/#/devices'
        vm.backUrlText = 'Back to devices'
      else
        if vm.currentDevice.isUnmanagedDevice is true
          vm.backUrl = "/#/tenants/#{vm.tenantKey}/unmanaged"
          vm.backUrlText = 'Back to tenant unmanaged devices'
        else
          vm.backUrl = "/#/tenants/#{vm.tenantKey}/managed"
          vm.backUrlText = 'Back to tenant managed devices'
      locationsPromise = LocationsService.getLocationsByTenantKey vm.tenantKey
      locationsPromise.then (data) ->
        vm.locations = data
        vm.setSelectedLocationOptions()

    vm.onGetDeviceFailure = (response) ->
      ToastsService.showErrorToast 'Oops. We were unable to fetch the details for this device at this time.'
      errorMessage = "No detail for device_key ##{vm.deviceKey}. Error: #{response.status} #{response.statusText}"
      $log.error errorMessage
      $state.go 'devices'

    vm.setSelectedLocationOptions = () ->
      if vm.currentDevice.panelModel == null
        vm.currentDevice.panelModel = vm.panelModels[0]
        vm.currentDevice.panelInput = vm.panelInputs[0]
      else
        for panelModel in vm.panelModels
          if panelModel.id is vm.currentDevice.panelModel
            vm.currentDevice.panelModel = panelModel
        for panelInput in vm.panelInputs
          isParent = panelInput.parentId is vm.currentDevice.panelModel.id
          if isParent and panelInput.id.toLowerCase() is vm.currentDevice.panelInput
            vm.currentDevice.panelInput = panelInput
      if vm.currentDevice.locationKey != null
        for location in vm.locations
          if location.key is vm.currentDevice.locationKey
            vm.currentDevice.location = location

    vm.copyDeviceKey = () ->
      ToastsService.showSuccessToast 'Device key has been copied to your clipboard'

    vm.onSaveDevice = () ->
      ProgressBarService.start()
      if vm.currentDevice.location != undefined && vm.currentDevice.location.key != undefined
        vm.currentDevice.locationKey = vm.currentDevice.location.key
      if vm.currentDevice.panelModel.id != undefined && vm.currentDevice.panelModel.id != 'None'
        vm.currentDevice.panelModelNumber = vm.currentDevice.panelModel.id
      if vm.currentDevice.panelInput.id != undefined && vm.currentDevice.panelInput.id != 'None'
        vm.currentDevice.panelSerialInput = vm.currentDevice.panelInput.id.toLowerCase()
      vm.currentDevice.timezone = vm.selectedTimezone
      promise = DevicesService.save vm.currentDevice
      promise.then vm.onSuccessDeviceSave, vm.onFailureDeviceSave

    vm.onSuccessDeviceSave = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast 'We saved your update.'

    vm.onFailureDeviceSave = (error) ->
      ProgressBarService.complete()
      if error.status == 409
        $log.info(
          "Failure saving device. Customer display code already exists for tenant: #{error.status } #{error.statusText}")
        sweet.show('Oops...', 'This customer display code already exists for this tenant. Please choose another.', 'error')
      else
        $log.error "Failure saving device: #{error.status } #{error.statusText}"
        ToastsService.showErrorToast 'Oops. We were unable to save your updates to this device at this time.'

    vm.confirmDeviceDelete = (event, key) ->
      confirm = $mdDialog.confirm(
        {
          title: 'Are you sure to delete this device?'
          textContent: 'Please remember, you MUST remove this device from Content Manager before deleting it from Provisioning.'
          targetEvent: event
          ok: 'Delete'
          cancel: 'Cancel'
        }
      )
      showPromise = $mdDialog.show confirm
      success = ->
        vm.onConfirmDelete key
      failure = ->
        vm.onConfirmCancel()
      showPromise.then success, failure

    vm.onConfirmDelete = (key) ->
      success = () ->
        ToastsService.showSuccessToast 'We processed your delete request.'
        $state.go 'devices'
      failure = (error) ->
        friendlyMessage = 'We were unable to complete your delete request at this time.'
        ToastsService.showErrorToast friendlyMessage
        $log.error "Delete device failure for device_key #{key}: #{error.status } #{error.statusText}"
      deletePromise = DevicesService.delete key
      deletePromise.then success, failure

    vm.onConfirmCancel = ->
      ToastsService.showInfoToast 'We canceled your delete request.'

    vm.onProofOfPlayLoggingCheck = ->
      if vm.currentDevice.proofOfPlayLogging
        noLocation = vm.currentDevice.locationKey == null
        noDisplayCode = vm.currentDevice.customerDisplayCode == null
        if noLocation
          sweet.show('Oops...', "You must have a Location to enable Proof of play.", 'error')
          vm.currentDevice.proofOfPlayLogging = false
        else if noDisplayCode
          sweet.show('Oops...', "You must have a Display code to enable Proof of play.", 'error')
          vm.currentDevice.proofOfPlayLogging = false
        else
          vm.onSaveDevice()
      else
        vm.onSaveDevice()

    vm.autoGenerateCustomerDisplayCode = ->
      newDisplayCode = ''
      if vm.currentDevice.customerDisplayName
        newDisplayCode = vm.currentDevice.customerDisplayName.toLowerCase()
        newDisplayCode = newDisplayCode.replace(/\s+/g, '_')
        newDisplayCode = newDisplayCode.replace(/\W+/g, '')
      vm.currentDevice.customerDisplayCode = newDisplayCode

    vm.logglyForUser = () ->
      userDomain = SessionsService.getUserEmail().split("@")[1]
      return userDomain == "demo.agosto.com" || userDomain == "agosto.com"

    vm
