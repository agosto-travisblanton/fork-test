'use strict'

skykitDisplayDeviceManagement = angular.module "skykitDisplayDeviceManagement"

skykitDisplayDeviceManagement.controller "TenantDetailsCtrl", ($scope, $log, sweet, TenantsService) ->
  @currentTenant = {tenant: {name: undefined}}

  @onClickSaveButton = () ->
    promise = TenantsService.createTenant @currentTenant
    promise.then (data) ->
      sweet.show 'Sweet Jebus', 'You\'ve done it!', 'success'


  @
