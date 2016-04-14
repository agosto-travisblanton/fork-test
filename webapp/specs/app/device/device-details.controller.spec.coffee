'use strict'

describe 'DeviceDetailsCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  $log = undefined
  $mdDialog = undefined
  DevicesService = undefined
  TimezonesService = undefined
  getDeviceIssuesPromise = undefined
  getPlayerCommandEventsPromise = undefined
  LocationsService = undefined
  locationsServicePromise = undefined
  CommandsService = undefined
  ToastsService = undefined
  commandsServicePromise = undefined
  sweet = undefined
  progressBarService = undefined
  serviceInjection = undefined
  cookieMock = undefined
  device = {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  issues = [
    {
      category: "Player down"
      created: "2015-12-15 18:05:52"
      elapsed_time: "37.3 minutes"
      level: 2
      level_descriptor: "danger"
      memory_utilization: 40
      program: "Test Content"
      storage_utilization: 44
      up: false
    }
    {
      category: "Player up"
      created: "2015-12-15 18:05:52"
      elapsed_time: "37.3 minutes"
      level: 0
      level_descriptor: "normal"
      memory_utilization: 40
      program: "Test Content"
      storage_utilization: 44
      up: true
    }
  ]
  commandEvents = [
    {
      payload: 'skykit.com/skdchromeapp/reset'
      gcmRegistrationId: 'asdfasdfasdfadfsa1'
      updated: '2016-01-14 18:45:44'
      confirmed: false
    }
    {
      payload: 'skykit.com/skdchromeapp/stop'
      gcmRegistrationId: 'asdfasdfasdfadfsa2'
      updated: '2016-01-14 18:23:30'
      confirmed: false
    }
  ]
  tenants = [
    {key: 'dhjad897d987fadafg708fg7d', name: 'Foobar1', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708y67d', name: 'Foobar2', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708hb55', name: 'Foobar3', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _DevicesService_, _TimezonesService_, _LocationsService_, _CommandsService_,
    _sweet_, _ToastsService_, _$state_, _$mdDialog_, _$log_) ->
    $controller = _$controller_
    $stateParams = {}
    $state = {}
    $state = _$state_
    $log = _$log_
    $mdDialog = _$mdDialog_
    DevicesService = _DevicesService_
    TimezonesService = _TimezonesService_
    LocationsService = _LocationsService_
    CommandsService = _CommandsService_
    ToastsService = _ToastsService_
    progressBarService = {
      start: ->
      complete: ->
    }
    sweet = _sweet_
    scope = {}
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
      ProgressBarService: progressBarService
      $mdDialog: $mdDialog
    }

  describe 'initialize', ->
    beforeEach ->
      locationsServicePromise = new skykitProvisioning.q.Mock
      spyOn(LocationsService, 'getLocationsByTenantKey').and.returnValue locationsServicePromise
      getDevicePromise = new skykitProvisioning.q.Mock
      timezonesPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getDeviceByKey').and.returnValue getDevicePromise
      getPlayerCommandEventsPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getCommandEventsByKey').and.returnValue getPlayerCommandEventsPromise
      getDeviceIssuesPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getIssuesByKey').and.returnValue getDeviceIssuesPromise
      spyOn(DevicesService, 'getPanelModels').and.returnValue [{'id': 'Sony–FXD40LX2F'}, {'id': 'NEC–LCD4215'}]
      inputs = [
        {
          'id': 'HDMI2'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'VGA'
          'parentId': 'NEC–LCD4215'
        }
      ]
      spyOn(DevicesService, 'getPanelInputs').and.returnValue inputs
      spyOn(TimezonesService, 'getUsTimezones').and.returnValue timezonesPromise

    describe 'new mode', ->
      beforeEach ->
        controller = $controller 'DeviceDetailsCtrl', {
          $stateParams: $stateParams
          $state: $state
          DevicesService: DevicesService
          TimezonesService: TimezonesService
          LocationsService: LocationsService
        }
        controller.initialize()

      it 'should call TimezonesService.getUsTimezones', ->
        expect(TimezonesService.getUsTimezones).toHaveBeenCalled()

      it 'currentDevice property should be defined', ->
        expect(controller.currentDevice).toBeDefined()

      it 'commandEvents array should be defined', ->
        expect(controller.commandEvents).toBeDefined()

      it 'issues array should be defined', ->
        expect(controller.issues).toBeDefined()

      it 'declares timezones as an empty array', ->
        expect(angular.isArray(controller.timezones)).toBeTruthy()
        expect(controller.timezones.length).toBe 0

      it 'declares a selectedTimezone', ->
        expect(controller.selectedTimezone).toBeUndefined()

    describe 'edit mode', ->
      beforeEach ->
        $stateParams = {
          deviceKey: 'fkasdhfjfa9s8udyva7dygoudyg'
          tenantKey: 'tkasdhfjfa9s2udyva5digopdy0'
        }
        controller = $controller 'DeviceDetailsCtrl', {
          $stateParams: $stateParams
          $state: $state
          DevicesService: DevicesService
          TimezonesService: TimezonesService
          LocationsService: LocationsService
        }
        now = new Date()
        today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
        @epochEnd = moment(new Date()).unix()
        today.setDate(today.getDate() - 30)
        @epochStart = moment(today).unix()
        controller.initialize()

      it 'should call TimezonesService.getTimezones', ->
        expect(TimezonesService.getUsTimezones).toHaveBeenCalled()

      it 'defines currentDevice property', ->
        expect(controller.currentDevice).toBeDefined()

      it 'calls DevicesService.getPanelModels to retrieve all panel models', ->
        expect(DevicesService.getPanelModels).toHaveBeenCalled()

      it 'calls DevicesService.getPanelInputs to retrieve all panel inputs', ->
        expect(DevicesService.getPanelInputs).toHaveBeenCalled()

      it 'calls DevicesService.getByKey to retrieve the selected device', ->
        expect(DevicesService.getDeviceByKey).toHaveBeenCalledWith $stateParams.deviceKey

      it 'calls DevicesService.getCommandEventsByKey to retrieve command events for device', ->
        expect(DevicesService.getCommandEventsByKey).toHaveBeenCalledWith $stateParams.deviceKey

      it 'calls DevicesService.getIssuesByKey to retrieve the issues for a given device and datetime range', ->
        expect(DevicesService.getIssuesByKey).toHaveBeenCalledWith($stateParams.deviceKey, @epochStart, @epochEnd)

      it "the 'then' handler caches the retrieved issues for a given device key in the controller", ->
        getDeviceIssuesPromise.resolve issues
        expect(controller.issues).toBe issues

      it "the 'then' handler caches the retrieved command events in the controller", ->
        getPlayerCommandEventsPromise.resolve commandEvents
        expect(controller.commandEvents).toBe commandEvents

  describe '.onClickSaveDevice', ->
    beforeEach ->
      devicesServicePromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'save').and.returnValue devicesServicePromise
      spyOn($state, 'go')
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.currentDevice.panelModel = {id: 'Sony-112'}
      controller.currentDevice.panelInput = {id: 'HDMI1', parentId: 'Sony-112'}
      controller.onClickSaveDevice()
      devicesServicePromise.resolve()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call DevicesService.save with the current device', ->
      expect(DevicesService.save).toHaveBeenCalledWith controller.currentDevice

    describe '.onSuccessDeviceSave', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onSuccessDeviceSave()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler shows a sweet", ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith 'We saved your updates to this device.'

    describe '.onFailureDeviceSave', ->
      beforeEach ->
        spyOn($log, 'info')
        spyOn(sweet, 'show')
        spyOn($log, 'error')
        spyOn(ToastsService, 'showErrorToast')

      it 'stops the progress bar', ->
        controller.onFailureDeviceSave({status: 200})
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert when the customer display code has already been used for the tenant', ->
        controller.onFailureDeviceSave({status: 409, statusText: 'Conflict'})
        expect(sweet.show).toHaveBeenCalledWith('Oops...',
          'This customer display code already exists for this tenant. Please choose another.', 'error')

      it 'logs info to the console when the customer display code has already been used for the tenant', ->
        controller.onFailureDeviceSave({status: 409, statusText: 'Conflict'})
        infoMessage = 'Failure saving device. Customer display code already exists for tenant: 409 Conflict'
        expect($log.info).toHaveBeenCalledWith infoMessage

      it 'displays a toast for general save failure', ->
        controller.onFailureDeviceSave({status: 400, statusText: 'Bad Request'})
        expect(ToastsService.showErrorToast).toHaveBeenCalledWith(
          'Oops. We were unable to save your updates to this device at this time.')

      it 'logs a detailed error to the console for a general save failure', ->
        controller.onFailureDeviceSave({status: 400, statusText: 'Bad Request'})
        expect($log.error).toHaveBeenCalledWith 'Failure saving device: 400 Bad Request'

  describe '.confirmDeviceDelete', ->
    jquery_event = {}
    device_key = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHIbCxIOQ2hyb21lT3NEZXZpY2UYgICAgICAhggM'
    confirm = undefined
    promise = undefined

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn($mdDialog, 'confirm').and.callFake -> return 'ok'
      spyOn($mdDialog, 'show').and.returnValue promise
      confirm = $mdDialog.confirm(
        {
          title: 'Are you sure to delete this device?'
          textContent: 'Please remember, you MUST remove this device from Content Manager before deleting it from Provisioning.'
          targetEvent: event
          ok: 'Delete'
          cancel: 'Cancel'
        }
      )
      controller = $controller 'DeviceDetailsCtrl', serviceInjection

    it 'calls $mdDialog.show confirm object', ->
      controller.confirmDeviceDelete(jquery_event, device_key)
      expect($mdDialog.show).toHaveBeenCalledWith confirm

    it 'calls controller.onConfirmDelete when promise resolved', ->
      spyOn(controller, 'onConfirmDelete')
      controller.confirmDeviceDelete(jquery_event, device_key)
      confirmResponse = [{result: 'ok'}]
      promise.resolve confirmResponse
      expect(controller.onConfirmDelete).toHaveBeenCalledWith device_key

    it 'calls controller.onConfirmCancel when promise rejected', ->
      spyOn(controller, 'onConfirmCancel')
      controller.confirmDeviceDelete(jquery_event, device_key)
      promise.reject([])
      expect(controller.onConfirmCancel).toHaveBeenCalled()

  describe '.onConfirmDelete', ->
    device_key = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHIbCxIOQ2hyb21lT3NEZXZpY2UYgICAgICAhggM'
    promise = undefined

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'delete').and.returnValue promise
      spyOn(sweet, 'show')
      spyOn(ToastsService, 'showSuccessToast')
      spyOn(ToastsService, 'showErrorToast')
      spyOn($state, 'go')
      spyOn($log, 'error')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection

    describe 'when promise is resolved', ->
      it 'calls DevicesService.delete with device key', ->
        controller.onConfirmDelete device_key
        expect(DevicesService.delete).toHaveBeenCalledWith device_key

      it 'displays a toast confirming that the delete request was processed', ->
        controller.onConfirmDelete device_key
        promise.resolve()
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith 'We processed your delete request.'

      it 'calls $state router', ->
        controller.onConfirmDelete device_key
        promise.resolve()
        expect($state.go).toHaveBeenCalledWith 'devices'

    describe 'when promise is rejected', ->
      it 'display an error toast with a friendly message about delete failure', ->
        controller.onConfirmDelete device_key
        promise.reject([])
        expect(ToastsService.showErrorToast).toHaveBeenCalledWith(
          'We were unable to complete your delete request at this time.')

      it 'logs a detailed error to the console', ->
        response = {status: 400, statusText: 'Bad request'}
        controller.onConfirmDelete device_key
        promise.reject(response)
        expect($log.error).toHaveBeenCalledWith "Delete device failure for device_key #{device_key}: 400 Bad request"

  describe '.onConfirmCancel', ->
    beforeEach ->
      spyOn(ToastsService, 'showInfoToast')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.onConfirmCancel()

    it 'displays a toast indicating delete request was canceled', ->
      expect(ToastsService.showInfoToast).toHaveBeenCalledWith 'We canceled your delete request.'

  describe '.onClickResetSendButton', ->
    beforeEach ->
      commandsServicePromise = new skykitProvisioning.q.Mock
      spyOn(CommandsService, 'reset').and.returnValue commandsServicePromise
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.editMode = true
      controller.onClickResetSendButton()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call CommandsService.reset with the current device', ->
      expect(CommandsService.reset).toHaveBeenCalledWith controller.currentDevice.key

    describe '.onResetSuccess', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onResetSuccess()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a toast indicating reset command was sent to the player queue', ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith "We posted your reset command into the player's queue."

    describe '.onResetFailure', ->
      error = {status: 404, statusText: 'Not Found'}

      beforeEach ->
        spyOn($log, 'error')
        spyOn(sweet, 'show')
        controller.onResetFailure error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert indicating unable to send reset command to the player queue', ->
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your reset command into the player's queue.", 'error')

      it 'logs a detailed error to the console', ->
        expect($log.error).toHaveBeenCalledWith "Reset command error: #{error.status} #{error.statusText}"

  describe '.onClickVolumeSendButton', ->
    beforeEach ->
      commandsServicePromise = new skykitProvisioning.q.Mock
      spyOn(CommandsService, 'volume').and.returnValue commandsServicePromise
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.editMode = true
      controller.currentDevice.volume = 5
      controller.onClickVolumeSendButton()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'calls CommandsService.volume with the current device', ->
      expect(CommandsService.volume).toHaveBeenCalledWith(controller.currentDevice.key, controller.currentDevice.volume)

    describe '.onVolumeSuccess', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onVolumeSuccess controller.currentDevice.volume

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a toast indicating volume command was sent to the player queue', ->
        message = "We posted a volume level command of #{controller.currentDevice.volume} into the player's queue."
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith message

    describe '.onVolumeFailure', ->
      error = {status: 404, statusText: 'Not Found'}

      beforeEach ->
        spyOn($log, 'error')
        spyOn(sweet, 'show')
        controller.onVolumeFailure error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert indicating unable to send volume command to the player queue', ->
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your volume level command into the player's queue.", 'error')

      it 'logs a detailed error to the console', ->
        expect($log.error).toHaveBeenCalledWith "Volume level command error: #{error.status} #{error.statusText}"


  describe '.onClickCommandSendButton', ->
    beforeEach ->
      commandsServicePromise = new skykitProvisioning.q.Mock
      spyOn(CommandsService, 'custom').and.returnValue(commandsServicePromise)
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.editMode = true
      controller.currentDevice.custom = 'skykit.com/skdchromeapp/channel/2'
      controller.onClickCommandSendButton()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'calls CommandsService.custom with the current device', ->
      expect(CommandsService.custom).toHaveBeenCalledWith(controller.currentDevice.key, controller.currentDevice.custom)

    describe '.onCommandSuccess', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onCommandSuccess controller.currentDevice.custom

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a toast indicating command was sent to the player queue', ->
        message = "We posted your command '#{controller.currentDevice.custom}' into the player's queue."
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith message

    describe '.onCommandFailure', ->
      error = {status: 404, statusText: 'Not Found'}

      beforeEach ->
        spyOn(sweet, 'show')
        spyOn($log, 'error')
        controller.onCommandFailure error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert indicating unable to command to the player queue', ->
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your command into the player's queue.", 'error')

      it 'logs a detailed error to the console', ->
        expect($log.error).toHaveBeenCalledWith "Command error: #{error.status} #{error.statusText}"

  describe '.onClickPowerOnSendButton', ->
    beforeEach ->
      commandsServicePromise = new skykitProvisioning.q.Mock
      spyOn(CommandsService, 'powerOn').and.returnValue commandsServicePromise
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.editMode = true
      controller.onClickPowerOnSendButton()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call CommandsService.powerOn with the current device', ->
      expect(CommandsService.powerOn).toHaveBeenCalledWith controller.currentDevice.key

    describe '.onPowerOnSuccess', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onPowerOnSuccess()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a toast indicating command was sent to player', ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted a power on command into the player's queue.")

    describe '.onPowerOnFailure', ->
      error = {status: 404, statusText: 'Not Found'}

      beforeEach ->
        spyOn(sweet, 'show')
        spyOn($log, 'error')
        controller.onPowerOnFailure error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your power on command into the player's queue.", 'error')

      it 'logs a detailed error to the console', ->
        expect($log.error).toHaveBeenCalledWith "Power on command error: #{error.status} #{error.statusText}"

  describe '.onClickPowerOffSendButton', ->
    beforeEach ->
      commandsServicePromise = new skykitProvisioning.q.Mock
      spyOn(CommandsService, 'powerOff').and.returnValue commandsServicePromise
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.editMode = true
      controller.onClickPowerOffSendButton()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call CommandsService.powerOff with the current device', ->
      expect(CommandsService.powerOff).toHaveBeenCalledWith controller.currentDevice.key

    describe '.onPowerOffSuccess', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onPowerOffSuccess()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a toast indicating command was sent to player', ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted a power off command into the player's queue.")

    describe '.onPowerOffFailure', ->
      error = {status: 404, statusText: 'Not Found'}

      beforeEach ->
        spyOn(sweet, 'show')
        spyOn($log, 'error')
        controller.onPowerOffFailure error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your power off command into the player's queue.", 'error')

      it 'logs a detailed error to the console', ->
        expect($log.error).toHaveBeenCalledWith "Power off command error: #{error.status} #{error.statusText}"

  describe '.onClickContentDeleteSendButton', ->
    beforeEach ->
      commandsServicePromise = new skykitProvisioning.q.Mock
      spyOn(CommandsService, 'contentDelete').and.returnValue commandsServicePromise
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.editMode = true
      controller.onClickContentDeleteSendButton()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'calls CommandsService.contentDelete with the current device', ->
      expect(CommandsService.contentDelete).toHaveBeenCalledWith controller.currentDevice.key

    describe '.onContentDeleteSuccess', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onContentDeleteSuccess()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a toast indicating command was sent to player', ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your content delete command into the player's queue.")

    describe '.onContentDeleteFailure', ->
      error = {status: 404, statusText: 'Not Found'}

      beforeEach ->
        spyOn(sweet, 'show')
        spyOn($log, 'error')
        controller.onContentDeleteFailure error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your delete content command into the player's queue.", 'error')

      it 'logs a detailed error to the console', ->
        expect($log.error).toHaveBeenCalledWith "Content delete command error: #{error.status} #{error.statusText}"

  describe '.onClickRefreshButton', ->
    beforeEach ->
      devicesServicePromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getIssuesByKey').and.returnValue getDeviceIssuesPromise
      spyOn(progressBarService, 'start')
      $stateParams.deviceKey = 'fkasdhfjfa9s8udyva7dygoudyg'
      controller = $controller 'DeviceDetailsCtrl', {
        $stateParams: $stateParams
        $state: $state
        DevicesService: DevicesService
        ProgressBarService: progressBarService
      }
      controller.onClickRefreshButton()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'defines epochStart', ->
      expect(controller.epochStart).toBeDefined()

    it 'defines epochEnd', ->
      expect(controller.epochEnd).toBeDefined()

    it 'calls service to refresh issues for a given device within a specified datetime range', ->
      expect(DevicesService.getIssuesByKey).toHaveBeenCalledWith(
        $stateParams.deviceKey, controller.epochStart, controller.epochEnd)

    describe '.onRefreshIssuesSuccess', ->
      beforeEach ->
        spyOn(progressBarService, 'complete')
        controller.onRefreshIssuesSuccess(issues)

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'populates the issues array with two records', ->
        expect(controller.issues.length).toBe 2

    describe '.onRefreshIssuesFailure', ->
      error = {status: 403, statusText: 'Forbidden'}

      beforeEach ->
        spyOn(progressBarService, 'complete')
        spyOn(ToastsService, 'showInfoToast')
        spyOn($log, 'error')
        controller.onRefreshIssuesFailure error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a toast with error information', ->
        expect(ToastsService.showInfoToast).toHaveBeenCalledWith(
          'We were unable to refresh the device issues list at this time.')

      it 'logs a detailed error to the console for failure to refresh issues', ->
        expect($log.error).toHaveBeenCalledWith(
          "Failure to refresh device issues: #{error.status } #{error.statusText}")

  describe '.autoGenerateCustomerDisplayCode', ->
    beforeEach ->
      controller = $controller 'DeviceDetailsCtrl', {}

    it 'generates a new customer display code', ->
      controller.currentDevice.customerDisplayName = 'Panel in Reception'
      controller.autoGenerateCustomerDisplayCode()
      expect(controller.currentDevice.customerDisplayCode).toBe 'panel_in_reception'

  describe 'isAgostoDomain', ->
    beforeEach ->
      cookieMock = {
        storage: {},
        put: (key, value) ->
          this.storage[key] = value
        get: (key) ->
          return this.storage[key]
      }
      controller = $controller 'DeviceDetailsCtrl', {$cookies: cookieMock}


    it 'is a valid domain if @demo.agosto.com', ->
      cookieMock.put("userEmail", "some.user@demo.agosto.com")
      expect(controller.logglyForUser()).toBeTruthy()

    it 'is a valid domain if @agosto.com', ->
      cookieMock.put("userEmail", "some.user@agosto.com")
      expect(controller.logglyForUser()).toBeTruthy()

    it 'is not if anything else', ->
      cookieMock.put("userEmail", "some.user@123.com")
      expect(controller.logglyForUser()).toBeFalsy()
