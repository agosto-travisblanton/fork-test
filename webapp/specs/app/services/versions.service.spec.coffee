'use strict'

describe 'VersionsService', ->
  VersionsService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_VersionsService_, _Restangular_) ->
    VersionsService = _VersionsService_
    Restangular = _Restangular_
    promise = new skykitDisplayDeviceManagement.q.Mock

  describe '.getVersions', ->
    versionsRestangularService = undefined
    result = undefined

    beforeEach ->
      versionsRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue versionsRestangularService
      spyOn(versionsRestangularService, 'get').and.returnValue promise
      result = VersionsService.getVersions()

    it 'obtains Restangular service for version', ->
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'versions'

    it 'obtains the versions from the Restangular service', ->
      expect(versionsRestangularService.get).toHaveBeenCalled()

    it 'returns a promise', ->
      expect(result).toBe promise

