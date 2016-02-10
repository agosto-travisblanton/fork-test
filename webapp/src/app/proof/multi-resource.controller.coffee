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

  @selected_resources = []

  @addToSelectedResource = () =>
    if @isResourceValid()
      @selected_resources.push @searchText
      index = @resources.indexOf(@searchText);
      @resources.splice(index, 1)
      @searchText = ''
    @areResourcesValid()
    @isDisabled()


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
    resources: false,
  }

  @disabled = true


  @isResourceValid = () =>
    if @searchText in @resources
      if @searchText not in @selected_resources
        true
    else
      false


  @areResourcesValid = () =>
    console.log((@selected_resources.length > 0))
    @formValidity.resources = (@selected_resources.length > 0)

  @isStartDateValid = () =>
    @formValidity.start_date = (@dateTimeSelection.start instanceof Date)
    @isDisabled()


  @isEndDateValid = () =>
    @formValidity.end_date = (@dateTimeSelection.end instanceof Date)
    @isDisabled()

  @removeFromSelectedResource = (item) =>
    index = @selected_resources.indexOf(item);
    @selected_resources.splice(index, 1)
    @resources.push item
    @areResourcesValid()
    @isDisabled()


  @isDisabled = () =>
    console.log(@formValidity)
    if @formValidity.start_date and @formValidity.end_date and @formValidity.resources
      @disabled = false
      @final = {
        start_date_unix: moment(@dateTimeSelection.start).unix(),
        end_date_unix: moment(@dateTimeSelection.end).unix(),
        resources: @selected_resources,
      }
    else
      @disabled = true

  @submit = () =>
    ProofPlayService.downloadCSVForMultipleResources(@final.start_date_unix, @final.end_date_unix, @final.resources)

  @
