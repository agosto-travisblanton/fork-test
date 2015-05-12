'use strict'

describe 'TenantsCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  TenantsService = undefined
  promise = undefined


  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _TenantsService_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    TenantsService = _TenantsService_
    controller = $controller 'TenantsCtrl', {$state: $state, TenantsService: TenantsService}

  describe 'initialization', ->
    it 'tenants should be an empty array', ->
      expect(angular.isArray(controller.tenants)).toBeTruthy()

  describe '.initialize', ->
    tenants = [
      {key: 'dhjad897d987fadafg708fg7d', name: 'Foobar1', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'dhjad897d987fadafg708y67d', name: 'Foobar2', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'dhjad897d987fadafg708hb55', name: 'Foobar3', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'fetchAllTenants').and.returnValue promise

    it 'call TenantsService.fetchAllTenants to retrieve all tenants', ->
      controller.initialize()
      promise.resolve tenants
      expect(TenantsService.fetchAllTenants).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved tenants in the controller", ->
      controller.initialize()
      promise.resolve tenants
      expect(controller.tenants).toBe tenants

  describe '.editItem', ->
    tenant = {key: 'dhjad897d987fadafg708hb55'}

    beforeEach ->
      spyOn $state, 'go'

    it "route to the 'editTenant' named route, passing the supplied tenant key", ->
      controller.editItem(tenant)
      expect($state.go).toHaveBeenCalledWith 'editTenant', {tenantKey: tenant.key}

  describe '.deleteItem', ->
    tenant = {
      key: 'dhjad897d987fadafg708fg7d'
      name: 'Foobar3'
      created: '2015-05-10 22:15:10'
      updated: '2015-05-10 22:15:10'
    }

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'delete').and.returnValue promise
      spyOn $state, 'go'

    it 'call TenantsService.delete to retrieve all tenants', ->
      controller.deleteItem tenant
      promise.resolve()
      expect(TenantsService.delete).toHaveBeenCalledWith tenant.key

    it "the 'then' handler caches the retrieved tenants in the controller", ->
      controller.deleteItem tenant
      promise.resolve()
      expect($state.go).toHaveBeenCalledWith 'tenants'
