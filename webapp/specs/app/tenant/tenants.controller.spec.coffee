'use strict'

describe 'TenantsCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  TenantsService = undefined
  promise = undefined
  ProgressBarService = undefined
  sweet = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _TenantsService_, _$state_, _ProgressBarService_, _sweet_) ->
    $controller = _$controller_
    $state = _$state_
    TenantsService = _TenantsService_
    ProgressBarService = _ProgressBarService_
    sweet = _sweet_
    controller = $controller 'TenantsCtrl', {$state: $state, TenantsService: TenantsService, ProgressBarService: ProgressBarService, sweet: sweet, }

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
      promise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'fetchAllTenants').and.returnValue promise
      spyOn(ProgressBarService, 'start')
      spyOn(ProgressBarService, 'complete')

    it 'call TenantsService.fetchAllTenants to retrieve all tenants', ->
      controller.initialize()
      promise.resolve tenants
      expect(TenantsService.fetchAllTenants).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved tenants in the controller", ->
      controller.initialize()
      promise.resolve tenants
      expect(controller.tenants).toBe tenants

  describe '.getFetchSuccess', ->
    beforeEach ->
      spyOn(ProgressBarService, 'complete')

    it 'stops the progress bar', ->
      controller.getFetchSuccess()
      expect(ProgressBarService.complete).toHaveBeenCalled()

  describe '.getFetchFailure', ->
    response = {status: 400, statusText: 'Bad request'}
    beforeEach ->
      spyOn(ProgressBarService, 'complete')
      spyOn(sweet, 'show')

    it 'stops the progress bar', ->
      controller.getFetchFailure response
      expect(ProgressBarService.complete).toHaveBeenCalled()

    it 'calls seet alert with error', ->
      controller.getFetchFailure response
      expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to fetch tenants. Error: 400 Bad request.', 'error')


  describe '.editItem', ->
    tenant = {key: 'dhjad897d987fadafg708hb55'}

    beforeEach ->
      spyOn $state, 'go'

    it "route to the 'tenantDetails' named route, passing the supplied tenant key", ->
      controller.editItem(tenant)
      expect($state.go).toHaveBeenCalledWith 'tenantDetails', {tenantKey: tenant.key}

  describe '.deleteItem', ->
    tenant = {
      key: 'dhjad897d987fadafg708fg7d'
      name: 'Foobar3'
      created: '2015-05-10 22:15:10'
      updated: '2015-05-10 22:15:10'
    }

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'delete').and.returnValue promise
      spyOn controller, 'initialize'
      spyOn(sweet, 'show').and.callFake (options, callback) ->
        callback()

    it 'call TenantsService.delete tenant', ->
      controller.deleteItem tenant
      promise.resolve()
      expect(TenantsService.delete).toHaveBeenCalledWith tenant

    it "the 'then' handler calls initialize to re-fetch all tenants", ->
      controller.deleteItem tenant
      promise.resolve()
      expect(controller.initialize).toHaveBeenCalled

    it "the SweetAlert confirmation should be shown", ->
      controller.deleteItem tenant
      promise.resolve()
      expect(sweet.show).toHaveBeenCalled

