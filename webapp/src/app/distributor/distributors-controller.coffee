'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "DistributorsCtrl", ($state) ->
  @distributors = []

  @initialize = ->
#    promise = TenantsService.fetchAllTenants()
#    promise.then (data) =>
#      @tenants = data

#  @editItem = (item) ->
#    $state.go 'editTenant', {tenantKey: item.key}
#
#  @deleteItem = (item) =>
#    promise = TenantsService.delete item
#    promise.then () =>
#      @initialize()

  @
