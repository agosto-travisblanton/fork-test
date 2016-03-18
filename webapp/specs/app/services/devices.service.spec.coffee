'use strict'

describe 'DevicesService', ->
  DevicesService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_DevicesService_, _Restangular_) ->
    DevicesService = _DevicesService_
    Restangular = _Restangular_
    promise = new skykitProvisioning.q.Mock

  describe '.getDevicesByTenant', ->
    it 'retrieve all devices associated to a tenant, returning a promise', ->
      restangularServiceStub = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'get').and.returnValue promise
      tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud'
      actual = DevicesService.getDevicesByTenant tenantKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/tenants/#{tenantKey}/devices?unmanaged=false"
      expect(actual).toBe promise

  describe '.getUnmanagedDevicesByTenant', ->
    it 'retrieve all unmanaged devices associated to a tenant, returning a promise', ->
      restangularServiceStub = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'get').and.returnValue promise
      tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud'
      actual = DevicesService.getUnmanagedDevicesByTenant tenantKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/tenants/#{tenantKey}/devices?unmanaged=true"
      expect(actual).toBe promise

  describe '.getDevicesByDistributor', ->
    it 'retrieve all devices associated with a distributor, returning a promise', ->
      restangularServiceStub = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'get').and.returnValue promise
      distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud'
      actual = DevicesService.getDevicesByDistributor distributorKey, null, null
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices',
        "api/v1/distributors/null/null/#{distributorKey}/devices?unmanaged=false")
      expect(actual).toBe promise

  describe '.getUnmanagedDevicesByDistributor', ->
    it 'retrieve all unmanaged devices associated with a distributor, returning a promise', ->
      restangularServiceStub = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'get').and.returnValue promise
      distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud'
      actual = DevicesService.getUnmanagedDevicesByDistributor distributorKey, null, null
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices',
        "api/v1/distributors/null/null/#{distributorKey}/devices?unmanaged=true")
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

  describe '.getIssuesByKey', ->
    it 'retrieve issues associated with supplied key, returning a promise', ->
      now = new Date()
      epochEnd = moment(now).unix()
      now.setDate(now.getDate() - 1)
      epochStart = moment(now).unix()
      expect(epochEnd).toBeGreaterThan(epochStart);
      deviceKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw'
      deviceRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue deviceRestangularService
      spyOn(deviceRestangularService, 'get').and.returnValue promise
      actual = DevicesService.getIssuesByKey(deviceKey, epochStart, epochEnd)
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices',
        "api/v1/devices/#{deviceKey}/issues?start=#{epochStart}&end=#{epochEnd}"
      expect(deviceRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getCommandEventsByKey', ->
    it 'retrieve command events associated with supplied key, returning a promise', ->
      deviceKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw'
      deviceRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue deviceRestangularService
      spyOn(deviceRestangularService, 'get').and.returnValue promise
      actual = DevicesService.getCommandEventsByKey(deviceKey)
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices',"/api/v1/player-command-events/#{deviceKey}"
      expect(deviceRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise


  describe '.searchDevicesByPartialMac', ->
    it 'search devices with a partial mac address returns an http promise', ->
      distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw'
      partialMac = "1234"
      unmanaged = false
      deviceRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue deviceRestangularService
      spyOn(deviceRestangularService, 'get').and.returnValue promise
      actual = DevicesService.searchDevicesByPartialMac(distributorKey, partialMac, unmanaged)
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices',"api/v1/distributors/search/mac/#{distributorKey}/#{partialMac}/#{unmanaged}/devices"
      expect(deviceRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.searchDevicesByPartialSerial', ->
    it 'search devices with a partial mac address returns an http promise', ->
      distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw'
      partialMac = "1234"
      unmanaged = false
      deviceRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue deviceRestangularService
      spyOn(deviceRestangularService, 'get').and.returnValue promise
      actual = DevicesService.searchDevicesByPartialSerial(distributorKey, partialMac, unmanaged)
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices',"api/v1/distributors/search/serial/#{distributorKey}/#{partialMac}/#{unmanaged}/devices"
      expect(deviceRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise
