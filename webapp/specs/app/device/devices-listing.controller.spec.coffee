'use strict'

describe 'DevicesListingCtrl', ->
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
    data = {}

    beforeEach ->
      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DevicesService, 'getDevices').and.returnValue devicesServicePromise
      controller = $controller 'DevicesListingCtrl', {
        $scope: scope,
        $stateParams: $stateParams,
        DevicesService: DevicesService
      }

    it 'devices list should be defined but empty', ->
      expect(controller.devices).toBeDefined()
      expect(controller.devices.length).toBe 0

    it 'will invoke getDevices on DeviceService', ->
      devicesServicePromise.resolve(data)
      expect(controller.devices).toBe data
      expect(DevicesService.getDevices).toHaveBeenCalled()

