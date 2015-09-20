'use strict'

describe 'SessionsService', ->
  SessionsService = undefined
  Restangular = undefined
  $http = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_SessionsService_, _$http_, _Restangular_) ->
    SessionsService = _SessionsService_
    Restangular = _Restangular_
    $http = _$http_

  describe 'initialization', ->
    it 'sets @uriBase variable', ->
      expect(SessionsService.uriBase).toEqual 'v1/sessions'

    it 'sets @currentUserKey variable to undefined', ->
      expect(SessionsService.currentUserKey).toBeUndefined()

  describe '.getIdentity', ->
    identityRestangularService = undefined
    result = undefined

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      identityRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue identityRestangularService
      spyOn(identityRestangularService, 'get').and.returnValue promise
      result = SessionsService.getIdentity()

    it 'obtains Restangular service for devices', ->
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'api/v1/devices'

    it 'obtains the identity from the Restangular service', ->
      expect(identityRestangularService.get).toHaveBeenCalled()

    it 'returns a promise', ->
      expect(result).toBe promise
