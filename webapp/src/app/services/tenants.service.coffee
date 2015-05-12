'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'TenantsService', (Restangular) ->

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

    delete: (tenant) ->
      promise = Restangular.oneUrl('tenants', "api/v1/tenants/#{tenant.key}").remove()
      promise

  new TenantsService()
