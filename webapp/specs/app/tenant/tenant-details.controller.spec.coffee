'use strict'

describe 'TenantDetailsCtrl', ->
  scope = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  DevicesService = undefined
  ProgressBarService = undefined
  tenantsServicePromise = undefined
  devicesServicePromise = undefined
  sweet = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _TenantsService_, _DevicesService_,  _$state_, _sweet_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    TenantsService = _TenantsService_
    DevicesService = _DevicesService_
    ProgressBarService = {
      start: ->
      complete: ->
    }
    sweet = _sweet_
    scope = {}


  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise)
      spyOn(DevicesService, 'getDevicesByTenant').and.returnValue(devicesServicePromise)

      it 'currentTenant should be set', ->
        controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
          ProgressBarService: ProgressBarService})
        expect(controller.currentTenant).toBeDefined()
        expect(controller.currentTenant.key).toBeUndefined()
        expect(controller.currentTenant.name).toBeUndefined()
        expect(controller.currentTenant.tenant_code).toBeUndefined()
        expect(controller.currentTenant.admin_email).toBeUndefined()
        expect(controller.currentTenant.content_server_url).toBeUndefined()
        expect(controller.currentTenant.chrome_device_domain).toBeUndefined()
        expect(controller.currentTenant.active).toBeTruthy()

      describe 'editing an existing tenant', ->
        it 'editMode should be set to true', ->
          $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
          controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
            ProgressBarService: ProgressBarService})
          expect(controller.editMode).toBeTruthy()

        it 'retrieve tenant by key from TenantsService', ->
          $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
          controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
            ProgressBarService: ProgressBarService})
          tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'}
          tenantsServicePromise.resolve(tenant)
          expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey)
          expect(controller.currentTenant).toBe(tenant)

        it 'retrieve tenant\'s devices by tenant key from DevicesService', ->
          $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
          controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
            ProgressBarService: ProgressBarService})
          devices = [{key: 'f8sa76d78fa978d6fa7dg7ds55'}, {key: 'f8sa76d78fa978d6fa7dg7ds56'}]
          devicesServicePromise.resolve(devices)
          expect(DevicesService.getDevicesByTenant).toHaveBeenCalledWith($stateParams.tenantKey)
          expect(controller.currentTenantDisplays).toBe(devices)

      describe 'creating a new tenant', ->
        it 'editMode should be set to false', ->
          $stateParams = {}
          controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
            ProgressBarService: ProgressBarService})
          expect(controller.editMode).toBeFalsy()

        it 'do not call TenantsService.getTenantByKey', ->
          $stateParams = {}
          controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
            ProgressBarService: ProgressBarService})
          expect(TenantsService.getTenantByKey).not.toHaveBeenCalled()

        it 'do not call Devices.getDevicesByTenant', ->
          $stateParams = {}
          controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
            ProgressBarService: ProgressBarService})
          expect(DevicesService.getDevicesByTenant).not.toHaveBeenCalled()

  describe '.onClickSaveButton', ->
    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'save').and.returnValue(tenantsServicePromise)
      spyOn($state, 'go')
      $stateParams = {}
#      spyOn(ProgressBarService, 'start')
#      spyOn(ProgressBarService, 'complete')
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
        ProgressBarService: ProgressBarService})

    it 'start the progress bar animation', ->
      controller.onClickSaveButton()
      tenantsServicePromise.resolve()
      expect(ProgressBarService.start).toHaveBeenCalled()

    it 'call TenantsService.save, pass the current tenant', ->
      controller.onClickSaveButton()
      tenantsServicePromise.resolve()
      expect(TenantsService.save).toHaveBeenCalledWith(controller.currentTenant)

    it "the 'then' handler routes navigation back to 'tenants'", ->
      controller.onClickSaveButton()
      tenantsServicePromise.resolve()
      expect($state.go).toHaveBeenCalledWith('tenants')

  describe '.autoGenerateTenantCode', ->
    beforeEach ->
      $stateParams = {}
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams,
        ProgressBarService: ProgressBarService})

    it 'generates a new tenant code when key is undefined', ->
      controller.currentTenant.key = undefined
      controller.currentTenant.name = 'Super Duper Foobar Inc.'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'super_duper_foobar_inc'

    it 'skips generating a new tenant code when key is defined', ->
      controller.currentTenant.key = 'd8ad97ad87afg897f987g0f8'
      controller.currentTenant.name = 'Foobar Inc.'
      controller.currentTenant.tenant_code = 'barfoo_company'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'barfoo_company'
