'use strict'
appModule = angular.module 'skykitProvisioning'
appModule.controller "ProofOfPlayMultiResourceCtrl", (ProofPlayService, $stateParams, $state, ToastsService) ->
  vm = @
  vm.radioButtonChoices = {
    group1: 'By Device',
    group2: 'By Date',
    selection: null
  }


  vm.dateTimeSelection = {
    start: null,
    end: null
  }

  vm.formValidity = {
    start_date: false,
    end_date: false,
    resources: false,
  }

  vm.tenant = $stateParams.tenant
  vm.no_cache = true
  vm.loading = true
  vm.disabled = true
  vm.disabledTenant = true
  vm.selected_resources = []

  vm.initialize = ->
    ProofPlayService.getAllResources(vm.tenant)
    .then (data) ->
      vm.loading = false
      vm.full_resource_map = data.data.resources
      vm.resources = (resource.resource_name for resource in data.data.resources)
      if vm.resources.length > 0
        vm.had_some_items = true
      else
        vm.had_some_items = false
        
  vm.refreshResources = () ->
    vm.searchText = ''
    vm.selectedItem = ''
    vm.loading = true
    vm.disabled = true
    vm.selected_resources = []
    ProofPlayService.proofplayCache.removeAll()
    vm.initialize()

  vm.addToSelectedResources = (searchText) ->
    if vm.isResourceValid(searchText)
      vm.selected_resources.push searchText
      index = vm.resources.indexOf searchText
      vm.resources.splice index, 1
      vm.searchText = ''
    vm.areResourcesValid()
    vm.isDisabled()

  vm.querySearch = (resources, searchText) ->
    ProofPlayService.querySearch(resources, searchText)


  vm.isRadioValid = (selection) ->
    vm.formValidity.type = selection
    vm.isDisabled()


  vm.isResourceValid = (searchText) ->
    if searchText in vm.resources
      if searchText not in vm.selected_resources
        true
      else
        false
    else
      false


  vm.areResourcesValid = () ->
    vm.formValidity.resources = (vm.selected_resources.length > 0)
    vm.isDisabled()

  vm.isStartDateValid = (start_date) ->
    vm.formValidity.start_date = (start_date instanceof Date)
    vm.isDisabled()


  vm.isEndDateValid = (end_date) ->
    vm.formValidity.end_date = (end_date instanceof Date)
    vm.isDisabled()

  vm.removeFromSelectedResource = (item) ->
    index = vm.selected_resources.indexOf(item)
    vm.selected_resources.splice(index, 1)
    vm.resources.push item
    vm.areResourcesValid()
    vm.isDisabled()


  vm.isDisabled = () ->
    if vm.formValidity.start_date and vm.formValidity.end_date and vm.formValidity.resources and vm.formValidity.type
      vm.disabled = false
      vm.final = {
        start_date_unix: moment(vm.dateTimeSelection.start).unix(),
        end_date_unix: moment(vm.dateTimeSelection.end).unix(),
        resources: vm.selected_resources,
        type: vm.radioButtonChoices.selection
      }

    else
      vm.disabled = true

  vm.submit = () ->
    resources_as_ids = []
    for item in vm.final.resources
      for each in vm.full_resource_map
        if each["resource_name"] == item
          resources_as_ids.push each["resource_identifier"]

    if vm.final.type is "1"
      ProofPlayService.downloadCSVForMultipleResourcesByDevice(vm.final.start_date_unix, vm.final.end_date_unix, resources_as_ids, vm.tenant)

    else
      ProofPlayService.downloadCSVForMultipleResourcesByDate(vm.final.start_date_unix, vm.final.end_date_unix, resources_as_ids, vm.tenant)

  vm.tenants = null
  vm.currentTenant = vm.tenant

  vm.initialize_tenant_select = () ->
    ProofPlayService.getAllTenants()
    .then (data) ->
      vm.tenants = data.data.tenants
      
  vm.querySearch = (resources, searchText) ->
    ProofPlayService.querySearch(resources, searchText)

  vm.isSelectionValid = (search) ->
    if search in vm.tenants
      vm.disabledTenant = false
    else
      vm.disabledTenant = true


  vm.submitTenant = (tenant) ->
    if tenant != vm.currentTenant
      $state.go 'proofDetail', {
        tenant: tenant
      }
      ToastsService.showSuccessToast "Proof of Play reporting set to " + tenant
    else
      ToastsService.showErrorToast "Proof of Play reporting is already set to " + tenant


  vm
