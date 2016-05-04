'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", (ProofPlayService, $stateParams, $state, ToastsService) ->
  @resource = {title: "Resource Report"}
  @location = {title: "Location Report"}
  @display = {title: "Display Report"}

  @chosen_tenant = null
  @tenants = null
  @disabled = true


  @initialize = () ->
    ProofPlayService.getAllTenants()
    .then (data) =>
      @tenants = data.data.tenants

  @querySearch = (resources, searchText) ->
    ProofPlayService.querySearch(resources, searchText)

      
  @isSelectionValid = (search) =>
    if search in @tenants
      @disabled = false
    else
      @disabled = true


  @submitTenant = (tenant) =>
    if tenant
      @chosen_tenant = (tenant)
      $state.go 'proofDetail', {
        tenant: @chosen_tenant
      }
      
  @refreshTenants = () =>
    @tenants = null
    url = ProofPlayService.makeHTTPURL "/retrieve_my_tenants", ''
    ProofPlayService.proofplayCache.remove(url)
    @initialize()


  @
