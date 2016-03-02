'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'DeviceDetailsCtrl', ($log,
  $stateParams,
  $state,
  DevicesService,
  LocationsService,
  CommandsService,
  sweet,
  ProgressBarService) ->
  @tenantKey = $stateParams.tenantKey
  @deviceKey = $stateParams.deviceKey
  @fromDevices = $stateParams.fromDevices is "true"
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
    proofOfPlayLogging: false
    location: undefined
    heartbeatInterval: undefined
    checkContentInterval: undefined
  }
  @commandEvents = []
  @dayRange = 30
  @editMode = !!$stateParams.deviceKey
  @issues = []
  @pickerOptions = "{widgetPositioning: {vertical:'bottom'}, showTodayButton: true, sideBySide: true, icons:{
      next:'glyphicon glyphicon-arrow-right',
      previous:'glyphicon glyphicon-arrow-left',
      up:'glyphicon glyphicon-arrow-up',
      down:'glyphicon glyphicon-arrow-down'}}"

  @initialize = () ->
    @panelModels = DevicesService.getPanelModels()
    @panelInputs = DevicesService.getPanelInputs()
    if @editMode
      devicePromise = DevicesService.getDeviceByKey @deviceKey
      devicePromise.then ((response) =>
        @onGetDeviceSuccess(response)
        return
      ), (response) =>
        @onGetDeviceFailure(response)
        return
      commandEventsPromise = DevicesService.getCommandEventsByKey @deviceKey
      commandEventsPromise.then (data) =>
        @commandEvents = data
      now = new Date()
      today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      @endTime = now.toLocaleString().replace(/,/g, "")
      today.setDate(now.getDate() - @dayRange)
      @startTime = today.toLocaleString().replace(/,/g, "")
      @epochStart = moment(new Date(@startTime)).unix()
      @epochEnd = moment(new Date(@endTime)).unix()
      issuesPromise = DevicesService.getIssuesByKey(@deviceKey, @epochStart, @epochEnd)
      issuesPromise.then (data) =>
        @issues = data

  @onGetDeviceSuccess = (response) ->
    @currentDevice = response
    @tenantKey = @currentDevice.tenantKey if @tenantKey is undefined
    if $stateParams.fromDevices is "true"
      @backUrl = '/#/devices'
      @backUrlText = 'Back to devices'
    else
      if @currentDevice.isUnmanagedDevice is true
        @backUrl = "/#/tenants/#{@tenantKey}/unmanaged"
        @backUrlText = 'Back to tenant unmanaged devices'
      else
        @backUrl = "/#/tenants/#{@tenantKey}/managed"
        @backUrlText = 'Back to tenant managed devices'
    locationsPromise = LocationsService.getLocationsByTenantKey @tenantKey
    locationsPromise.then (data) =>
      @locations = data
      @setSelectedOptions()

  @onGetDeviceFailure = (response) ->
    errorMessage = "No detail for key ##{@deviceKey}.\nError: #{response.status} #{response.statusText}"
    sweet.show('Oops...', errorMessage, 'error')

  @setSelectedOptions = () ->
    if @currentDevice.panelModel == null
      @currentDevice.panelModel = @panelModels[0]
      @currentDevice.panelInput = @panelInputs[0]
    else
      for panelModel in @panelModels
        if panelModel.id is @currentDevice.panelModel
          @currentDevice.panelModel = panelModel
      for panelInput in @panelInputs
        isParent = panelInput.parentId is @currentDevice.panelModel.id
        if isParent and panelInput.id.toLowerCase() is @currentDevice.panelInput
          @currentDevice.panelInput = panelInput
    if @currentDevice.locationKey != null
      for location in @locations
        if location.key is @currentDevice.locationKey
          @currentDevice.location = location

  @onClickSavePanels = () ->
    ProgressBarService.start()
    promise = DevicesService.save @currentDevice
    promise.then @onSuccessDeviceSave, @onFailureDeviceSavePanels

  @onClickSaveIntervals = () ->
    ProgressBarService.start()
    @setPanelInfo()
    promise = DevicesService.save @currentDevice
    promise.then @onSuccessDeviceSave, @onFailureDeviceSaveIntervals

  @onClickSaveLocation = () ->
    ProgressBarService.start()
    @currentDevice.locationKey = @currentDevice.location.key
    @setPanelInfo()
    promise = DevicesService.save @currentDevice
    promise.then @onSuccessDeviceSave, @onFailureDeviceSaveLocation

  @onSuccessDeviceSave = ->
    ProgressBarService.complete()
    $state.go 'devices'

  @onFailureDeviceSavePanels = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save the serial control information.', 'error')

  @onFailureDeviceSaveIntervals = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save intervals information.', 'error')

  @onFailureDeviceSaveLocation = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save the location information.', 'error')

  @onClickSaveDevice = () ->
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
      promise = CommandsService.reset @deviceKey
      promise.then @onResetSuccess, @onResetFailure

  @onResetSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent a reset command to Google Cloud Messaging.', 'success')

  @onResetFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Reset error: #{error.data}", 'error')

  @onClickContentDeleteSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.contentDelete @deviceKey
      promise.then @onContentDeleteSuccess, @onContentDeleteFailure

  @onContentDeleteSuccess = () ->
    ProgressBarService.complete()
    sweet.show('Success!', 'Sent a content delete command to Google Cloud Messaging.', 'success')

  @onContentDeleteFailure = (error) ->
    ProgressBarService.complete()
    sweet.show('Oops...', "Content delete error: #{error.data}", 'error')

  @onClickVolumeSendButton = () ->
    if @editMode
      ProgressBarService.start()
      promise = CommandsService.volume @deviceKey, @currentDevice.volume
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
      promise = CommandsService.custom @deviceKey, @currentDevice.custom
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
    issuesPromise = DevicesService.getIssuesByKey(@deviceKey, @epochStart, @epochEnd)
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
      promise = CommandsService.powerOn @deviceKey
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
      promise = CommandsService.powerOff @deviceKey
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
      @currentDevice.panelInput = if @currentDevice.panelInput.id == 'None' then null else @currentDevice.panelInput.id.toLowerCase()

  @autoGenerateCustomerDisplayCode = ->
    newDisplayCode = ''
    if @currentDevice.customerDisplayName
      newDisplayCode = @currentDevice.customerDisplayName.toLowerCase()
      newDisplayCode = newDisplayCode.replace(/\s+/g, '_')
      newDisplayCode = newDisplayCode.replace(/\W+/g, '')
    @currentDevice.customerDisplayCode = newDisplayCode

  @
