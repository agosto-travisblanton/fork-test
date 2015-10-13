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
      restangularServiceStub = {doGET: ->}
      spyOn(Restangular, 'one').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'doGET').and.returnValue promise
      tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFudEVudGl0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      actual = DevicesService.getDevicesByTenant(tenantKey)
      expect(Restangular.one).toHaveBeenCalledWith 'tenants', tenantKey
      expect(restangularServiceStub.doGET).toHaveBeenCalledWith 'devices'
      expect(actual).toBe promise

  describe '.getDevicesByDistributor', ->
    it 'retrieve all devices associated with a distributor, returning a promise', ->
      restangularServiceStub = {doGET: ->}
      spyOn(Restangular, 'one').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'doGET').and.returnValue promise
      distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFudEVudGl0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      actual = DevicesService.getDevicesByDistributor(distributorKey)
      expect(Restangular.one).toHaveBeenCalledWith 'distributors', distributorKey
      expect(restangularServiceStub.doGET).toHaveBeenCalledWith 'devices'
      expect(actual).toBe promise

  describe '.getDeviceByKey', ->
    it 'retrieve device associated with supplied key, returning a promise', ->
      deviceKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFudEVudGl0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      deviceRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue deviceRestangularService
      spyOn(deviceRestangularService, 'get').and.returnValue promise
      actual = DevicesService.getDeviceByKey deviceKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{deviceKey}"
      expect(deviceRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getDevices', ->
    it 'retrieve all devices, returning a promise', ->
      deviceRestangularService = {getList: ->}
      spyOn(Restangular, 'all').and.returnValue deviceRestangularService
      spyOn(deviceRestangularService, 'getList').and.returnValue promise
      actual = DevicesService.getDevices()
      expect(Restangular.all).toHaveBeenCalledWith 'devices'
      parameters = {}
      expect(deviceRestangularService.getList).toHaveBeenCalled()
      expect(actual).toBe promise

