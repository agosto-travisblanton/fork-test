'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayOneResourceCtrl", (ProofPlayService) ->
  @radioButtonChoices = {
    group1: 'By Location',
    group2: 'By Date',
    selection: null
  }

  @dateTimeSelection = {
    start: null,
    end: null
  }

  @formValidity = {
    start_date: false,
    end_date: false,
    resource: false,
    type: false
  }

  @chosen_tenant = null
  @no_cache = true
  @loading = true
  @disabled = true


  @initialize = =>
    ProofPlayService.getAllResources()
    .then (data) =>
      @loading = false
      @resources = data.data.resources


  @querySearch = (resources, searchText) =>
    ProofPlayService.querySearch(resources, searchText)


  @isRadioValid = (selection) =>
    @formValidity.type = selection
    @isDisabled()


  @isResourceValid = (searchText) =>
    if searchText in @resources
      @formValidity.resource = searchText
    else
      @formValidity.resource = null
    @isDisabled()


  @isStartDateValid = (start_date) =>
    @formValidity.start_date = (start_date instanceof Date)
    @isDisabled()


  @isEndDateValid = (end_date) =>
    @formValidity.end_date = (end_date instanceof Date)
    @isDisabled()


  @isDisabled = () =>
    if @formValidity.start_date and @formValidity.end_date and @formValidity.type and @formValidity.resource
      @disabled = false
      @final = {
        start_date_unix: moment(@dateTimeSelection.start).unix(),
        end_date_unix: moment(@dateTimeSelection.end).unix(),
        resource: @searchText,
        type: @radioButtonChoices.selection
      }
    else
      @disabled = true

  @submit = () =>
    if @final.type is "1"
      ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByLocation(@final.start_date_unix, @final.end_date_unix, @final.resource)

    else
      ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByDate(@final.start_date_unix, @final.end_date_unix, @final.resource)

  @
