'use strict'
appModule = angular.module('skykitProvisioning')
appModule.factory 'TenantsService', (Restangular) ->
  class TenantsService
    
    cache = {}

    save: (tenant) ->
      if tenant.key != undefined
        promise = tenant.put()
      else
        promise = Restangular.service('tenants').post(tenant)
      promise

    fetchAllTenants: () ->
      promise = Restangular.all('tenants').getList()
      promise

    fetchAllTenantsPaginated: (page_size, offset) ->
      promise = Restangular.oneUrl('tenants', "api/v1/tenants/paginated/#{page_size}/#{offset}").get()
      promise

    getTenantByKey: (tenantKey) ->
      promise = Restangular.oneUrl('tenants', "api/v1/tenants/#{tenantKey}").get()
      promise

    delete: (tenant) ->
      if tenant.key != undefined
        promise = Restangular.one("tenants", tenant.key).remove()
        promise
        
    cacheBust: () =>
      cache = {}

  new TenantsService()
