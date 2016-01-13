'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "TenantsCtrl", ($state, $log, TenantsService, sweet) ->
  @tenants = []

  @initialize = ->
    promise = TenantsService.fetchAllTenants()
    promise.then (data) =>
      @tenants = data

  @editItem = (item) ->
    $state.go 'editTenant', {tenantKey: item.key}

  @deleteItem = (item) =>
    callback = () =>
      promise = TenantsService.delete item
      promise.then () =>
        @initialize()
    sweet.show({
      title: "Are you sure?",
      text: "This will permanently remove the tenant from the system.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, remove the tenant!",
      closeOnConfirm: true
    }, callback)

  @
