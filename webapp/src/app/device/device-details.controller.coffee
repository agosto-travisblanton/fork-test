'use strict'
appModule = angular.module('skykitProvisioning')
appModule.controller 'DeviceDetailsCtrl', ($log,
  $stateParams,
  $state,
  DevicesService,
  LocationsService,
  CommandsService,
  TimezonesService,
  sweet,
  $cookies,
  ProgressBarService,
  $mdDialog,
  ToastsService) ->
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
    panelModelNumber: undefined
    panelSerialInput: undefined
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
  @locations = []
  @commandEvents = []
  @dayRange = 30
  @issues = []
  @pickerOptions = "{widgetPositioning: {vertical:'bottom'}, showTodayButton: true, sideBySide: true, icons:{
      next:'glyphicon glyphicon-arrow-right',
      previous:'glyphicon glyphicon-arrow-left',
      up:'glyphicon glyphicon-arrow-up',
      down:'glyphicon glyphicon-arrow-down'}}"
  @timezones = []
  @selectedTimezone = undefined
  now = new Date()
  today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  @endTime = now.toLocaleString().replace(/,/g, "")
  today.setDate(now.getDate() - @dayRange)
  @startTime = today.toLocaleString().replace(/,/g, "")

  @getIssues = (device, epochStart, epochEnd, prev, next) =>
    ProgressBarService.start()
    issuesPromise = DevicesService.getIssuesByKey(device, epochStart, epochEnd, prev, next)
    issuesPromise.then (data) =>
      @issues = data.issues
      @prev_cursor = data.prev
      @next_cursor = data.next
      ProgressBarService.complete()

  @paginateCall = (forward) =>
    if forward
      @getIssues @deviceKey, @epochStart, @epochEnd, null, @next_cursor

    else
      @getIssues @deviceKey, @epochStart, @epochEnd, @prev_cursor, null


  @getEvents = (deviceKey, prev, next) =>
    commandEventsPromise = DevicesService.getCommandEventsByKey deviceKey, prev, next
    commandEventsPromise.then (data) =>
      @event_next_cursor = data.next_cursor
      @event_prev_cursor = data.prev_cursor
      @commandEvents = data.events

  @paginateEventCall = (forward) =>
    if forward
      @getEvents @deviceKey, null, @event_next_cursor

    else
      @getEvents @deviceKey, @event_prev_cursor, null

  @initialize = () ->
    @epochStart = moment(new Date(@startTime)).unix()
    @epochEnd = moment(new Date(@endTime)).unix()
    timezonePromise = TimezonesService.getUsTimezones()
    timezonePromise.then (data) =>
      @timezones = data

    @panelModels = DevicesService.getPanelModels()
    @panelInputs = DevicesService.getPanelInputs()

    devicePromise = DevicesService.getDeviceByKey @deviceKey
    devicePromise.then ((response) =>
      @onGetDeviceSuccess(response)
    ), (response) =>
      @onGetDeviceFailure(response)

    @getEvents @deviceKey
    @getIssues(@deviceKey, @epochStart, @epochEnd)

  @onGetDeviceSuccess = (response) ->
    @currentDevice = response
    @selectedTimezone = response.timezone if response.timezone != @selectedTimezone
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
    ToastsService.showErrorToast 'Oops. We were unable to fetch the details for this device at this time.'
    errorMessage = "No detail for device_key ##{@deviceKey}. Error: #{response.status} #{response.statusText}"
    $log.error errorMessage
    $state.go 'devices'

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

  #####################
  # Properties Tab
  #####################

  @onSaveDevice = () ->
    ProgressBarService.start()
    if @currentDevice.location != undefined && @currentDevice.location.key != undefined
      @currentDevice.locationKey = @currentDevice.location.key
    if @currentDevice.panelModel.id != undefined && @currentDevice.panelModel.id != 'None'
      @currentDevice.panelModelNumber = @currentDevice.panelModel.id
    if @currentDevice.panelInput.id != undefined && @currentDevice.panelInput.id != 'None'
      @currentDevice.panelSerialInput = @currentDevice.panelInput.id.toLowerCase()
    @currentDevice.timezone = @selectedTimezone
    promise = DevicesService.save @currentDevice
    promise.then @onSuccessDeviceSave, @onFailureDeviceSave

  @onSuccessDeviceSave = ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast 'We saved your update.'

  @onFailureDeviceSave = (error) ->
    ProgressBarService.complete()
    if error.status == 409
      $log.info(
        "Failure saving device. Customer display code already exists for tenant: #{error.status } #{error.statusText}")
      sweet.show('Oops...', 'This customer display code already exists for this tenant. Please choose another.', 'error')
    else
      $log.error "Failure saving device: #{error.status } #{error.statusText}"
      ToastsService.showErrorToast 'Oops. We were unable to save your updates to this device at this time.'

  @confirmDeviceDelete = (event, key) ->
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
    success = =>
      @onConfirmDelete key
    failure = =>
      @onConfirmCancel()
    showPromise.then success, failure

  @onConfirmDelete = (key) ->
    success = () ->
      ToastsService.showSuccessToast 'We processed your delete request.'
      $state.go 'devices'
    failure = (error) ->
      friendlyMessage = 'We were unable to complete your delete request at this time.'
      ToastsService.showErrorToast friendlyMessage
      $log.error "Delete device failure for device_key #{key}: #{error.status } #{error.statusText}"
    deletePromise = DevicesService.delete key
    deletePromise.then success, failure

  @onConfirmCancel = ->
    ToastsService.showInfoToast 'We canceled your delete request.'

  @onProofOfPlayLoggingCheck = ->
    if @currentDevice.proofOfPlayLogging
      if @currentDevice.locationKey == null
        sweet.show('Oops...', "Must have a location for this device to enable Proof of Play.", 'error')
        @currentDevice.proofOfPlayLogging = false
      else
        @onSaveDevice()
    else
      @onSaveDevice()

  @onUpdateLocation  = ->
    @onSaveDevice()

  @autoGenerateCustomerDisplayCode = ->
    newDisplayCode = ''
    if @currentDevice.customerDisplayName
      newDisplayCode = @currentDevice.customerDisplayName.toLowerCase()
      newDisplayCode = newDisplayCode.replace(/\s+/g, '_')
      newDisplayCode = newDisplayCode.replace(/\W+/g, '')
    @currentDevice.customerDisplayCode = newDisplayCode

  @logglyForUser = () ->
    userDomain = $cookies.get('userEmail').split("@")[1]
    return  userDomain == "demo.agosto.com" || userDomain == "agosto.com"

  #####################
  # Commands Tab
  #####################

  @onClickResetSendButton = () ->
    ProgressBarService.start()
    promise = CommandsService.reset @deviceKey
    promise.then @onResetSuccess, @onResetFailure

  @onResetSuccess = () ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast "We posted your reset command into the player's queue."

  @onResetFailure = (error) ->
    ProgressBarService.complete()
    $log.error "Reset command error: #{error.status } #{error.statusText}"
    sweet.show('Oops...', "We were unable to post your reset command into the player's queue.", 'error')

  @onClickContentDeleteSendButton = () ->
    ProgressBarService.start()
    promise = CommandsService.contentDelete @deviceKey
    promise.then @onContentDeleteSuccess, @onContentDeleteFailure

  @onContentDeleteSuccess = () ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast "We posted your content delete command into the player's queue."

  @onContentDeleteFailure = (error) ->
    ProgressBarService.complete()
    $log.error "Content delete command error: #{error.status } #{error.statusText}"
    sweet.show('Oops...', "We were unable to post your delete content command into the player's queue.", 'error')

  @onClickVolumeSendButton = () ->
    ProgressBarService.start()
    promise = CommandsService.volume @deviceKey, @currentDevice.volume
    promise.then @onVolumeSuccess(@currentDevice.volume), @onVolumeFailure

  @onVolumeSuccess = (level) ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast "We posted a volume level command of #{level} into the player's queue."

  @onVolumeFailure = (error) ->
    ProgressBarService.complete()
    $log.error "Volume level command error: #{error.status } #{error.statusText}"
    sweet.show('Oops...', "We were unable to post your volume level command into the player's queue.", 'error')

  @onClickCommandSendButton = () ->
    ProgressBarService.start()
    promise = CommandsService.custom @deviceKey, @currentDevice.custom
    promise.then @onCommandSuccess(@currentDevice.custom), @onCommandFailure

  @onCommandSuccess = (command) ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast "We posted your command '#{command}' into the player's queue."

  @onCommandFailure = (error) ->
    ProgressBarService.complete()
    $log.error "Command error: #{error.status } #{error.statusText}"
    sweet.show('Oops...', "We were unable to post your command into the player's queue.", 'error')

  @onClickRefreshButton = () ->
    ProgressBarService.start()
    @epochStart = moment(new Date(@startTime)).unix()
    @epochEnd = moment(new Date(@endTime)).unix()
    @prev_cursor = null
    @next_cursor = null
    issuesPromise = DevicesService.getIssuesByKey(@deviceKey, @epochStart, @epochEnd, @prev_cursor, @next_cursor)
    issuesPromise.then ((data) =>
      @onRefreshIssuesSuccess(data)
    ), (error) =>
      @onRefreshIssuesFailure(error)

  @onRefreshIssuesSuccess = (data) ->
    @issues = data.issues
    @prev_cursor = data.prev
    @next_cursor = data.next
    ProgressBarService.complete()

  @onRefreshIssuesFailure = (error) ->
    ProgressBarService.complete()
    ToastsService.showInfoToast 'We were unable to refresh the device issues list at this time.'
    $log.error "Failure to refresh device issues: #{error.status } #{error.statusText}"

  @onClickPowerOnSendButton = () ->
    ProgressBarService.start()
    promise = CommandsService.powerOn @deviceKey
    promise.then @onPowerOnSuccess, @onPowerOnFailure

  @onPowerOnSuccess = () ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast "We posted a power on command into the player's queue."

  @onPowerOnFailure = (error) ->
    ProgressBarService.complete()
    $log.error "Power on command error: #{error.status } #{error.statusText}"
    sweet.show('Oops...', "We were unable to post your power on command into the player's queue.", 'error')

  @onClickPowerOffSendButton = () ->
    ProgressBarService.start()
    promise = CommandsService.powerOff @deviceKey
    promise.then @onPowerOffSuccess, @onPowerOffFailure

  @onPowerOffSuccess = () ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast "We posted a power off command into the player's queue."

  @onPowerOffFailure = (error) ->
    ProgressBarService.complete()
    $log.error "Power off command error: #{error.status } #{error.statusText}"
    sweet.show('Oops...', "We were unable to post your power off command into the player's queue.", 'error')

  @
