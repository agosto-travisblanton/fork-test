'use strict'

describe 'DevicesListingCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DevicesService = undefined
  promise = undefined
  unmanagedPromise = undefined
  devices = [
    {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]
  unmanagedDevices = [
    {key: 'uhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'uhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'uhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _DevicesService_, _$stateParams_, _$state_) ->
    $controller = _$controller_
    $stateParams = _$stateParams_
    DevicesService = _DevicesService_
    $state = _$state_

  describe 'initialization', ->
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      unmanagedPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getDevicesByDistributor').and.returnValue promise
      spyOn(DevicesService, 'getUnmanagedDevicesByDistributor').and.returnValue unmanagedPromise
      controller = $controller 'DevicesListingCtrl', {}
      controller.distributorKey = 'some-key'

    it 'devices should be an array', ->
      expect(angular.isArray(controller.devices)).toBeTruthy()

    it 'unmanagedDevices should be an array', ->
      expect(angular.isArray(controller.unmanagedDevices)).toBeTruthy()

    it 'calls DevicesService.getDevicesByDistributor to retrieve all distributor devices', ->
      controller.initialize()
      expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey

    it 'calls DevicesService.getUnmanagedDevicesByDistributor to retrieve all distributor unmanaged devices', ->
      controller.initialize()
      expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey

    it "the 'then' handler caches the retrieved devices in the controller", ->
      controller.initialize()
      promise.resolve devices
      expect(controller.devices).toBe devices

    it "the 'then' handler caches the retrieved unmanaged devices in the controller", ->
      controller.initialize()
      unmanagedPromise.resolve unmanagedDevices
      expect(controller.unmanagedDevices).toBe unmanagedDevices

  describe '.editItem', ->
    item = {key: 'ahjad897d987fadafg708fg71'}

    beforeEach ->
      spyOn $state, 'go'
      controller = $controller 'DevicesListingCtrl', {}

    it "route to the 'editDevice' named route, passing the supplied device key", ->
      controller.editItem(item)
      expect($state.go).toHaveBeenCalledWith('editDevice', {deviceKey: item.key, tenantKey: ''})


