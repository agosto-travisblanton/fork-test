'use strict'

describe 'TenantsService', ->
  TenantsService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_TenantsService_, _Restangular_) ->
    TenantsService = _TenantsService_
    Restangular = _Restangular_
    promise = new skykitDisplayDeviceManagement.q.Mock

  describe '.save', ->
    it 'update an existing tenant, returning a promise', ->
      tenant = {
        key: 'kdfalkdsjfakjdf98ad87fa87df0'
        put: ->
      }
      spyOn(tenant, 'put').and.returnValue promise
      actual = TenantsService.save tenant
      expect(tenant.put).toHaveBeenCalled()
      expect(actual).toBe promise

    it 'insert a new tenant, returning a promise', ->
      tenant = {name: 'Foobar'}
      tenantRestangularService = { post: (tenant) -> }
      spyOn(Restangular, 'service').and.returnValue tenantRestangularService
      spyOn(tenantRestangularService, 'post').and.returnValue promise
      actual = TenantsService.save tenant
      expect(Restangular.service).toHaveBeenCalledWith 'tenants'
      expect(tenantRestangularService.post).toHaveBeenCalledWith tenant
      expect(actual).toBe promise

  describe '.fetchAllTenants', ->
    it 'retrieve all tenants, returning a promise', ->
      tenantRestangularService = { getList: -> }
      spyOn(Restangular, 'all').and.returnValue tenantRestangularService
      spyOn(tenantRestangularService, 'getList').and.returnValue promise
      actual = TenantsService.fetchAllTenants()
      expect(Restangular.all).toHaveBeenCalledWith 'tenants'
      expect(tenantRestangularService.getList).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getTenantByKey', ->
    it 'retrieve tenant by key, returning a promise', ->
      tenantKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67'
      tenantRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue tenantRestangularService
      spyOn(tenantRestangularService, 'get').and.returnValue promise
      actual = TenantsService.getTenantByKey tenantKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'tenants', "api/v1/tenants/#{tenantKey}"
      expect(tenantRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.delete', ->
    it 'delete tenant, returning a promise', ->
      tenant = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'Foobar'}
      tenantRestangularService = { remove: -> }
      spyOn(Restangular, 'one').and.returnValue tenantRestangularService
      spyOn(tenantRestangularService, 'remove').and.returnValue promise
      actual = TenantsService.delete tenant
      expect(Restangular.one).toHaveBeenCalledWith 'tenants', tenant.key
      expect(tenantRestangularService.remove).toHaveBeenCalled()
      expect(actual).toBe promise
