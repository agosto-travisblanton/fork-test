'use strict'

skykitDisplayDeviceManagement = angular.module "skykitDisplayDeviceManagement"

skykitDisplayDeviceManagement.controller "TenantsCtrl", ($scope, $log, $state, TenantsService) ->
  @tenants = []

  @initialize = () ->
    promise = TenantsService.fetchAllTenants()
    promise.then (data) =>
      @tenants = data

  @editItem = (item) ->
    $state.go('editTenant', {tenantKey: item.key})

  @deleteItem = (item) ->
    promise = TenantsService.delete item
    promise.then () =>
      $state.go 'tenants'

  @
