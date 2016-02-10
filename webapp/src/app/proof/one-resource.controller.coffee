'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayOneResourceCtrl", ($state, $log, $timeout, ProofPlayService) ->
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

  @no_cache = true
  @loading = true
  @disabled = true

  loadAllResources = =>
    ProofPlayService.getAllResources()
    .then (data) =>
      data.data.resources


  loadAllResources()
  .then (data) =>
    @loading = false
    @resources = data


  @querySearch = (resources, searchText) =>
    ProofPlayService.querySearch(resources, searchText)


  @isRadioValid = () =>
    @formValidity.type = @radioButtonChoices.selection
    @isDisabled()


  @isResourceValid = () =>
    if @searchText in @resources
      @formValidity.resource = @searchText
    else
      @formValidity.resource = null
    @isDisabled()


  @isStartDateValid = () =>
    @formValidity.start_date = (@dateTimeSelection.start instanceof Date)
    @isDisabled()


  @isEndDateValid = () =>
    @formValidity.end_date = (@dateTimeSelection.end instanceof Date)
    @isDisabled()


  @isDisabled = () =>
    console.log(@formValidity)
    if @formValidity.start_date and @formValidity.end_date and @formValidity.type and @formValidity.resource
      @disabled = false
      @final = {
        start_date_unix: moment(@dateTimeSelection.start).unix(),
        end_date_unix: moment(@dateTimeSelection.end).unix(),
        resource: @searchText,
        type: @radioButtonChoices.selection,
      }
    else
      @disabled = true

  @submit = () =>
    if @final.type is "1"
      ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByLocation(@final.start_date_unix, @final.end_date_unix, @final.resource)

    else
      ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByDate(@final.start_date_unix, @final.end_date_unix, @final.resource)

  @
