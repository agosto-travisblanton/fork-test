'use strict'

describe 'TenantDetailsCtrl', ->
  scope = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _TenantsService_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    TenantsService = _TenantsService_
    scope = {}


  describe 'initialization', ->
    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(promise)

    it 'currentTenant should be set', ->
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams})
      expect(controller.currentTenant).toBeDefined()
      expect(controller.currentTenant.key).toBeUndefined()
      expect(controller.currentTenant.name).toBeUndefined()
      expect(controller.currentTenant.tenant_code).toBeUndefined()
      expect(controller.currentTenant.admin_email).toBeUndefined()
      expect(controller.currentTenant.content_server_url).toBeUndefined()
      expect(controller.currentTenant.chrome_device_domain).toBeUndefined()
      expect(controller.currentTenant.active).toBeTruthy()

    it 'editMode should be set to true', ->
      $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams})
      expect(controller.editMode).toBeTruthy()

    it 'editMode should be set to false', ->
      $stateParams = {}
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams})
      expect(controller.editMode).toBeFalsy()

    it 'when editMode is true, retrieve tenant by key', ->
      $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams})
      tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'}
      promise.resolve(tenant)
      expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey)
      expect(controller.currentTenant).toBe(tenant)

    it 'when editMode is false, do not call TenantsService.getTenantByKey', ->
      $stateParams = {}
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams})
      expect(TenantsService.getTenantByKey).not.toHaveBeenCalled()

  describe '.onClickSaveButton', ->
    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'save').and.returnValue(promise)
      spyOn($state, 'go')
      $stateParams = {}
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams})

    it 'call TenantsService.save, pass the current tenant', ->
      controller.onClickSaveButton()
      promise.resolve()
      expect(TenantsService.save).toHaveBeenCalledWith(controller.currentTenant)

    it "the 'then' handler routes navigation back to 'tenants'", ->
      controller.onClickSaveButton()
      promise.resolve()
      expect($state.go).toHaveBeenCalledWith('tenants')

  describe '.autoGenerateTenantCode', ->
    beforeEach ->
      $stateParams = {}
      controller = $controller('TenantDetailsCtrl', {$scope: scope, $stateParams: $stateParams})

    it 'generates a new tenant code when key is undefined', ->
      controller.currentTenant.key = undefined
      controller.currentTenant.name = 'Foobar Inc.'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'foobar_inc'

    it 'skips generating a new tenant code when key is defined', ->
      controller.currentTenant.key = 'd8ad97ad87afg897f987g0f8'
      controller.currentTenant.name = 'Foobar Inc.'
      controller.currentTenant.tenant_code = 'barfoo_company'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'barfoo_company'
