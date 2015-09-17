'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'DistributorsService', (Restangular) ->
  new class DistributorsService
    SERVICE_NAME = 'distributors'
    @currentDistributor = undefined

    save: (tenant) ->
      if tenant.key != undefined
        promise = tenant.put()
      else
        promise = Restangular.service(SERVICE_NAME).post(tenant)
      promise

    fetchAll: () ->
      promise = Restangular.all(SERVICE_NAME).getList()
      promise

    fetchAllByUser: (userKey) ->
      if userKey
        promise = Restangular.one('users', userKey).doGET(SERVICE_NAME)
        promise

    getByKey: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/distributors/#{key}").get()
      promise

    delete: (entity) ->
      if entity.key
        promise = Restangular.one(SERVICE_NAME, entity.key).remove()
        promise

    getByName: (name) ->
      promise = Restangular.all(SERVICE_NAME).getList distributorName: name
      promise

    getDomainsByKey: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/distributors/#{key}/domains").get()
      promise
