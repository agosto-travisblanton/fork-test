'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DistributorSelectorCtrl", ($scope,
  $log,
  $state,
  DistributorsService,
  SessionsService,
  ProofPlayService,
  TenantsService,
  DevicesService,
  StorageService,
  ToastsService) ->
  # I don't know how to fix the errors in the style guide here
    @distributors = []
    @currentDistributor = undefined
    @loading = true

    @initialize = ->
      @loading = true
      distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.currentUserKey)
      distributorsPromise.then (data) =>
        @distributors = data
        if @distributors.length == 1
          @selectDistributor(@distributors[0])
        else
          @loading = false


    @selectDistributor = (distributor) =>
      ProofPlayService.proofplayCache.removeAll()
      TenantsService.tenantCache.removeAll()
      DevicesService.deviceCache.removeAll()
      DevicesService.deviceByTenantCache.removeAll()
      @currentDistributor = distributor
      DistributorsService.currentDistributor = @currentDistributor
      StorageService.set('currentDistributorName', @currentDistributor.name)
      StorageService.set('currentDistributorKey', @currentDistributor.key)
      if not @distributors.length == 1
        ToastsService.showSuccessToast "Distributor #{distributor.name} selected!"
      $state.go 'welcome'

    @
