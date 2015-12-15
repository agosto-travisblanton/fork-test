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
    panelModel: undefined
    panelInput: undefined
    status: undefined #"ACTIVE"
    tenantKey: undefined
    created: undefined #"2015-07-07 19:22:57"
    updated: undefined #"2015-07-07 19:22:57"
    volume: undefined
    custom: undefined
  }
  @editMode = !!$stateParams.deviceKey
  @issues = []

  @initialize = () ->
    @panelModels = DevicesService.getPanelModels()
    @panelInputs = DevicesService.getPanelInputs()
    tenantsPromise = TenantsService.fetchAllTenants()
    tenantsPromise.then (data) =>
      @tenants = data

    if @editMode
      devicePromise = DevicesService.getDeviceByKey($stateParams.deviceKey)
      devicePromise.then (data) =>
        @currentDevice = data
        @setSelectedOptions()
      issuesPromise = DevicesService.getIssuesByKey($stateParams.deviceKey)
      issuesPromise.then (data) =>
        @issues = data

  @setSelectedOptions = () ->
    if @currentDevice.panelModel == null
      @currentDevice.panelModel = @panelModels[0]
      @currentDevice.panelInput = @panelInputs[0]
    else
      for panelModel in @panelModels
        if panelModel.id is @currentDevice.panelModel
          @currentDevice.panelModel = panelModel
      for panelInput in @panelInputs
        if panelInput.id is @currentDevice.panelInput
          @currentDevice.panelInput = panelInput

  @onClickSaveButton = () ->
    ProgressBarService.start()
    if @currentDevice.panelModel != null
      @currentDevice.panelModel = if @currentDevice.panelModel.id == 'None' then null else @currentDevice.panelModel.id
    if @currentDevice.panelInput != null
      @currentDevice.panelInput = if @currentDevice.panelInput.id == '0' then null else @currentDevice.panelInput.id
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
    sweet.show('Success!', 'Sent a reset command to the device.', 'success')

  @onResetFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Reset error: #{error.data}", 'error')

  @onClickVolumeSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.volume $stateParams.deviceKey, @currentDevice.volume
      promise.then @onVolumeSuccess(@currentDevice.volume), @onVolumeFailure

  @onVolumeSuccess = (level) ->
    ProgressBarService.complete()
    sweet.show('Success!', "Sent a volume level of #{level} to the device.", 'success')

  @onVolumeFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Volume error: #{error.data}", 'error')

  @onClickCommandSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.custom $stateParams.deviceKey, @currentDevice.custom
      promise.then @onCommandSuccess(@currentDevice.custom), @onCommandFailure

  @onCommandSuccess = (command) ->
    ProgressBarService.complete()
    sweet.show('Success!', "Sent '#{command}' to the device.", 'success')

  @onCommandFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Command error: #{error.data}", 'error')

  @
