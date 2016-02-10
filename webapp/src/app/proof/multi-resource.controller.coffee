'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayMultiResourceCtrl", ($state, $log, $timeout, ProofPlayService) ->
  @dateTimeSelection = {
    start: null,
    end: null
  }

  @formValidity = {
    start_date: false,
    end_date: false,
    resources: false,
  }

  @no_cache = true
  @loading = true
  @disabled = true
  @selected_resources = []

  @addToSelectedResource = () =>
    if @isResourceValid()
      @selected_resources.push @searchText
      index = @resources.indexOf @searchText
      @resources.splice index, 1
      @searchText = ''
    @areResourcesValid()
    @isDisabled()

  @querySearch = (resources, searchText) =>
    ProofPlayService.querySearch(resources, searchText)


  loadAllResources = =>
    ProofPlayService.getAllResources()
    .then (data) =>
      data.data.resources


  loadAllResources()
  .then (data) =>
    @loading = false
    @resources = data


  @isResourceValid = () =>
    if @searchText in @resources
      if @searchText not in @selected_resources
        true
      else
        false
    else
      false


  @areResourcesValid = () =>
    @formValidity.resources = (@selected_resources.length > 0)
    @isDisabled()

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
