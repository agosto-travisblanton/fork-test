'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DistributorSelectorCtrl", (
  $log,
  $state,
  DistributorsService,
  SessionsService) ->
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
    DistributorsService.switchDistributor(distributor)
 
  vm
