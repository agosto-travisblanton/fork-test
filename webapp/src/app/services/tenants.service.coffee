'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'TenantsService', ($log, Restangular) ->

  class TenantsService

    save: (tenant) ->
      if tenant.key != undefined
        promise = tenant.put()
      else
        promise = Restangular.service('tenants').post(tenant)
      promise

    fetchAllTenants: () ->
      promise = Restangular.all('tenants').getList()
      promise

    getTenantByKey: (tenantKey) ->
      promise = Restangular.oneUrl('tenants', "api/v1/tenants/#{tenantKey}").get()
      promise

  new TenantsService()
