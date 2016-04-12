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
    _sweet_, _$state_, _$mdDialog_, _$log_) ->
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
        spyOn(sweet, 'show')
        controller.onSuccessDeviceSave()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler shows a sweet", ->
        expect(sweet.show).toHaveBeenCalledWith('WooHoo!', 'Your changes were saved!', 'success')

    describe '.onFailureDeviceSave', ->
      beforeEach ->
        spyOn(sweet, 'show')

      it 'stops the progress bar', ->
        controller.onFailureDeviceSave({status: 200})
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert for general save failure', ->
        controller.onFailureDeviceSave({status: 400})
        expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to save updated device.', 'error')

      it 'displays a sweet alert for customer display code already used for tenant', ->
        controller.onFailureDeviceSave({status: 409})
        expect(sweet.show).toHaveBeenCalledWith('Oops...',
          'This customer display code already exists for this tenant. Please choose another.', 'error')

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
      spyOn($state, 'go')
      spyOn($log, 'error')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection

    describe 'when promise is resolved', ->
      it 'calls DevicesService.delete with device key', ->
        controller.onConfirmDelete device_key
        expect(DevicesService.delete).toHaveBeenCalledWith device_key

      it 'calls sweet alert', ->
        controller.onConfirmDelete device_key
        promise.resolve()
        expect(sweet.show).toHaveBeenCalledWith('Ok', 'Delete processed.', 'success')

      it 'calls $state router', ->
        controller.onConfirmDelete device_key
        promise.resolve()
        expect($state.go).toHaveBeenCalledWith 'devices'

    describe 'when promise is rejected', ->
      it 'calls sweet alert with friendly message', ->
        controller.onConfirmDelete device_key
        promise.reject([])
        expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to delete device', 'error')

      it 'logs a detailed error', ->
        response = {status: 400, statusText: 'Bad request'}
        controller.onConfirmDelete device_key
        promise.reject(response)
        expect($log.error).toHaveBeenCalledWith "Unable to delete device with key #{device_key}: 400 Bad request"

  describe '.onConfirmCancel', ->
    beforeEach ->
      spyOn(sweet, 'show')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection

    it 'calls sweet alert confirming delete was cancelled', ->
      controller.onConfirmCancel()
      expect(sweet.show).toHaveBeenCalledWith('Ok', 'Delete cancelled.', 'success')

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
        spyOn(sweet, 'show')
        controller.onResetSuccess()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Success!', 'Sent a reset command to Google Cloud Messaging.',
          'success')

    describe '.onResetFailure', ->
      beforeEach ->
        @error = {data: '404 Not Found'}
        spyOn(sweet, 'show')
        controller.onResetFailure @error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Oops...', "Reset error: #{@error.data}", 'error')

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
        spyOn(sweet, 'show')
        controller.onVolumeSuccess controller.currentDevice.volume

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Success!',
          "Sent a volume level of #{controller.currentDevice.volume} to Google Cloud Messaging.", 'success')

    describe '.onVolumeFailure', ->
      beforeEach ->
        @error = {data: '404 Not Found'}
        spyOn(sweet, 'show')
        controller.onVolumeFailure @error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Oops...', "Volume error: #{@error.data}", 'error')

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
        spyOn(sweet, 'show')
        controller.onCommandSuccess controller.currentDevice.custom

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Success!',
          "Sent '#{controller.currentDevice.custom}' to Google Cloud Messaging.", 'success')

    describe '.onCommandFailure', ->
      beforeEach ->
        @error = {data: '404 Not Found'}
        spyOn(sweet, 'show')
        controller.onCommandFailure @error

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Oops...', "Command error: #{@error.data}", 'error')

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
          spyOn(sweet, 'show')
          controller.onPowerOnSuccess()

        it 'stops the progress bar', ->
          expect(progressBarService.complete).toHaveBeenCalled()

        it 'displays a sweet alert', ->
          expect(sweet.show).toHaveBeenCalledWith('Success!', 'Sent a power on command to Google Cloud Messaging.',
            'success')

      describe '.onPowerOnFailure', ->
        beforeEach ->
          @error = {data: '404 Not Found'}
          spyOn(sweet, 'show')
          controller.onPowerOnFailure @error

        it 'stops the progress bar', ->
          expect(progressBarService.complete).toHaveBeenCalled()

        it 'displays a sweet alert', ->
          expect(sweet.show).toHaveBeenCalledWith('Oops...', "Reset error: #{@error.data}", 'error')

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
          spyOn(sweet, 'show')
          controller.onPowerOffSuccess()

        it 'stops the progress bar', ->
          expect(progressBarService.complete).toHaveBeenCalled()

        it 'displays a sweet alert', ->
          expect(sweet.show).toHaveBeenCalledWith('Success!', 'Sent a power off command to Google Cloud Messaging.',
            'success')

      describe '.onPowerOffFailure', ->
        beforeEach ->
          @error = {data: '404 Not Found'}
          spyOn(sweet, 'show')
          controller.onPowerOnFailure @error

        it 'stops the progress bar', ->
          expect(progressBarService.complete).toHaveBeenCalled()

        it 'displays a sweet alert', ->
          expect(sweet.show).toHaveBeenCalledWith('Oops...', "Reset error: #{@error.data}", 'error')

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
          spyOn(sweet, 'show')
          controller.onContentDeleteSuccess()

        it 'stops the progress bar', ->
          expect(progressBarService.complete).toHaveBeenCalled()

        it 'displays a sweet alert', ->
          expect(sweet.show).toHaveBeenCalledWith('Success!', 'Sent a content delete command to Google Cloud Messaging.',
            'success')

      describe '.onContentDeleteFailure', ->
        beforeEach ->
          @error = {data: '404 Not Found'}
          spyOn(sweet, 'show')
          controller.onContentDeleteFailure @error

        it 'stops the progress bar', ->
          expect(progressBarService.complete).toHaveBeenCalled()

        it 'displays a sweet alert', ->
          expect(sweet.show).toHaveBeenCalledWith('Oops...', "Content delete error: #{@error.data}", 'error')

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
      error_text = undefined

      beforeEach ->
        spyOn(progressBarService, 'complete')
        spyOn(sweet, 'show')
        error_text = '403 Forbidden'
        error = {'data': error_text}
        controller.onRefreshIssuesFailure(error)

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert with error information', ->
        expect(sweet.show).toHaveBeenCalledWith('Oops...', "Refresh error: #{error_text}", 'error')

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
