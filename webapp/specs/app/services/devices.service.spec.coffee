'use strict'

describe 'DevicesService', ->
  DevicesService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_DevicesService_, _Restangular_) ->
    DevicesService = _DevicesService_
    Restangular = _Restangular_
    promise = new skykitDisplayDeviceManagement.q.Mock

  describe '.getDevicesByTenant', ->
    it 'retrieve all devices associated to a tenant, returning a promise', ->
      restangularServiceStub = { doGET: -> }
      spyOn(Restangular, 'one').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'doGET').and.returnValue promise
      tenant = {
        key: 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFudEVudGl0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      }
      actual = DevicesService.getDevicesByTenant(tenant)
      expect(Restangular.one).toHaveBeenCalledWith 'tenants', tenant.key
      expect(restangularServiceStub.doGET).toHaveBeenCalledWith 'devices'
      expect(actual).toBe promise

