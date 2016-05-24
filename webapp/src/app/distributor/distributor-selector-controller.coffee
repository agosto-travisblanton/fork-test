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
  vm = @
  vm.distributors = []
  vm.currentDistributor = undefined
  vm.loading = true

  vm.initialize = ->
    vm.loading = true
    distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.getUserKey())
    distributorsPromise.then (data) ->
      vm.distributors = data
      if vm.distributors.length == 1
        vm.selectDistributor(vm.distributors[0])
      else
        vm.loading = false


  vm.selectDistributor = (distributor) ->
    ProofPlayService.proofplayCache.removeAll()
    TenantsService.tenantCache.removeAll()
    DevicesService.deviceCache.removeAll()
    DevicesService.deviceByTenantCache.removeAll()
    vm.currentDistributor = distributor

    SessionsService.setCurrentDistributorName vm.currentDistributor.name
    SessionsService.setCurrentDistributorKey vm.currentDistributor.key

    if not vm.distributors.length == 1
      ToastsService.showSuccessToast "Distributor #{distributor.name} selected!"
    $state.go 'welcome'

  vm
