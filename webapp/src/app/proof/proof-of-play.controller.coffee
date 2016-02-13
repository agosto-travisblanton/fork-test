'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", (ProofPlayService) ->
  @tab = {title: "One-Resource"}
  @tab2 = {title: "Multi-Resource"}
  @chosen_tenant = null
  @tenants = null

  ProofPlayService.getAllTenants()
  .then (data) =>
    @tenants = data.data.tenants



  @submitTenant = (tenant) =>
    ProofPlayService.setTenant(tenant)
    @chosen_tenant = (tenant)


  @
