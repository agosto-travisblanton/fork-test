'use strict'

skykitDisplayDeviceManagement = angular.module "skykitDisplayDeviceManagement"

skykitDisplayDeviceManagement.controller "TenantDetailsCtrl", ($scope, $log, $state, $stateParams, TenantsService) ->
  @currentTenant = {key: undefined, name: undefined}
  @editMode = !!$stateParams.tenantKey

  if @editMode
    promise = TenantsService.getTenantByKey($stateParams.tenantKey)
    promise.then (data) =>
      @currentTenant = data

  @onClickSaveButton = () ->
    promise = TenantsService.save @currentTenant
    promise.then (data) =>
      $state.go 'tenants'

  @
