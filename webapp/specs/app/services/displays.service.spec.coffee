'use strict'

describe 'DisplaysService', ->
  DisplaysService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_DisplaysService_, _Restangular_) ->
    DisplaysService = _DisplaysService_
    Restangular = _Restangular_
    promise = new skykitDisplayDeviceManagement.q.Mock

  describe '.getDisplaysByTenant', ->
    it 'retrieve all displays associated to a tenant, returning a promise', ->
      restangularServiceStub = { doGET: -> }
      spyOn(Restangular, 'one').and.returnValue restangularServiceStub
      spyOn(restangularServiceStub, 'doGET').and.returnValue promise
      tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFudEVudGl0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      actual = DisplaysService.getDisplaysByTenant(tenantKey)
      expect(Restangular.one).toHaveBeenCalledWith 'tenants', tenantKey
      expect(restangularServiceStub.doGET).toHaveBeenCalledWith 'displays'
      expect(actual).toBe promise

  describe '.getByKey', ->
    it 'retrieve display associated with supplied key, returning a promise', ->
      displayKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFudEVudGl0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      displayRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue displayRestangularService
      spyOn(displayRestangularService, 'get').and.returnValue promise
      actual = DisplaysService.getByKey displayKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'displays', "api/v1/displays/#{displayKey}"
      expect(displayRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getByMacAddress', ->
    it 'retrieve display associated with supplied MAC address, returning a promise', ->
      macAddress = '0LWRpc3BsYXk'
      displayRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue displayRestangularService
      spyOn(displayRestangularService, 'get').and.returnValue promise
      actual = DisplaysService.getByMacAddress macAddress
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'api/v1/displays', "api/v1/displays?mac_address=#{macAddress}"
      expect(displayRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getDisplays', ->
    it 'retrieve all displays, returning a promise', ->
      displayRestangularService = { getList: -> }
      spyOn(Restangular, 'all').and.returnValue displayRestangularService
      spyOn(displayRestangularService, 'getList').and.returnValue promise
      actual = DisplaysService.getDisplays()
      expect(Restangular.all).toHaveBeenCalledWith 'displays'
      parameters = {}
      expect(displayRestangularService.getList).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.save', ->
    it 'update an existing display, returning a promise', ->
      display = {
        key: 'kdfalkdsjfakjdf98ad87fa87df0'
        put: ->
      }
      spyOn(display, 'put').and.returnValue promise
      actual = DisplaysService.save display
      expect(display.put).toHaveBeenCalled()
      expect(actual).toBe promise

    it 'insert a new tenant, returning a promise', ->
      display = {name: 'Foobar'}
      displayRestangularService = { post: (tenant) -> }
      spyOn(Restangular, 'service').and.returnValue displayRestangularService
      spyOn(displayRestangularService, 'post').and.returnValue promise
      actual = DisplaysService.save display
      expect(Restangular.service).toHaveBeenCalledWith 'displays'
      expect(displayRestangularService.post).toHaveBeenCalledWith display
      expect(actual).toBe promise

