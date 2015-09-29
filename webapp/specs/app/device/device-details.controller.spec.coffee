'use strict'

describe 'DeviceDetailsCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DevicesService = undefined
  devicesServicePromise = undefined
  TenantsService = undefined
  tenantsServicePromise = undefined
  sweet = undefined
  progressBarService = undefined
  serviceInjection = undefined
  device = {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  tenants = [
    {key: 'dhjad897d987fadafg708fg7d', name: 'Foobar1', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708y67d', name: 'Foobar2', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708hb55', name: 'Foobar3', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _DevicesService_, _TenantsService_, _sweet_, _$state_) ->
    $controller = _$controller_
    $stateParams = {}
    $state = {}
    $state = _$state_
    DevicesService = _DevicesService_
    TenantsService = _TenantsService_
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

  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'fetchAllTenants').and.returnValue tenantsServicePromise
      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DevicesService, 'getDeviceByKey').and.returnValue devicesServicePromise

    describe 'new mode', ->
      beforeEach ->
        controller = $controller 'DeviceDetailsCtrl', {
          $stateParams: $stateParams
          $state: $state
          DevicesService: DevicesService
          TenantsService: TenantsService
        }

      it 'currentDevice property should be defined', ->
        expect(controller.currentDevice).toBeDefined()

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

      it 'currentDevice property should be defined', ->
        expect(controller.currentDevice).toBeDefined()

      it 'call TenantsService.fetchAllTenants to retrieve all tenants', ->
        expect(TenantsService.fetchAllTenants).toHaveBeenCalled()

      it "the 'then' handler caches the retrieved tenants in the controller", ->
        tenantsServicePromise.resolve tenants
        expect(controller.tenants).toBe tenants

      it 'call DevicesService.getByKey to retrieve the selected device', ->
        expect(DevicesService.getDeviceByKey).toHaveBeenCalledWith($stateParams.deviceKey)

      it "the 'then' handler caches the retrieved device in the controller", ->
        devicesServicePromise.resolve device
        expect(controller.currentDevice).toBe device

  describe '.onClickSaveButton', ->
    beforeEach ->
      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DevicesService, 'save').and.returnValue(devicesServicePromise)
      spyOn($state, 'go')
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DeviceDetailsCtrl', serviceInjection
      controller.onClickSaveButton()
      devicesServicePromise.resolve()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call DevicesService.save with the current device', ->
      expect(DevicesService.save).toHaveBeenCalledWith(controller.currentDevice)

    describe '.onSuccessDeviceSave', ->
      beforeEach ->
        controller.onSuccessDeviceSave()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation to 'devices'", ->
        expect($state.go).toHaveBeenCalledWith('devices')

    describe '.onFailureDeviceSave', ->
      beforeEach ->
        controller.onFailureDeviceSave()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation back to 'devices'", ->
        expect($state.go).toHaveBeenCalledWith('devices')

