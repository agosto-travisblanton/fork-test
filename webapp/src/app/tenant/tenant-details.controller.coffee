'use strict'

skykitDisplayDeviceManagement = angular.module "skykitDisplayDeviceManagement"

skykitDisplayDeviceManagement.controller "TenantDetailsCtrl", ($scope, $log, $state, TenantsService) ->
  @currentTenant = {tenant: {name: undefined}}

  @onClickSaveButton = () ->
    promise = TenantsService.createTenant @currentTenant
    promise.then (data) ->
      $state.go 'tenants'

  @
