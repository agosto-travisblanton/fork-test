'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "TenantsCtrl", ($state, $log, TenantsService, ProgressBarService, sweet) ->
  @tenants = []

  @initialize = ->
    ProgressBarService.start()
    promise = TenantsService.fetchAllTenants()
    promise.then ((response) =>
      @getFetchSuccess(response)
      return
    ), (response) =>
      @getFetchFailure(response)
      return

  @getFetchSuccess = (response) ->
    @tenants = response
    ProgressBarService.complete()

  @getFetchFailure = (response) ->
    ProgressBarService.complete()
    errorMessage = "Unable to fetch tenants. Error: #{response.status} #{response.statusText}."
    sweet.show('Oops...', errorMessage, 'error')

  @editItem = (item) ->
    $state.go 'tenantDetails', {tenantKey: item.key}

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
