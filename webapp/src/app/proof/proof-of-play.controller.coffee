'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", (ProofPlayService, $stateParams, $state, ToastsService) ->
  vm = @
  vm.resource = {title: "Resource Report"}
  vm.location = {title: "Location Report"}
  vm.display = {title: "Display Report"}

  vm.chosen_tenant = null
  vm.tenants = null
  vm.disabled = true


  vm.initialize = () ->
    ProofPlayService.getAllTenants()
    .then (data) ->
      vm.tenants = data.data.tenants

  vm.querySearch = (resources, searchText) ->
    ProofPlayService.querySearch(resources, searchText)

      
  vm.isSelectionValid = (search) ->
    if search in vm.tenants
      vm.disabled = false
    else
      vm.disabled = true


  vm.submitTenant = (tenant) ->
    if tenant
      vm.chosen_tenant = (tenant)
      $state.go 'proofDetail', {
        tenant: vm.chosen_tenant
      }
      
  vm.refreshTenants = () ->
    vm.tenants = null
    url = ProofPlayService.makeHTTPURL "/retrieve_my_tenants", ''
    ProofPlayService.proofplayCache.remove(url)
    vm.initialize()


  vm
