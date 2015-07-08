'use strict'

describe 'DeviceDetailsCtrl', ->
  scope = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined
  DevicesService = undefined
  devicesServicePromise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _DevicesService_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    DevicesService = _DevicesService_
    scope = {}


  describe 'initialization', ->
    beforeEach ->
      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DevicesService, 'getDeviceByKey').and.returnValue(devicesServicePromise)

    describe 'initialization', ->
      beforeEach ->
        controller = $controller('DeviceDetailsCtrl', {$scope: scope, $stateParams: $stateParams})

      it 'currentDevice should be defined', ->
        expect(controller.currentDevice).toBeDefined()

      it 'currentDevice.key should be undefined', ->
        expect(controller.currentDevice.key).toBeUndefined()

    describe 'editing an existing device', ->
      device = {key: 'fahdsfyudsyfauisdyfoiusydfu'}

      beforeEach ->
        $stateParams = {deviceKey: 'fahdsfyudsyfauisdyfoiusydfu'}
        controller = $controller('DeviceDetailsCtrl', {$scope: scope, $stateParams: $stateParams})

      it 'editMode should be true', ->
        expect(controller.editMode).toBeTruthy()

      it 'retrieve device by key from DevicesService', ->
        devicesServicePromise.resolve(device)
        expect(DevicesService.getDeviceByKey).toHaveBeenCalledWith($stateParams.deviceKey)
        expect(controller.currentDevice).toBe(device)

    describe 'creating a new device', ->
      beforeEach ->
        $stateParams = {}
        controller = $controller('DeviceDetailsCtrl', {$scope: scope, $stateParams: $stateParams})

      it 'editMode should be false', ->
        expect(controller.editMode).toBeFalsy()

      it 'do not call DevicesService.getDeviceByKey', ->
        expect(DevicesService.getDeviceByKey).not.toHaveBeenCalled()

#  describe '.onClickSaveButton', ->
#    beforeEach ->
#      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
#      spyOn(DevicesService, 'save').and.returnValue(devicesServicePromise)
#      spyOn($state, 'go')
#      $stateParams = {}
#      controller = $controller('DeviceDetailsCtrl', {$scope: scope, $stateParams: $stateParams})
#
#    it 'call DevicesService.save, pass the current device', ->
#      controller.onClickSaveButton()
#      devicesServicePromise.resolve()
#      expect(DevicesService.save).toHaveBeenCalledWith(controller.currentDevice)
#
#    it "the 'then' handler routes navigation back to 'devices'", ->
#      controller.onClickSaveButton()
#      devicesServicePromise.resolve()
#      expect($state.go).toHaveBeenCalledWith('devices')
#
