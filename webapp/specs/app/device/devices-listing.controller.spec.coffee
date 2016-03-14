'use strict'

describe 'DevicesListingCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DevicesService = undefined
  promise = undefined
  unmanagedPromise = undefined
  ProgressBarService = undefined
  sweet = undefined
  to_respond_with_devices = {
    devices: [
      {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'dhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'dhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]
  }
  to_respond_with_unmanagedDevices = {
    unmanagedDevices: [
      {key: 'uhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'uhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'uhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]
  }

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _DevicesService_, _$stateParams_, _$state_, _ProgressBarService_, _sweet_) ->
    $controller = _$controller_
    $stateParams = _$stateParams_
    DevicesService = _DevicesService_
    $state = _$state_
    ProgressBarService = _ProgressBarService_
    sweet = _sweet_

  describe 'initialization', ->
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      unmanagedPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getDevicesByDistributor').and.returnValue promise
      spyOn(DevicesService, 'getUnmanagedDevicesByDistributor').and.returnValue unmanagedPromise
      spyOn(ProgressBarService, 'start')
      spyOn(ProgressBarService, 'complete')
      controller = $controller 'DevicesListingCtrl', {}
      controller.distributorKey = 'some-key'

    it 'devices should be an array', ->
      expect(angular.isArray(controller.devices)).toBeTruthy()

    it 'unmanagedDevices should be an array', ->
      expect(angular.isArray(controller.unmanagedDevices)).toBeTruthy()

    it 'calls DevicesService.getDevicesByDistributor to retrieve all distributor devices', ->
      controller.initialize()
      expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.devicesPrev, controller.devicesNext

    it 'starts the progress bar', ->
      controller.initialize()
      expect(ProgressBarService.start).toHaveBeenCalled()

    it 'calls DevicesService.getUnmanagedDevicesByDistributor to retrieve all distributor unmanaged devices', ->
      controller.initialize()
      expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.unmanagedDevicesPrev, controller.unmanagedDevicesNext

    it "the 'then' handler caches the retrieved devices and unmanaged devices in the controller", ->
      controller.getManagedAndUnmanagedDevices()
      promise.resolve to_respond_with_devices
      unmanagedPromise.resolve to_respond_with_unmanagedDevices
      expect(controller.devices).toBe to_respond_with_devices.devices
      expect(controller.unmanagedDevices).toBe to_respond_with_unmanagedDevices.devices

  describe '.getFetchSuccess', ->
    beforeEach ->
      spyOn(ProgressBarService, 'complete')
      controller = $controller 'DevicesListingCtrl', {}

    it 'stops the progress bar', ->
      controller.getFetchSuccess()
      expect(ProgressBarService.complete).toHaveBeenCalled()

  describe '.getFetchFailure', ->
    response = {status: 400, statusText: 'Bad request'}
    beforeEach ->
      spyOn(ProgressBarService, 'complete')
      spyOn(sweet, 'show')
      controller = $controller 'DevicesListingCtrl', {}

    it 'stops the progress bar', ->
      controller.getFetchFailure response
      expect(ProgressBarService.complete).toHaveBeenCalled()

    it 'calls seet alert with error', ->
      controller.getFetchFailure response
      expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to fetch devices. Error: 400 Bad request.', 'error')

  describe '.editItem', ->
    item = {key: 'ahjad897d987fadafg708fg71', tenantKey: 'ahjad897d987fadafg708fg71', fromDevices: true}

    beforeEach ->
      spyOn $state, 'go'
      controller = $controller 'DevicesListingCtrl', {}

    it "route to the 'editDevice' named route, passing the supplied device key", ->
      controller.editItem(item)
      expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: item.key,
        tenantKey: item.tenantKey,
        fromDevices: true
      })

  describe '.paginateCall', ->

    beforeEach ->
      spyOn $state, 'go'
      promise = new skykitProvisioning.q.Mock
      unmanagedPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getDevicesByDistributor').and.returnValue promise
      spyOn(DevicesService, 'getUnmanagedDevicesByDistributor').and.returnValue unmanagedPromise
      spyOn(ProgressBarService, 'start')
      spyOn(ProgressBarService, 'complete')
      controller = $controller 'DevicesListingCtrl', {}
      controller.devicesPrev = '1'
      controller.devicesNext = '2'
      controller.unmanagedDevicesPrev = '3'
      controller.unmanagedDevicesNext = '4'
      controller.distributorKey = 'some-key'

    it "paginated forward with unmanaged", ->
      controller.paginateCall(true, false)
      expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, null, controller.unmanagedDevicesNext

    it 'paginates forward with managed', ->
      controller.paginateCall(true, true)
      expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, null, controller.devicesNext


    it "paginated backward with unmanaged", ->
      controller.paginateCall(false, false)
      expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.unmanagedDevicesPrev, null

    it 'paginates backward with managed', ->
      controller.paginateCall(false, true)
      expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.devicesPrev, null
