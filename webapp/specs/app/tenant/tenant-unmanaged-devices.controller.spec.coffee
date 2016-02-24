'use strict'

describe 'TenantUnmanagedDevicesCtrl', ->
  scope = undefined
  $controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  DevicesService = undefined
  serviceInjection = undefined
  tenantsServicePromise = undefined
  devicesServicePromise = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _TenantsService_, _DevicesService_, _$state_, _$rootScope_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    $rootScope = _$rootScope_
    TenantsService = _TenantsService_
    DevicesService = _DevicesService_
    scope = $rootScope.$new()
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
      TenantsService: TenantsService
      DevicesService: DevicesService
    }

  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      devicesServicePromise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'getTenantByKey').and.returnValue tenantsServicePromise
      spyOn(DevicesService, 'getUnmanagedDevicesByTenant').and.returnValue devicesServicePromise

    it 'currentTenant should be set', ->
      controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
      expect(controller.currentTenant).toBeDefined()
      expect(controller.currentTenant.key).toBeUndefined()
      expect(controller.currentTenant.name).toBeUndefined()
      expect(controller.currentTenant.tenant_code).toBeUndefined()
      expect(controller.currentTenant.admin_email).toBeUndefined()
      expect(controller.currentTenant.content_server_url).toBeUndefined()
      expect(controller.currentTenant.domain_key).toBeUndefined()
      expect(controller.currentTenant.notification_emails).toBeUndefined()
      expect(controller.currentTenant.proof_of_play_logging).toBeFalsy()
      expect(controller.currentTenant.active).toBeTruthy()

    it 'tenantDevices property should be defined', ->
      controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
      expect(controller.tenantDevices).toBeDefined()

    describe 'editing an existing tenant', ->
      beforeEach ->
        progressBarService = {
          start: ->
          complete: ->
        }
        $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
        serviceInjection = {
          $scope: scope
          $stateParams: $stateParams
          ProgressBarService: progressBarService
        }

      it 'editMode should be set to true', ->
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        expect(controller.editMode).toBeTruthy()

      it 'retrieve tenant by key from TenantsService', ->
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'}
        tenantsServicePromise.resolve(tenant)
        expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey)
        expect(controller.currentTenant).toBe(tenant)

      it 'retrieve tenant\'s devices by tenant key from DevicesService', ->
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        devices = [{key: 'f8sa76d78fa978d6fa7dg7ds55'}, {key: 'f8sa76d78fa978d6fa7dg7ds56'}]
        data = {objects: devices}
        devicesServicePromise.resolve(data)
        expect(DevicesService.getUnmanagedDevicesByTenant).toHaveBeenCalledWith($stateParams.tenantKey)
        expect(controller.tenantDevices).toBe(devices)

    describe 'creating a new tenant', ->
      it 'editMode should be set to false', ->
        $stateParams = {}
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        expect(controller.editMode).toBeFalsy()

      it 'do not call TenantsService.getTenantByKey', ->
        $stateParams = {}
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        expect(TenantsService.getTenantByKey).not.toHaveBeenCalled()

      it 'do not call Devices.getUnmanagedDevicesByTenant', ->
        $stateParams = {}
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        expect(DevicesService.getUnmanagedDevicesByTenant).not.toHaveBeenCalled()

