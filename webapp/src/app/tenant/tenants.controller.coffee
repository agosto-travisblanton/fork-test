'use strict'

skykitDisplayDeviceManagement = angular.module "skykitDisplayDeviceManagement"

skykitDisplayDeviceManagement.controller "TenantsCtrl", ($scope, $log, $state, TenantsService) ->
  @tenants = []

  @initialize = () ->
    promise = TenantsService.fetchAllTenants()
    promise.then (data) =>
      @tenants = data
#      $scope.$apply()

  @editItem = (item) ->
    $state.go( 'editTenant', { tenantKey: item.key } )

  @
