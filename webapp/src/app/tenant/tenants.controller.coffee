'use strict'

skykitDisplayDeviceManagement = angular.module "skykitDisplayDeviceManagement"

skykitDisplayDeviceManagement.controller "TenantsCtrl", ($scope, $log, sweet, TenantsService) ->
#  TODO Wire up TenantsService to call backend for list of tenants ie., getAllTenants
  @tenants = [
  ]

  $scope.tenant_list = @tenants

#  $scope.editItem = (item) ->
#    $rootScope.item = item
#    return
#
#
#  promise = TenantsService.getAllTenants()



  @
