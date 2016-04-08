'use strict'

appModule = angular.module('skykitProvisioning')

appModule.factory 'LocationsService', (Restangular) ->

  class LocationsService

    save: (location) ->
      if location.key != undefined
        promise = location.put()
      else
        promise = Restangular.service('locations').post(location)
      promise

    getLocationsByTenantKey: (tenantKey) ->
      promise = Restangular.oneUrl('tenants', "api/v1/tenants/#{tenantKey}/locations").get()
      promise

    getLocationByKey: (locationKey) ->
      promise = Restangular.oneUrl('locations', "api/v1/locations/#{locationKey}").get()
      promise

  new LocationsService()
