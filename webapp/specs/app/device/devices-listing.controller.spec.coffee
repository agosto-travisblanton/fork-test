'use strict'

describe 'DevicesListingCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  DevicesService = undefined
  promise = undefined
  devices = [
    {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]


  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _DevicesService_, _$stateParams_) ->
    $controller = _$controller_
    $stateParams = _$stateParams_
    DevicesService = _DevicesService_

  describe 'initialization', ->
    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DevicesService, 'getDevices').and.returnValue promise
      controller = $controller 'DevicesListingCtrl', {$stateParams: $stateParams, DevicesService: DevicesService}

    it 'displays should be an empty array', ->
      expect(angular.isArray(controller.devices)).toBeTruthy()

    it 'call DevicesService.getDisplays to retrieve all displays', ->
      controller.initialize()
      expect(DevicesService.getDevices).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved displays in the controller", ->
      controller.initialize()
      promise.resolve devices
      expect(controller.devices).toBe devices


