'use strict'

describe 'IdentityService', ->
  IdentityService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_IdentityService_, _Restangular_) ->
    IdentityService = _IdentityService_
    Restangular = _Restangular_
    promise = new skykitProvisioning.q.Mock

  describe '.getIdentity', ->
    identityRestangularService = undefined
    result = undefined

    beforeEach ->
      identityRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue identityRestangularService
      spyOn(identityRestangularService, 'get').and.returnValue promise
      result = IdentityService.getIdentity()

    it 'obtains Restangular service for identity', ->
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'identity'

    it 'obtains the identity from the Restangular service', ->
      expect(identityRestangularService.get).toHaveBeenCalled()

    it 'returns a promise', ->
      expect(result).toBe promise

