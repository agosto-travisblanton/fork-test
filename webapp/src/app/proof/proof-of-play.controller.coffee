'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", (ProofPlayService, $stateParams, $state, ToastsService) ->
  
  @resource = {title: "Resource Report"}
  @location = {title: "Location Report"}
  @display = {title: "Display Report"}

  @chosen_tenant = null
  @tenants = null

  @initialize = () ->
    ProofPlayService.getAllTenants()
    .then (data) =>
      @tenants = data.data.tenants


  @submitTenant = (tenant) =>
    @chosen_tenant = (tenant)
    $state.go 'proofDetail', {
      tenant: @chosen_tenant
    }
    ToastsService.showSuccessToast "Proof of Play reporting set to " + tenant



  @
