'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'TenantsService', ($log, Restangular) ->

  class TenantsService

    createTenant: (tenant) ->
      promise = Restangular.service('tenants').post(tenant)
      promise

  new TenantsService()
