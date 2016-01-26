'use strict'

describe 'DeviceDetailsCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DevicesService = undefined
  devicesServicePromise = undefined
  getDevicePromise = undefined
  getDeviceIssuesPromise = undefined
  getPlayerCommandEventsPromise = undefined
  TenantsService = undefined
  tenantsServicePromise = undefined
  CommandsService = undefined
  commandsServicePromise = undefined
  sweet = undefined
  progressBarService = undefined
  serviceInjection = undefined
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

  beforeEach inject (_$controller_, _DevicesService_, _TenantsService_, _CommandsService_, _sweet_, _$state_) ->
    $controller = _$controller_
    $stateParams = {}
    $state = {}
    $state = _$state_
    DevicesService = _DevicesService_
    TenantsService = _TenantsService_
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
    }

  describe 'initialize', ->
    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'fetchAllTenants').and.returnValue tenantsServicePromise
      getDevicePromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getDeviceByKey').and.returnValue getDevicePromise
      getPlayerCommandEventsPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getCommandEventsByKey').and.returnValue getPlayerCommandEventsPromise
      getDeviceIssuesPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getIssuesByKey').and.returnValue getDeviceIssuesPromise
      spyOn(DevicesService, 'getPanelModels').and.returnValue [{'id': 'Sony–FXD40LX2F'}, {'id': 'NEC–LCD4215'}]
      inputs = [
        {
          'id': 'son1'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son2'
          'displayName': '0x09 INPUT1 YUV (Analog)'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'nec1'
          'displayName': 'HDMI-1'
          'parentId': 'NEC–LCD4215'
        }
      ]
      spyOn(DevicesService, 'getPanelInputs').and.returnValue inputs

    describe 'new mode', ->
      beforeEach ->
        controller = $controller 'DeviceDetailsCtrl', {
          $stateParams: $stateParams
          $state: $state
          DevicesService: DevicesService
          TenantsService: TenantsService
        }
        controller.initialize()

      it 'currentDevice property should be defined', ->
        expect(controller.currentDevice).toBeDefined()

      it 'commandEvents array should be defined', ->
        expect(controller.commandEvents).toBeDefined()

      it 'issues array should be defined', ->
        expect(controller.issues).toBeDefined()

      it 'call TenantsService.fetchAllTenants to retrieve all tenants', ->
        expect(TenantsService.fetchAllTenants).toHaveBeenCalled()

      it "the 'then' handler caches the retrieved tenants in the controller", ->
        tenantsServicePromise.resolve tenants
        expect(controller.tenants).toBe tenants

    describe 'edit mode', ->
      beforeEach ->
        $stateParams.deviceKey = 'fkasdhfjfa9s8udyva7dygoudyg'
        controller = $controller 'DeviceDetailsCtrl', {
          $stateParams: $stateParams
          $state: $state
          DevicesService: DevicesService
          TenantsService: TenantsService
        }
        now = new Date()
        today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
        @epochEnd = moment(new Date()).unix()
        today.setDate(today.getDate() - 1)
        @epochStart = moment(today).unix()
        controller.initialize()

      it 'defines currentDevice property', ->
        expect(controller.currentDevice).toBeDefined()

      it 'calls DevicesService.getPanelModels to retrieve all panel models', ->
        expect(DevicesService.getPanelModels).toHaveBeenCalled()

      it 'calls DevicesService.getPanelInputs to retrieve all panel inputs', ->
        expect(DevicesService.getPanelInputs).toHaveBeenCalled()

      it 'calls TenantsService.fetchAllTenants to retrieve all tenants', ->
        expect(TenantsService.fetchAllTenants).toHaveBeenCalled()

      it "the 'then' handler caches the retrieved tenants in the controller", ->
        tenantsServicePromise.resolve tenants
        expect(controller.tenants).toBe tenants

      it 'calls DevicesService.getByKey to retrieve the selected device', ->
        expect(DevicesService.getDeviceByKey).toHaveBeenCalledWith $stateParams.deviceKey

      it 'calls DevicesService.getCommandEventsByKey to retrieve command events for device', ->
        expect(DevicesService.getCommandEventsByKey).toHaveBeenCalledWith $stateParams.deviceKey

      it "the 'then' handler caches the retrieved device in the controller", ->
        getDevicePromise.resolve device
        expect(controller.currentDevice).toBe device

      it 'calls DevicesService.getIssuesByKey to retrieve the issues for a given device and datetime range', ->
        expect(DevicesService.getIssuesByKey).toHaveBeenCalledWith($stateParams.deviceKey, @epochStart, @epochEnd)

      it "the 'then' handler caches the retrieved issues for a given device key in the controller", ->
        getDeviceIssuesPromise.resolve issues
        expect(controller.issues).toBe issues

      it "the 'then' handler caches the retrieved command events in the controller", ->
        getPlayerCommandEventsPromise.resolve commandEvents
        expect(controller.commandEvents).toBe commandEvents

  describe '.onClickSaveNotes', ->
    beforeEach ->
      devicesServicePromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'save').and.returnValue devicesServicePromise
      spyOn($state, 'go')
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.currentDevice.panelModel = {id: 'Sony-112'}
      controller.currentDevice.panelInput = {id: 'son01'}
      controller.onClickSaveNotes()
      devicesServicePromise.resolve()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call DevicesService.save with the current device', ->
      expect(DevicesService.save).toHaveBeenCalledWith controller.currentDevice

    describe '.onSuccessDeviceSave', ->
      beforeEach ->
        controller.onSuccessDeviceSave()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation to 'devices'", ->
        expect($state.go).toHaveBeenCalledWith 'devices'

    describe '.onFailureDeviceSaveNotes', ->
      beforeEach ->
        spyOn(sweet, 'show')
        controller.onFailureDeviceSaveNotes()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to save the device notes.', 'error')

      it "the 'then' handler routes navigation back to 'devices'", ->
        expect($state.go).toHaveBeenCalledWith 'devices'

  describe '.onClickSavePanels', ->
    beforeEach ->
      devicesServicePromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'save').and.returnValue devicesServicePromise
      spyOn($state, 'go')
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.currentDevice.panelModel = {id: 'Sony-112'}
      controller.currentDevice.panelInput = {id: 'son01'}
      controller.onClickSavePanels()
      devicesServicePromise.resolve()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call DevicesService.save with the current device', ->
      expect(DevicesService.save).toHaveBeenCalledWith controller.currentDevice

    describe '.setPanelInfo', ->
      it 'sets panel model None to null', ->
        controller.currentDevice.panelModel = {id: 'None'}
        controller.setPanelInfo()
        expect(controller.currentDevice.panelModel).toBe null

      it 'sets panel model to id', ->
        panelModel = 'Foobar-122'
        controller.currentDevice.panelModel = {id: panelModel}
        controller.setPanelInfo()
        expect(controller.currentDevice.panelModel).toBe panelModel

      it 'sets panel input 0 to null', ->
        controller.currentDevice.panelInput = {id: '0'}
        controller.setPanelInfo()
        expect(controller.currentDevice.panelInput).toBe null

      it 'sets panel input to id', ->
        panelInput = 'DVI'
        controller.currentDevice.panelInput = {id: panelInput}
        controller.setPanelInfo()
        expect(controller.currentDevice.panelInput).toBe panelInput

    describe '.onSuccessDeviceSave', ->
      beforeEach ->
        controller.onSuccessDeviceSave()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation to 'devices'", ->
        expect($state.go).toHaveBeenCalledWith 'devices'

    describe '.onFailureDeviceSavePanels', ->
      beforeEach ->
        spyOn(sweet, 'show')
        controller.onFailureDeviceSavePanels()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to save the serial control information.', 'error')

      it "the 'then' handler routes navigation back to 'devices'", ->
        expect($state.go).toHaveBeenCalledWith 'devices'

  describe '.onClickSaveGeoLocation', ->
    beforeEach ->
      devicesServicePromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'save').and.returnValue devicesServicePromise
      spyOn($state, 'go')
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.currentDevice.panelModel = {id: 'Sony-112'}
      controller.currentDevice.panelInput = {id: 'son01'}
      controller.onClickSaveGeoLocation()
      devicesServicePromise.resolve()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call DevicesService.save with the current device', ->
      expect(DevicesService.save).toHaveBeenCalledWith controller.currentDevice

    describe '.onFailureGeoLocation', ->
      beforeEach ->
        spyOn(sweet, 'show')
        controller.onFailureGeoLocation()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays a sweet alert', ->
        expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to save the geo location.', 'error')

      it "the 'then' handler routes navigation back to 'devices'", ->
        expect($state.go).toHaveBeenCalledWith 'devices'

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
