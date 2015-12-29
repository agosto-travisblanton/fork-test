'use strict'

describe 'DomainsService', ->
  DomainsService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skyKitProvisioning')

  beforeEach inject (_DomainsService_, _Restangular_) ->
    DomainsService = _DomainsService_
    Restangular = _Restangular_
    promise = new skyKitProvisioning.q.Mock

  describe '.save', ->
    it 'update an existing domain, returning a promise', ->
      domain = {
        key: 'kdfalkdsjfakjdf98ad87fa87df0'
        put: ->
      }
      spyOn(domain, 'put').and.returnValue promise
      actual = DomainsService.save domain
      expect(domain.put).toHaveBeenCalled()
      expect(actual).toBe promise

    it 'insert a new domain, returning a promise', ->
      domain = {name: 'bob.agosto.com'}
      domainRestangularService = { post: (domain) -> }
      spyOn(Restangular, 'service').and.returnValue domainRestangularService
      spyOn(domainRestangularService, 'post').and.returnValue promise
      actual = DomainsService.save domain
      expect(Restangular.service).toHaveBeenCalledWith 'domains'
      expect(domainRestangularService.post).toHaveBeenCalledWith domain
      expect(actual).toBe promise

  describe '.fetchAllDomains', ->
    it 'retrieve all domains, returning a promise', ->
      domainRestangularService = { getList: -> }
      spyOn(Restangular, 'all').and.returnValue domainRestangularService
      spyOn(domainRestangularService, 'getList').and.returnValue promise
      actual = DomainsService.fetchAllDomains()
      expect(Restangular.all).toHaveBeenCalledWith 'domains'
      expect(domainRestangularService.getList).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getDomainByKey', ->
    it 'retrieve domain by key, returning a promise', ->
      domainKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67'
      domainRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue domainRestangularService
      spyOn(domainRestangularService, 'get').and.returnValue promise
      actual = DomainsService.getDomainByKey domainKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'domains', "api/v1/domains/#{domainKey}"
      expect(domainRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.delete', ->
    it 'delete domain, returning a promise', ->
      domain = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'dev.agosto.com'}
      domainRestangularService = { remove: -> }
      spyOn(Restangular, 'one').and.returnValue domainRestangularService
      spyOn(domainRestangularService, 'remove').and.returnValue promise
      actual = DomainsService.delete domain
      expect(Restangular.one).toHaveBeenCalledWith 'domains', domain.key
      expect(domainRestangularService.remove).toHaveBeenCalled()
      expect(actual).toBe promise
