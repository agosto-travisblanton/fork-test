'use strict'

describe 'LocationsService', ->
  LocationsService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_LocationsService_, _Restangular_) ->
    LocationsService = _LocationsService_
    Restangular = _Restangular_
    promise = new skykitProvisioning.q.Mock

  describe '.save', ->
    it 'updates an existing location, returning a promise', ->
      location = {
        key: 'kdfalkdsjfakjdf98ad87fa87df0'
        put: ->
      }
      spyOn(location, 'put').and.returnValue promise
      actual = LocationsService.save location
      expect(location.put).toHaveBeenCalled()
      expect(actual).toBe promise

    it 'inserts a new location, returning a promise', ->
      location = {customerLocationName: 'Back of the store'}
      locationRestangularService = { post: (location) -> }
      spyOn(Restangular, 'service').and.returnValue locationRestangularService
      spyOn(locationRestangularService, 'post').and.returnValue promise
      actual = LocationsService.save location
      expect(Restangular.service).toHaveBeenCalledWith 'locations'
      expect(locationRestangularService.post).toHaveBeenCalledWith location
      expect(actual).toBe promise

  describe '.getLocationsByTenantKey', ->
    it 'retrieve locations by tenant key, returning a promise', ->
      tenantKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67'
      locationRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue locationRestangularService
      spyOn(locationRestangularService, 'get').and.returnValue promise
      actual = LocationsService.getLocationsByTenantKey tenantKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'tenants', "api/v1/tenants/#{tenantKey}/locations"
      expect(locationRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getLocationByKey', ->
    it 'retrieve location by location key, returning a promise', ->
      locationKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67'
      locationRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue locationRestangularService
      spyOn(locationRestangularService, 'get').and.returnValue promise
      actual = LocationsService.getLocationByKey locationKey
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'locations', "api/v1/locations/#{locationKey}"
      expect(locationRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.getTimezones', ->
    it 'retrieve list of timezones, returning a promise', ->
      locationRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue locationRestangularService
      spyOn(locationRestangularService, 'get').and.returnValue promise
      actual = LocationsService.getTimezones promise
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'timezones', 'api/v1/timezones'
      expect(locationRestangularService.get).toHaveBeenCalled()
      expect(actual).toBe promise
