'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayMultiResourceCtrl", ($state, $log, $timeout, ProofPlayService) ->
  @radioButtonChoices = {
    group1: 'By Location',
    group2: 'By Date',
    selection: null
  };

  @dateTimeSelection = {
    start: null,
    end: null
  }

  @loading = true

  loadAllResources = =>
    ProofPlayService.getAllResources()
    .then (data) =>
      @loading = false
      return data.data.resources


  loadAllResources()
  .then (data) =>
    @resources = data


  @formValidity = {
    start_date: false,
    end_date: false,
    resource: false,
  }

  @disabled = true


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
    if @formValidity.start_date and @formValidity.end_date and @formValidity.resource
      @disabled = false
      @final = {
        start_date_unix: moment(@dateTimeSelection.start).unix(),
        end_date_unix: moment(@dateTimeSelection.end).unix(),
        resource: @searchText,
      }
    else
      @disabled = true

  @submit = () =>
    console.log(@final)

  @
