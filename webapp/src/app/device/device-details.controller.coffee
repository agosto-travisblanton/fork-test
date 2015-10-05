'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DeviceDetailsCtrl', ($log,
                                           $stateParams,
                                           $state,
                                           DevicesService,
                                           TenantsService,
                                           CommandsService,
                                           sweet,
                                           ProgressBarService) ->
  @tenantKey = $stateParams.tenantKey

  @currentDevice = {
    key: undefined
    gcmRegistrationId: undefined
    annotatedLocation: undefined
    annotatedUser: undefined
    apiKey: undefined
    deviceId: undefined #"41b0f043-4296-4c56-b21a-c8bd660ea9ca"
    bootMode: undefined
    chromeDeviceDomain: undefined
    contentServerUrl: undefined
    etag: undefined
    ethernetMacAddress: undefined #"3863bb98f982"
    macAddress: undefined #"38b1db95ac21"
    firmwareVersion: undefined #""
    kind: undefined #"admin#directory#chromeosdevice"
    lastEnrollmentTime: undefined #"2015-05-06T20:01:31.459Z"
    lastSync: undefined #"2015-07-07T17:38:14.274Z"
    model: undefined #"HP Chromebox CB1-(000-099) / HP Chromebox G1"
    orgUnitPath: undefined #"/Beta/Fairchild Semi"
    osVersion: undefined #"42.0.2311.153"
    platformVersion: undefined #"6812.88.0 (Official Build) stable-channel zako"
    serialNumber: undefined #"5CD45183T6"
    status: undefined #"ACTIVE"
    tenantKey: undefined
    created: undefined #"2015-07-07 19:22:57"
    updated: undefined #"2015-07-07 19:22:57"
    volume: undefined
    custom: undefined
  }
  @editMode = !!$stateParams.deviceKey

  tenantsPromise = TenantsService.fetchAllTenants()
  tenantsPromise.then (data) =>
    @tenants = data


  if @editMode
    devicePromise = DevicesService.getDeviceByKey($stateParams.deviceKey)
    devicePromise.then (data) =>
      @currentDevice = data

  @onClickSaveButton = () ->
    ProgressBarService.start()
    promise = DevicesService.save @currentDevice
    promise.then @onSuccessDeviceSave, @onFailureDeviceSave

  @onSuccessDeviceSave = ->
    ProgressBarService.complete()
    $state.go 'devices'

  @onFailureDeviceSave = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save the device.', 'error')

  @onClickResetSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.reset $stateParams.deviceKey
      promise.then @onResetSuccess, @onResetFailure

  @onResetSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent reset command to the device.', 'success')

  @onResetFailure = () ->
    ProgressBarService.complete()
    sweet.show('Oops...', 'Unable to send reset command to the device.', 'error')

  @onClickVolumeSendButton = () ->
    if @editMode
      volume = @currentDevice.volume
      debugger
      ProgressBarService.start()
      promise = CommandsService.volume $stateParams.deviceKey, volume
      promise.then @onVolumeSuccess, @onVolumeFailure

  @onVolumeSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent volume command to the device.', 'success')

  @onVolumeFailure = () ->
    ProgressBarService.complete()
    sweet.show('Oops...', 'Unable to send volume command to the device.', 'error')

  @onClickCommandSendButton = () ->
    if @editMode
      custom_command = @currentDevice.custom
      debugger
      ProgressBarService.start()
      promise = CommandsService.custom $stateParams.deviceKey, custom_command
      promise.then @onCommandSuccess, @onCommandFailure

  @onCommandSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent custom command to the device.', 'success')

  @onCommandFailure = () ->
    ProgressBarService.complete()
    message = ""
    sweet.show('Oops...', 'Unable to send custom command to the device.', 'error')

  @
