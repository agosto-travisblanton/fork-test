'use strict'
appModule = angular.module 'skykitProvisioning'
appModule.controller "ProofOfPlayMultiDisplayCtrl", (ProofPlayService, $stateParams, $state, ToastsService) ->
  vm = @
  
  vm.radioButtonChoices = {
    group1: 'By Date',
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
    displays: false,
  }

  vm.tenant = $stateParams.tenant
  vm.no_cache = true
  vm.loading = true
  vm.disabled = true
  vm.disabledTenant = true
  vm.selected_displays = []
  

  vm.initialize = ->
    ProofPlayService.getAllDisplays(vm.tenant)
    .then (data) ->
      vm.loading = false
      vm.displays = data.data.devices
      if vm.displays.length > 0
        vm.had_some_items = true
      else
        vm.had_some_items = false
        
  vm.refreshDisplays = () ->
    vm.searchText = ''
    vm.selectedItem = ''
    vm.loading = true
    vm.disabled = true
    vm.selected_displays = []
    ProofPlayService.proofplayCache.removeAll()
    vm.initialize()

  vm.addToSelectedDisplays = (searchText) ->
    if vm.isDisplayValid(searchText)
      vm.selected_displays.push searchText
      index = vm.displays.indexOf searchText
      vm.displays.splice index, 1
      vm.searchText = ''
    vm.areDisplaysValid()
    vm.isDisabled()

  vm.querySearch = (displays, searchText) ->
    ProofPlayService.querySearch(displays, searchText)


  vm.isRadioValid = (selection) ->
    vm.formValidity.type = selection
    vm.isDisabled()


  vm.isDisplayValid = (searchText) ->
    if searchText in vm.displays
      if searchText not in vm.selected_displays
        true
      else
        false
    else
      false

  vm.areDisplaysValid = () ->
    vm.formValidity.displays = (vm.selected_displays.length > 0)
    vm.isDisabled()

  vm.isStartDateValid = (start_date) ->
    vm.formValidity.start_date = (start_date instanceof Date)
    vm.isDisabled()


  vm.isEndDateValid = (end_date) ->
    vm.formValidity.end_date = (end_date instanceof Date)
    vm.isDisabled()

  vm.removeFromSelectedDisplay = (item) ->
    index = vm.selected_displays.indexOf(item)
    vm.selected_displays.splice(index, 1)
    vm.displays.push item
    vm.areDisplaysValid()
    vm.isDisabled()


  vm.isDisabled = () ->
    if vm.formValidity.start_date and vm.formValidity.end_date and vm.formValidity.displays and vm.formValidity.type
      vm.disabled = false
      vm.final = {
        start_date_unix: moment(vm.dateTimeSelection.start).unix(),
        end_date_unix: moment(vm.dateTimeSelection.end).unix(),
        displays: vm.selected_displays,
        type: vm.radioButtonChoices.selection

      }

    else
      vm.disabled = true

  vm.submit = () ->
    if vm.final.type is "1"
      ProofPlayService.downloadCSVForMultipleDevicesByDate(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.displays, vm.tenant)

    else
      ProofPlayService.downloadCSVForMultipleDevicesSummarized(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.displays, vm.tenant)


  vm.tenants = null
  vm.currentTenant = vm.tenant

  vm.initialize_tenant_select = () ->
    ProofPlayService.getAllTenants()
    .then (data) ->
      vm.tenants = data.data.tenants

  vm.submitTenant = (tenant) ->
    if tenant != vm.currentTenant
      $state.go 'proofDetail', {
        tenant: tenant
      }

      ToastsService.showSuccessToast "Proof of Play reporting set to " + tenant

    else
      ToastsService.showErrorToast "Proof of Play reporting is already set to " + tenant

  vm.querySearch = (resources, searchText) ->
    ProofPlayService.querySearch(resources, searchText)

  vm.isSelectionValid = (search) ->
    if search in vm.tenants
      vm.disabledTenant = false
    else
      vm.disabledTenant = true


  vm