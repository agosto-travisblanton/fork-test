'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "WelcomeCtrl", ($state, DistributorsService) ->
  @distributors = []

  @initialize = ->
    promise = DistributorsService.fetchAll()
    promise.then (data) =>
      @distributors = data


  @
