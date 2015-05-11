'use strict'

skykitDisplayDeviceManagement = angular.module "skykitDisplayDeviceManagement"

skykitDisplayDeviceManagement.controller "TenantDetailsCtrl", ($scope, $log, $state, $stateParams, TenantsService) ->
  @currentTenant = {tenant: {name: undefined}}
  @editMode = !!$stateParams.tenantKey

  if @editMode
    @currentTenant = {tenant: {name: 'foo', key: '32343234'}} #TenantsService.getTenantByKey($stateParams.tenantKey)

  @onClickSaveButton = () ->
    promise = TenantsService.createTenant @currentTenant
    promise.then (data) ->
      $state.go 'tenants'

  @
