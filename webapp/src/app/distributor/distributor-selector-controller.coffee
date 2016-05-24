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
  ToastsService) ->
# I don't know how to fix the errors in the style guide here
  @distributors = []
  @currentDistributor = undefined
  @loading = true

  @initialize = ->
    @loading = true
    distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.getUserKey())
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

    SessionsService.setCurrentDistributorName @currentDistributor.name
    SessionsService.setCurrentDistributorKey @currentDistributor.key

    if not @distributors.length == 1
      ToastsService.showSuccessToast "Distributor #{distributor.name} selected!"
    $state.go 'welcome'

  @
