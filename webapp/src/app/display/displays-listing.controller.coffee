'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DisplaysListingCtrl', ($stateParams, DisplaysService) ->

  @displays = []

  displaysPromise = DisplaysService.getDisplays()
  displaysPromise.then (data) =>
    @displays = data

  initialize: ->


  @
