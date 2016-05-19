'use strict'

describe 'TimezonesService', ->
  TimezonesService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_TimezonesService_, _Restangular_) ->
    TimezonesService = _TimezonesService_
    Restangular = _Restangular_
    promise = new skykitProvisioning.q.Mock

  describe '.getTimezones', ->
    it 'retrieve list of timezones, returning a promise', ->
      timezonesRestangularService = {get: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue timezonesRestangularService
      spyOn(timezonesRestangularService, 'get').and.returnValue promise
      actual = TimezonesService.getUsTimezones promise
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'timezones', 'api/v1/timezones/us'
      expect(timezonesRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise
