'use strict'
appModule = angular.module 'skykitProvisioning'
appModule.controller "ProofOfPlayMultiLocationCtrl", (ProofPlayService, $stateParams, $state, ToastsService) ->
  @radioButtonChoices = {
    group1: 'By Device',
    group2: 'Summarized',
    selection: null
  }


  @dateTimeSelection = {
    start: null,
    end: null
  }

  @formValidity = {
    start_date: false,
    end_date: false,
    locations: false,
  }

  @tenant = $stateParams.tenant
  @no_cache = true
  @loading = true
  @disabled = true
  @selected_locations = []

  @initialize = =>
    ProofPlayService.getAllLocations(@tenant)
    .then (data) =>
      @loading = false
      @locations = data.data.locations
      if @locations.length > 0
        @had_some_items = true
      else
        @had_some_items = false

  @addToSelectedLocations = (searchText) =>
    if @isLocationValid(searchText)
      @selected_locations.push searchText
      index = @locations.indexOf searchText
      @locations.splice index, 1
      @searchText = ''
    @areLocationsValid()
    @isDisabled()

  @querySearch = (locations, searchText) ->
    ProofPlayService.querySearch(locations, searchText)


  @isRadioValid = (selection) =>
    @formValidity.type = selection
    @isDisabled()


  @isLocationValid = (searchText) =>
    if searchText in @locations
      if searchText not in @selected_locations
        true
      else
        false
    else
      false


  @areLocationsValid = () =>
    @formValidity.locations = (@selected_locations.length > 0)
    @isDisabled()

  @isStartDateValid = (start_date) =>
    @formValidity.start_date = (start_date instanceof Date)
    @isDisabled()


  @isEndDateValid = (end_date) =>
    @formValidity.end_date = (end_date instanceof Date)
    @isDisabled()

  @removeFromSelectedLocation = (item) =>
    index = @selected_locations.indexOf(item)
    @selected_locations.splice(index, 1)
    @locations.push item
    @areLocationsValid()
    @isDisabled()


  @isDisabled = () =>
    if @formValidity.start_date and @formValidity.end_date and @formValidity.locations and @formValidity.type
      @disabled = false
      @final = {
        start_date_unix: moment(@dateTimeSelection.start).unix(),
        end_date_unix: moment(@dateTimeSelection.end).unix(),
        locations: @selected_locations,
        type: @radioButtonChoices.selection

      }

    else
      @disabled = true

  @submit = () =>
    if @final.type is "1"
      ProofPlayService.downloadCSVForMultipleLocationsByDevice(@final.start_date_unix, @final.end_date_unix, @final.locations, @tenant)

    else
      ProofPlayService.downloadCSVForMultipleLocationsSummarized(@final.start_date_unix, @final.end_date_unix, @final.locations, @tenant)

  @tenants = null
  @currentTenant = @tenant

  @initialize_tenant_select = () ->
    ProofPlayService.getAllTenants()
    .then (data) =>
      @tenants = data.data.tenants


  @submitTenant = (tenant) =>
    if tenant != @currentTenant
      $state.go 'proofDetail', {
        tenant: tenant
      }
      ToastsService.showSuccessToast "Proof of Play reporting set to " + tenant 
    else 
      ToastsService.showErrorToast "Proof of Play reporting is already set to " + tenant 

  @