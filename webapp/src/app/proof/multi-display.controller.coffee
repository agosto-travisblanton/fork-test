'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayMultiDisplayCtrl", (ProofPlayService) ->
  @radioButtonChoices = {
    group1: 'By Date',
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
    displays: false,
  }

  @no_cache = true
  @loading = true
  @disabled = true
  @selected_displays = []

  @initialize = =>
    ProofPlayService.getAllDisplays()
    .then (data) =>
      @loading = false
      @displays = data.data.devices

  @addToSelectedDisplays = (searchText) =>
    if @isDisplayValid(searchText)
      @selected_displays.push searchText
      index = @displays.indexOf searchText
      @displays.splice index, 1
      @searchText = ''
    @areDisplaysValid()
    @isDisabled()

  @querySearch = (displays, searchText) ->
    ProofPlayService.querySearch(displays, searchText)


  @isRadioValid = (selection) =>
    @formValidity.type = selection
    @isDisabled()


  @isDisplayValid = (searchText) =>
    if searchText in @displays
      if searchText not in @selected_displays
        true
      else
        false
    else
      false


  @areDisplaysValid = () =>
    @formValidity.displays = (@selected_displays.length > 0)
    @isDisabled()

  @isStartDateValid = (start_date) =>
    @formValidity.start_date = (start_date instanceof Date)
    @isDisabled()


  @isEndDateValid = (end_date) =>
    @formValidity.end_date = (end_date instanceof Date)
    @isDisabled()

  @removeFromSelectedDisplay = (item) =>
    index = @selected_displays.indexOf(item)
    @selected_displays.splice(index, 1)
    @displays.push item
    @areDisplaysValid()
    @isDisabled()


  @isDisabled = () =>
    if @formValidity.start_date and @formValidity.end_date and @formValidity.displays and @formValidity.type
      @disabled = false
      @final = {
        start_date_unix: moment(@dateTimeSelection.start).unix(),
        end_date_unix: moment(@dateTimeSelection.end).unix(),
        displays: @selected_displays,
        type: @radioButtonChoices.selection

      }

    else
      @disabled = true

  @submit = () =>
    if @final.type is "1"
      ProofPlayService.downloadCSVForMultipleDevicesByDate(@final.start_date_unix, @final.end_date_unix, @final.displays)

    else
      ProofPlayService.downloadCSVForMultipleDevicesSummarized(@final.start_date_unix, @final.end_date_unix, @final.displays)

  @
