'use strict'
appModule = angular.module('skykitProvisioning')
appModule.factory 'TenantsService', (Restangular, CacheFactory, $cookies) ->
  new class TenantsService
    
    constructor: ->
      if !CacheFactory.get('tenantCache')
        distributorKey = Lockr.get('currentDistributorKey')
        @tenantCache = CacheFactory('tenantCache',
          maxAge: 60 * 60 * 1000
          deleteOnExpire: 'aggressive'
          storageMode: 'localStorage'
          onExpire: (key, value) =>
            $http.get(key).success (data) =>
              @tenantCache.put key, data
              return
            return
        )

    
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
      url = "api/v1/tenants/paginated/#{page_size}/#{offset}"
      promise = Restangular.oneUrl('tenants', url).get()
      promise

    getTenantByKey: (tenantKey) ->
      url = "api/v1/tenants/#{tenantKey}"
      promise = Restangular.oneUrl('tenants', url).get()
      promise

    delete: (tenant) ->
      if tenant.key != undefined
        promise = Restangular.one("tenants", tenant.key).remove()
        promise


