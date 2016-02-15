'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", (ProofPlayService) ->
  @resource = {title: "Resource"}
  @chosen_tenant = null
  @tenants = null

  ProofPlayService.getAllTenants()
  .then (data) =>
    @tenants = data.data.tenants



  @submitTenant = (tenant) =>
    ProofPlayService.setTenant(tenant)
    @chosen_tenant = (tenant)


  @
