'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'DistributorsService', (Restangular) ->

  class DistributorsService

    save: (tenant) ->
      if tenant.key != undefined
        promise = tenant.put()
      else
        promise = Restangular.service('distributors').post(tenant)
      promise

    fetchAllDistributors: () ->
      promise = Restangular.all('distributors').getList()
      promise

    getTenantByKey: (distributorKey) ->
      promise = Restangular.oneUrl('distributors', "api/v1/distributors/#{distributorKey}").get()
      promise

    delete: (tenant) ->
      if tenant.key != undefined
        promise = Restangular.one('distributors', tenant.key).remove()
        promise

  new DistributorsService()
