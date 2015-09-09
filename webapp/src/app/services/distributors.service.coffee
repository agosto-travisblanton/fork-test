'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'DistributorsService', (Restangular) ->

  class DistributorsService
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

    getByKey: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "distributors/#{key}").get()
      promise

    delete: (entity) ->
      if entity.key
        promise = Restangular.one(SERVICE_NAME, entity.key).remove()
        promise

    getByName: (name) ->
      promise = Restangular.all(SERVICE_NAME).getList distributorName: name
      promise

  new DistributorsService()
