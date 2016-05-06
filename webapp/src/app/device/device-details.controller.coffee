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


    @copyDeviceKey = () ->
      ToastsService.showSuccessToast 'Device key has been copied to your clipboard'

    # event tab
    @getIssues = (device, epochStart, epochEnd, prev, next) =>
      ProgressBarService.start()
      issuesPromise = DevicesService.getIssuesByKey(device, epochStart, epochEnd, prev, next)
      issuesPromise.then (data) =>
        @issues = data.issues
        @prev_cursor = data.prev
        @next_cursor = data.next
        ProgressBarService.complete()


    # command history tab
    @getEvents = (deviceKey, prev, next) =>
      ProgressBarService.start()
      commandEventsPromise = DevicesService.getCommandEventsByKey deviceKey, prev, next
      commandEventsPromise.then (data) =>
        @event_next_cursor = data.next_cursor
        @event_prev_cursor = data.prev_cursor
        @commandEvents = data.events
        ProgressBarService.complete()

    @paginateCall = (forward) =>
      if forward
        @getIssues @deviceKey, @epochStart, @epochEnd, null, @next_cursor

      else
        @getIssues @deviceKey, @epochStart, @epochEnd, @prev_cursor, null


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
      @getIssues @deviceKey, @epochStart, @epochEnd

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
        noLocation = @currentDevice.locationKey == null
        noDisplayCode = @currentDevice.customerDisplayCode == null
        if noLocation
          sweet.show('Oops...', "You must have a Location to enable Proof of play.", 'error')
          @currentDevice.proofOfPlayLogging = false
        else if noDisplayCode
          sweet.show('Oops...', "You must have a Display code to enable Proof of play.", 'error')
          @currentDevice.proofOfPlayLogging = false
        else
          @onSaveDevice()
      else
        @onSaveDevice()

    @onUpdateLocation = ->
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

    @onResetContent = ->
      ProgressBarService.start()
      promise = CommandsService.contentDelete @deviceKey
      promise.then @onResetContentSuccess, @onResetContentFailure

    @onResetContentSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your reset content command into the player's queue."

    @onResetContentFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Reset content command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your reset content command into the player's queue.", 'error')

    @onUpdateContent = ->
      ProgressBarService.start()
      promise = CommandsService.contentUpdate @deviceKey
      promise.then @onUpdateContentSuccess, @onUpdateContentFailure

    @onUpdateContentSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your update content command into the player's queue."

    @onUpdateContentFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Content update command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your update content command into the player's queue.", 'error')

    @onResetPlayer = ->
      ProgressBarService.start()
      promise = CommandsService.reset @deviceKey
      promise.then @onResetPlayerSuccess, @onResetPlayerFailure

    @onResetPlayerSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your reset player command into the player's queue."

    @onResetPlayerFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Reset player command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your reset player command into the player's queue.", 'error')

    @onPanelOn = ->
      ProgressBarService.start()
      promise = CommandsService.powerOn @deviceKey
      promise.then @onPanelOnSuccess, @onPanelOnFailure

    @onPanelOnSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your panel on command into the player's queue."

    @onPanelOnFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Panel on command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your panel on command into the player's queue.", 'error')

    @onPanelOff = ->
      ProgressBarService.start()
      promise = CommandsService.powerOff @deviceKey
      promise.then @onPanelOffSuccess, @onPanelOffFailure

    @onPanelOffSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your panel off command into the player's queue."

    @onPanelOffFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Panel off command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your panel off command into the player's queue.", 'error')

    @onUpdateDevice = ->
      ProgressBarService.start()
      promise = CommandsService.updateDevice @deviceKey
      promise.then @onUpdateDeviceSuccess, @onUpdateDeviceFailure

    @onUpdateDeviceSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your update device command into the player's queue."

    @onUpdateDeviceFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Update device command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your update device command into the player's queue.", 'error')

    @onVolumeChange = ->
      ProgressBarService.start()
      promise = CommandsService.volume @deviceKey, @currentDevice.volume
      promise.then @onVolumeChangeSuccess(@currentDevice.volume), @onVolumeChangeFailure

    @onVolumeChangeSuccess = (level) ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your volume change command of #{level} into the player's queue."

    @onVolumeChangeFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Volume change command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your volume change command into the player's queue.", 'error')

    @onCustomCommand = ->
      ProgressBarService.start()
      promise = CommandsService.custom @deviceKey, @currentDevice.custom
      promise.then @onCustomCommandSuccess(@currentDevice.custom), @onCustomCommandFailure

    @onCustomCommandSuccess = (command) ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your custom command '#{command}' into the player's queue."

    @onCustomCommandFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Custom command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your custom command into the player's queue.", 'error')

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

    @
