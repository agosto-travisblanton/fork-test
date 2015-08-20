'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "WelcomeCtrl", ($state, DistributorsService) ->
  @distributors = []
  @currentDistributor = undefined

  @initialize = ->
    alert 'foo'
    promise = DistributorsService.fetchAll()
    promise.then (data) =>
      @distributors = data

  @selectDistributor = ->
    if @currentDistributor and @currentDistributor != null
      DistributorsService.currentDistributor = @currentDistributor

  @
