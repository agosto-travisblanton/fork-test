'use strict'

appModule = angular.module('skykitProvisioning')

appModule.factory 'DistributorsService', (Restangular,
  $state,
  SessionsService,
  ProofPlayService,
  TenantsService,
  DevicesService) ->
    new class DistributorsService
      constructor: ->
        @DISTRIBUTOR_SERVICE = 'distributors'

      save: (tenant) ->
        if tenant.key != undefined
          promise = tenant.put()
        else
          promise = Restangular.service(@DISTRIBUTOR_SERVICE).post(tenant)
        promise

      fetchAll: () ->
        promise = Restangular.all(@DISTRIBUTOR_SERVICE).getList()
        promise

      fetchAllByUser: (userKey) ->
        if userKey
          promise = Restangular.one('users', userKey).doGET(@DISTRIBUTOR_SERVICE)
          promise

      getByKey: (key) ->
        promise = Restangular.oneUrl(@DISTRIBUTOR_SERVICE, "api/v1/distributors/#{key}").get()
        promise

      delete: (entity) ->
        if entity.key
          promise = Restangular.one(@DISTRIBUTOR_SERVICE, entity.key).remove()
          promise

      getByName: (name) ->
        promise = Restangular.all(@DISTRIBUTOR_SERVICE).getList distributorName: name
        promise

      getDomainsByKey: (key) ->
        promise = Restangular.oneUrl(@DISTRIBUTOR_SERVICE, "api/v1/distributors/#{key}/domains").get()
        promise

      switchDistributor: (distributor) ->
        ProofPlayService.proofplayCache.removeAll()
        TenantsService.tenantCache.removeAll()
        DevicesService.deviceCache.removeAll()
        DevicesService.deviceByTenantCache.removeAll()

        SessionsService.setCurrentDistributorName distributor.name
        SessionsService.setCurrentDistributorKey distributor.key

        $state.go 'welcome'
