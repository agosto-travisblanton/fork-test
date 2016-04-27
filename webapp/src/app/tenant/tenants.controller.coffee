'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "TenantsCtrl", ($state, $log, TenantsService, ProgressBarService, sweet) ->
  @tenants = []

  @getTenants = (page_size, offset) =>
    @offset = offset
    @loading = true
    ProgressBarService.start()
    promise = TenantsService.fetchAllTenantsPaginated(page_size, offset)
    promise.then ((response) =>
      @getFetchSuccess(response)
    ), (response) =>
      @getFetchFailure(response)

  @initialize = ->
    @offset = 0
    @getTenants(100, @offset)

  @getFetchSuccess = (response) ->
    @tenants = response.tenants
    @total = response.total
    @is_first_page = response.is_first_page
    @is_last_page = response.is_last_page
    console.log(response)
    ProgressBarService.complete()
    @loading = false

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
