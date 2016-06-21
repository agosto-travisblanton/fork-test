'use strict'
appModule = angular.module('skykitProvisioning')
appModule.controller 'DeviceDetailsCommandsCtrl', (
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
  ToastsService,
  $timeout) ->
    vm = @
    vm.tenantKey = $stateParams.tenantKey
    vm.deviceKey = $stateParams.deviceKey
    vm.fromDevices = $stateParams.fromDevices is "true"
    vm.currentDevice = {}
    vm.commandEvents = []

    vm.generateLocalFromUTC = (UTCTime) ->
      localTime = moment.utc(UTCTime).toDate()
      localTime = moment(localTime).format('YYYY-MM-DD hh:mm:ss A')

    vm.replaceCommandTime = (issues) ->
      for each in issues
        if each.postedTime
          each.postedTime = vm.generateLocalFromUTC(each.postedTime)
        if each.confirmedTime
          each.confirmedTime = vm.generateLocalFromUTC(each.confirmedTime)

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

    vm.getEventsTimeOut = (deviceKey, prev, next) ->
      $timeout ( ->
        vm.getEvents deviceKey, prev, next
      ), 1000

    vm.commandHistorySelected = () ->
      vm.getEvents vm.deviceKey
      
    vm.paginateEventCall = (forward) ->
      if forward
        vm.getEvents vm.deviceKey, null, vm.event_next_cursor

      else
        vm.getEvents vm.deviceKey, vm.event_prev_cursor, null

    vm.initialize = () ->
      devicePromise = DevicesService.getDeviceByKey vm.deviceKey
      devicePromise.then ((response) ->
        vm.onGetDeviceSuccess(response)
      ), (response) ->
        vm.onGetDeviceFailure(response)

      vm.getEvents vm.deviceKey

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

    #####################
    # Commands Tab
    #####################

    vm.onResetContent = ->
      ProgressBarService.start()
      promise = CommandsService.contentDelete vm.deviceKey
      promise.then vm.onResetContentSuccess, vm.onResetContentFailure

    vm.onResetContentSuccess = ->
      ProgressBarService.complete()
      vm.getEventsTimeOut vm.deviceKey
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
      vm.getEventsTimeOut vm.deviceKey
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
      vm.getEventsTimeOut vm.deviceKey
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
      vm.getEventsTimeOut vm.deviceKey
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
      vm.getEventsTimeOut vm.deviceKey
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
      vm.getEventsTimeOut vm.deviceKey
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
      vm.getEventsTimeOut vm.deviceKey
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
      vm.getEventsTimeOut vm.deviceKey
      ToastsService.showSuccessToast "We posted your custom command '#{command}' into the player's queue."

    vm.onCustomCommandFailure = (error) ->
      ProgressBarService.complete()
      $log.error "Custom command error: #{error.status } #{error.statusText}"
      sweet.show('Oops...', "We were unable to post your custom command into the player's queue.", 'error')

    vm
