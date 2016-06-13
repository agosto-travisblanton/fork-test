'use strict'
appModule = angular.module 'skykitProvisioning'
appModule.controller "ProofOfPlayMultiLocationCtrl", (ProofPlayService, $stateParams, $state, ToastsService) ->
  vm = @
  vm.radioButtonChoices = {
    group1: 'By Device',
    group2: 'Summarized',
    selection: null
  }


  vm.dateTimeSelection = {
    start: null,
    end: null
  }

  vm.formValidity = {
    start_date: false,
    end_date: false,
    locations: false,
  }

  vm.tenant = $stateParams.tenant
  vm.no_cache = true
  vm.loading = true
  vm.disabled = true
  vm.disabledTenant = true
  vm.selected_locations = []

  vm.initialize = ->
    ProofPlayService.getAllLocations(vm.tenant)
    .then (data) ->
      vm.loading = false
      vm.locations = data.data.locations
      if vm.locations.length > 0
        vm.had_some_items = true
      else
        vm.had_some_items = false
        
  vm.refreshLocations = () ->
    vm.searchText = ''
    vm.selectedItem = ''
    vm.loading = true
    vm.disabled = true
    vm.selected_locations = []
    ProofPlayService.proofplayCache.removeAll()
    vm.initialize()

  vm.addToSelectedLocations = (searchText) ->
    if vm.isLocationValid(searchText)
      vm.selected_locations.push searchText
      index = vm.locations.indexOf searchText
      vm.locations.splice index, 1
      vm.searchText = ''
    vm.areLocationsValid()
    vm.isDisabled()

  vm.querySearch = (locations, searchText) ->
    ProofPlayService.querySearch(locations, searchText)


  vm.isRadioValid = (selection) ->
    vm.formValidity.type = selection
    vm.isDisabled()


  vm.isLocationValid = (searchText) ->
    if searchText in vm.locations
      if searchText not in vm.selected_locations
        true
      else
        false
    else
      false


  vm.areLocationsValid = () ->
    vm.formValidity.locations = (vm.selected_locations.length > 0)
    vm.isDisabled()

  vm.isStartDateValid = (start_date) ->
    vm.formValidity.start_date = (start_date instanceof Date)
    vm.isDisabled()


  vm.isEndDateValid = (end_date) ->
    vm.formValidity.end_date = (end_date instanceof Date)
    vm.isDisabled()

  vm.removeFromSelectedLocation = (item) ->
    index = vm.selected_locations.indexOf(item)
    vm.selected_locations.splice(index, 1)
    vm.locations.push item
    vm.areLocationsValid()
    vm.isDisabled()


  vm.isDisabled = () ->
    if vm.formValidity.start_date and vm.formValidity.end_date and vm.formValidity.locations and vm.formValidity.type
      vm.disabled = false
      vm.final = {
        start_date_unix: moment(vm.dateTimeSelection.start).unix(),
        end_date_unix: moment(vm.dateTimeSelection.end).unix(),
        locations: vm.selected_locations,
        type: vm.radioButtonChoices.selection

      }

    else
      vm.disabled = true

  vm.submit = () ->
    if vm.final.type is "1"
      ProofPlayService.downloadCSVForMultipleLocationsByDevice(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.locations, vm.tenant)

    else
      ProofPlayService.downloadCSVForMultipleLocationsSummarized(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.locations, vm.tenant)

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