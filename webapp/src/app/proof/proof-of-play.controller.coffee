'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", ($state, $log, $timeout, ProofPlayService) ->
  @tab = {title: "One-Resource"}
  @tab2 = {title: "Multi-Resource"}

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


  @submit = () ->
    console.log(@searchText)
    console.log(@radioButtonChoices.selection)
    console.log(@dateTimeSelection)

    if @searchText and @radioButtonChoices.selection and @dateTimeSelection.start and @dateTimeSelection.end
      if @searchText in @resources

        final = {
          start_date_unix: moment(@dateTimeSelection.start).unix(),
          end_date_unix: moment(@dateTimeSelection.end).unix(),
          resource: @searchText,
          type: @radioButtonChoices.selection,
        }

        console.log(final)

      else
        alert("you need to choose a valid resource")

    else
      alert("please complete your form")
  @
