'use strict'

describe 'VersionService', ->
  VersionService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_VersionService_, _Restangular_) ->
    VersionService = _VersionService_
    Restangular = _Restangular_
    promise = new skykitDisplayDeviceManagement.q.Mock

  describe '.getVersion', ->
    versionRestangularService = undefined
    result = undefined

    beforeEach ->
      versionRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue versionRestangularService
      spyOn(versionRestangularService, 'get').and.returnValue promise
      result = VersionService.getVersion()

    it 'obtains Restangular service for version', ->
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'version'

    it 'obtains the version from the Restangular service', ->
      expect(versionRestangularService.get).toHaveBeenCalled()

    it 'returns a promise', ->
      expect(result).toBe promise

