'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "TenantsCtrl", ($state, $log, TenantsService, ProgressBarService, sweet) ->
  vm = @
  vm.tenants = []

  vm.getTenants = (page_size, offset) ->
    vm.offset = offset
    vm.loading = true
    ProgressBarService.start()
    promise = TenantsService.fetchAllTenantsPaginated(page_size, offset)
    promise.then ((response) ->
      vm.getFetchSuccess(response)
    ), (response) ->
      vm.getFetchFailure(response)

  vm.initialize = ->
    vm.offset = 0
    vm.getTenants(100, vm.offset)

  vm.getFetchSuccess = (response) ->
    vm.tenants = response.tenants
    vm.total = response.total
    vm.is_first_page = response.is_first_page
    vm.is_last_page = response.is_last_page
    ProgressBarService.complete()
    vm.loading = false

  vm.getFetchFailure = (response) ->
    ProgressBarService.complete()
    errorMessage = "Unable to fetch tenants. Error: #{response.status} #{response.statusText}."
    sweet.show('Oops...', errorMessage, 'error')

  vm.editItem = (item) ->
    $state.go 'tenantDetails', {tenantKey: item.key}

  vm.deleteItem = (item) ->
    callback = () ->
      promise = TenantsService.delete item
      promise.then () ->
        vm.initialize()
    
    sweet.show({
      title: "Are you sure?",
      text: "This will permanently remove the tenant from the system.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, remove the tenant!",
      closeOnConfirm: true
    }, callback)

  vm