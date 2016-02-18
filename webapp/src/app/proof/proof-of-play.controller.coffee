'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", (ProofPlayService) ->
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
    ProofPlayService.setTenant(tenant)
    @chosen_tenant = (tenant)


  @
