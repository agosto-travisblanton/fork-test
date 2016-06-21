'use strict'
appModule = angular.module('skykitProvisioning')
appModule.controller 'DeviceDetailsCtrl', (
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

    vm.copyDeviceKey = () ->
      ToastsService.showSuccessToast 'Device key has been copied to your clipboard'

    vm.initialize = () ->
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

    vm.onGetDeviceFailure = (response) ->
      ToastsService.showErrorToast 'Oops. We were unable to fetch the details for this device at this time.'
      errorMessage = "No detail for device_key ##{vm.deviceKey}. Error: #{response.status} #{response.statusText}"
      $log.error errorMessage
      $state.go 'devices'

    vm
