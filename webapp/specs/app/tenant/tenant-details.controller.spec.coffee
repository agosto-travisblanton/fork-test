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
