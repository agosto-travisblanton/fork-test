'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'DistributorsService', (Restangular) ->

  class DistributorsService
    serviceName = 'distributors'

    save: (tenant) ->
      if tenant.key != undefined
        promise = tenant.put()
      else
        promise = Restangular.service(serviceName).post(tenant)
      promise

    fetchAllDistributors: () ->
      promise = Restangular.all(serviceName).getList()
      promise

    getByKey: (key) ->
      promise = Restangular.oneUrl(serviceName, "distributors/#{key}").get()
      promise

    delete: (entity) ->
      if entity.key
        promise = Restangular.one(serviceName, entity.key).remove()
        promise

  new DistributorsService()
