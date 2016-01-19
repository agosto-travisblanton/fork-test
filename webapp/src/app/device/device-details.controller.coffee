'use strict'

appModule = angular.module('skykitProvisioning')

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
  @commandEvents = []
  @editMode = !!$stateParams.deviceKey
  @issues = []
  @pickerOptions = "{icons:{next:'glyphicon glyphicon-arrow-right',
      previous:'glyphicon glyphicon-arrow-left',up:'glyphicon glyphicon-arrow-up',down:'glyphicon glyphicon-arrow-down'}}"

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
      commandEventsPromise = DevicesService.getCommandEventsByKey($stateParams.deviceKey)
      commandEventsPromise.then (data) =>
        @commandEvents = data
      now = new Date()
      today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      @endTime = now.toLocaleString().replace(/,/g, "")
      today.setDate(now.getDate() - 1)
      @startTime = today.toLocaleString().replace(/,/g, "")
      @epochStart = moment(new Date(@startTime)).unix()
      @epochEnd = moment(new Date(@endTime)).unix()
      issuesPromise = DevicesService.getIssuesByKey($stateParams.deviceKey, @epochStart, @epochEnd)
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

  @onClickSavePanels = () ->
    ProgressBarService.start()
    @setPanelInfo()
    promise = DevicesService.save @currentDevice
    promise.then @onSuccessDeviceSave, @onFailureDeviceSavePanels

  @onSuccessDeviceSave = ->
    ProgressBarService.complete()
    $state.go 'devices'

  @onFailureDeviceSavePanels = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save the serial control information.', 'error')

  @onClickSaveNotes = () ->
    ProgressBarService.start()
    @setPanelInfo()
    promise = DevicesService.save @currentDevice
    promise.then @onSuccessDeviceSave, @onFailureDeviceSaveNotes

  @onFailureDeviceSaveNotes = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save the device notes.', 'error')

  @onClickResetSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.reset $stateParams.deviceKey
      promise.then @onResetSuccess, @onResetFailure

  @onResetSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent a reset command to Google Cloud Messaging.', 'success')

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
    sweet.show('Success!', "Sent a volume level of #{level} to Google Cloud Messaging.", 'success')

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
    sweet.show('Success!', "Sent '#{command}' to Google Cloud Messaging.", 'success')

  @onCommandFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Command error: #{error.data}", 'error')

  @onClickRefreshButton = () ->
    ProgressBarService.start()
    @epochStart = moment(new Date(@startTime)).unix()
    @epochEnd = moment(new Date(@endTime)).unix()
    issuesPromise = DevicesService.getIssuesByKey($stateParams.deviceKey, @epochStart, @epochEnd)
    issuesPromise.then ((data) =>
      @onRefreshIssuesSuccess(data)
    ), (error) =>
      @onRefreshIssuesFailure(error)

  @onRefreshIssuesSuccess = (data) ->
    ProgressBarService.complete()
    @issues = data

  @onRefreshIssuesFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Refresh error: #{error.data}", 'error')

  @onClickPowerOnSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.powerOn $stateParams.deviceKey
      promise.then @onPowerOnSuccess, @onPowerOnFailure

  @onPowerOnSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent a power on command to Google Cloud Messaging.', 'success')

  @onPowerOnFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Power on error: #{error.data}", 'error')

  @onClickPowerOffSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.powerOff $stateParams.deviceKey
      promise.then @onPowerOffSuccess, @onPowerOffFailure

  @onPowerOffSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent a power off command to Google Cloud Messaging.', 'success')

  @onPowerOffFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Power off error: #{error.data}", 'error')

  @setPanelInfo = () ->
    if @currentDevice.panelModel != null
      @currentDevice.panelModel = if @currentDevice.panelModel.id == 'None' then null else @currentDevice.panelModel.id
    if @currentDevice.panelInput != null
      @currentDevice.panelInput = if @currentDevice.panelInput.id == '0' then null else @currentDevice.panelInput.id

  @
