'use strict'

angular.module('skykitProvisioning').directive 'expander',
  () ->
    {
      templateUrl: 'app/items/detail/item-form.html'
    }

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
  IntegrationEvents,
  sweet,
  ProgressBarService,
  $mdDialog,
  ToastsService) ->
    vm = @
    vm.tenantKey = $stateParams.tenantKey
    vm.deviceKey = $stateParams.deviceKey
    vm.fromDevices = $stateParams.fromDevices is "true"
    vm.currentDevice = {
    }
    vm.locations = []
    vm.commandEvents = []
    vm.dayRange = 30
    vm.issues = []
    vm.pickerOptions = "{widgetPositioning: {vertical:'bottom'}, showTodayButton: true, sideBySide: true, icons:{
              next:'glyphicon glyphicon-arrow-right',
              previous:'glyphicon glyphicon-arrow-left',
              up:'glyphicon glyphicon-arrow-up',
              down:'glyphicon glyphicon-arrow-down'}}"
    vm.timezones = []
    vm.selectedTimezone = undefined
    now = new Date()
    today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    vm.endTime = now.toLocaleString().replace(/,/g, "")
    today.setDate(now.getDate() - vm.dayRange)
    vm.startTime = today.toLocaleString().replace(/,/g, "")
    vm.enrollmentEvents = []

    vm.generateLocalFromUTC = (UTCTime) ->
      localTime = moment.utc(UTCTime).toDate()
      localTime = moment(localTime).format('YYYY-MM-DD hh:mm:ss A')

    vm.replaceIssueTime = (issues) ->
      for each in issues
        if each.created
          each.created = vm.generateLocalFromUTC(each.created)
        if each.updated
          each.updated = vm.generateLocalFromUTC(each.updated)

    vm.replaceCommandTime = (issues) ->
      for each in issues
        if each.postedTime
          each.postedTime = vm.generateLocalFromUTC(each.postedTime)
        if each.confirmedTime
          each.confirmedTime = vm.generateLocalFromUTC(each.confirmedTime)

    vm.copyDeviceKey = ->
      ToastsService.showSuccessToast 'Device key copied to your clipboard'

    vm.copyCorrelationIdentifier = ->
      ToastsService.showSuccessToast 'Correlation ID copied to your clipboard'

    # event tab
    vm.getIssues = (device, epochStart, epochEnd, prev, next) ->
      ProgressBarService.start()
      issuesPromise = DevicesService.getIssuesByKey(device, epochStart, epochEnd, prev, next)
      issuesPromise.then (data) ->
        vm.replaceIssueTime(data.issues)
        vm.issues = data.issues
        vm.prev_cursor = data.prev
        vm.next_cursor = data.next
        ProgressBarService.complete()

    # command history tab
    vm.getEvents = (deviceKey, prev, next) ->
      ProgressBarService.start()
      commandEventsPromise = DevicesService.getCommandEventsByKey deviceKey, prev, next
      commandEventsPromise.then (data) ->
        vm.replaceCommandTime(data.events)
        vm.event_next_cursor = data.next_cursor
        vm.event_prev_cursor = data.prev_cursor
        vm.commandEvents = data.events
        ProgressBarService.complete()

    # enrollment tab
    vm.getEnrollmentEvents = (deviceKey) ->
      ProgressBarService.start()
      commandEventsPromise = IntegrationEvents.getEnrollmentEvents deviceKey
      commandEventsPromise.then (data) ->
        vm.enrollmentEvents = data
        ProgressBarService.complete()

    vm.showEnrollmentDetail = (details) ->
      alert details
#      confirm = $mdDialog.confirm(
#        {
#          textContent: detail
#          targetEvent: event
#          ok: 'ok'
#        }
#      )
#      showPromise = $mdDialog.show confirm
#      success = ->
#        alert 'success'
#      failure = ->
#        alert 'failure'
#      showPromise.then success, failure

    vm.paginateCall = (forward) ->
      if forward
        vm.getIssues vm.deviceKey, vm.epochStart, vm.epochEnd, null, vm.next_cursor

      else
        vm.getIssues vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, null

    vm.paginateEventCall = (forward) ->
      if forward
        vm.getEvents vm.deviceKey, null, vm.event_next_cursor

      else
        vm.getEvents vm.deviceKey, vm.event_prev_cursor, null

    vm.initialize = () ->
      vm.epochStart = moment(new Date(vm.startTime)).unix()
      vm.epochEnd = moment(new Date(vm.endTime)).unix()
      timezonePromise = TimezonesService.getCustomTimezones()
      timezonePromise.then (data) ->
        vm.timezones = data

      vm.panelModels = DevicesService.getPanelModels()
      vm.panelInputs = DevicesService.getPanelInputs()

      devicePromise = DevicesService.getDeviceByKey vm.deviceKey
      devicePromise.then ((response) ->
        vm.onGetDeviceSuccess(response)
      ), (response) ->
        vm.onGetDeviceFailure(response)

      vm.getEvents vm.deviceKey
      vm.getIssues vm.deviceKey, vm.epochStart, vm.epochEnd
      vm.getEnrollmentEvents vm.deviceKey

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
        vm.setSelectedOptions()

    vm.onGetDeviceFailure = (response) ->
      ToastsService.showErrorToast 'Oops. We were unable to fetch the details for this device at this time.'
      errorMessage = "No detail for device_key ##{vm.deviceKey}. Error: #{response.status} #{response.statusText}"
      $log.error errorMessage
      $state.go 'devices'

    vm.setSelectedOptions = () ->
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

    #####################
    # Properties Tab
    #####################

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

    vm.onUpdateLocation = ->
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

    #####################
    # Commands Tab
    #####################

    vm.onResetContent = ->
      ProgressBarService.start()
      promise = CommandsService.contentDelete vm.deviceKey
      promise.then vm.onResetContentSuccess, vm.onResetContentFailure

    vm.onResetContentSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your reset content command into the player's queue."

    vm.onResetContentFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Reset content command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your reset content command into the player's queue.", 'error')

    vm.onUpdateContent = ->
      ProgressBarService.start()
      promise = CommandsService.contentUpdate vm.deviceKey
      promise.then vm.onUpdateContentSuccess, vm.onUpdateContentFailure

    vm.onUpdateContentSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your update content command into the player's queue."

    vm.onUpdateContentFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Content update command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your update content command into the player's queue.", 'error')

    vm.onResetPlayer = ->
      ProgressBarService.start()
      promise = CommandsService.reset vm.deviceKey
      promise.then vm.onResetPlayerSuccess, vm.onResetPlayerFailure

    vm.onResetPlayerSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your reset player command into the player's queue."

    vm.onResetPlayerFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Reset player command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your reset player command into the player's queue.", 'error')

    vm.onPanelOn = ->
      ProgressBarService.start()
      promise = CommandsService.powerOn vm.deviceKey
      promise.then vm.onPanelOnSuccess, vm.onPanelOnFailure

    vm.onPanelOnSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your panel on command into the player's queue."

    vm.onPanelOnFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Panel on command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your panel on command into the player's queue.", 'error')

    vm.onPanelOff = ->
      ProgressBarService.start()
      promise = CommandsService.powerOff vm.deviceKey
      promise.then vm.onPanelOffSuccess, vm.onPanelOffFailure

    vm.onPanelOffSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your panel off command into the player's queue."

    vm.onPanelOffFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Panel off command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your panel off command into the player's queue.", 'error')

    vm.onUpdateDevice = ->
      ProgressBarService.start()
      promise = CommandsService.updateDevice vm.deviceKey
      promise.then vm.onUpdateDeviceSuccess, vm.onUpdateDeviceFailure

    vm.onUpdateDeviceSuccess = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your update device command into the player's queue."

    vm.onUpdateDeviceFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Update device command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your update device command into the player's queue.", 'error')

    vm.onVolumeChange = ->
      ProgressBarService.start()
      promise = CommandsService.volume vm.deviceKey, vm.currentDevice.volume
      promise.then vm.onVolumeChangeSuccess(vm.currentDevice.volume), vm.onVolumeChangeFailure

    vm.onVolumeChangeSuccess = (level) ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your volume change command of #{level} into the player's queue."

    vm.onVolumeChangeFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Volume change command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your volume change command into the player's queue.", 'error')

    vm.onCustomCommand = ->
      ProgressBarService.start()
      promise = CommandsService.custom vm.deviceKey, vm.currentDevice.custom
      promise.then vm.onCustomCommandSuccess(vm.currentDevice.custom), vm.onCustomCommandFailure

    vm.onCustomCommandSuccess = (command) ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast "We posted your custom command '#{command}' into the player's queue."

    vm.onCustomCommandFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Custom command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your custom command into the player's queue.", 'error')

    vm.onClickRefreshButton = () ->
      ProgressBarService.start()
      vm.epochStart = moment(new Date(vm.startTime)).unix()
      vm.epochEnd = moment(new Date(vm.endTime)).unix()
      vm.prev_cursor = null
      vm.next_cursor = null
      issuesPromise = DevicesService.getIssuesByKey(vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, vm.next_cursor)
      issuesPromise.then ((data) ->
        vm.onRefreshIssuesSuccess(data)
      ), (error) ->
        vm.onRefreshIssuesFailure(error)

    vm.onRefreshIssuesSuccess = (data) ->
      vm.replaceIssueTime(data.issues)
      vm.issues = data.issues
      vm.prev_cursor = data.prev
      vm.next_cursor = data.next
      ProgressBarService.complete()

    vm.onRefreshIssuesFailure = (error) ->
      ProgressBarService.complete()
      ToastsService.showInfoToast 'We were unable to refresh the device issues list at this time.'
      $log.error "Failure to refresh device issues: #{error.status } #{error.statusText}"

    vm
