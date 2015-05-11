'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'TenantsService', ($log, Restangular) ->

  class TenantsService

    createTenant: (tenant) ->
      promise = Restangular.service('tenants').post(tenant)
      promise

    fetchAllTenants: () ->
      promise = Restangular.all('tenants').getList()
      promise

    getTenantByKey: (tenantKey) ->
#      Restangular.oneUrl('api/v1/tenants', "api/v1/tenants?tenantKey=#{tenantKey}").get()

  new TenantsService()
