'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "WelcomeCtrl", ($log, DistributorsService, identity) ->
  @distributors = []
  @currentDistributor = undefined
  @clientId = identity.CLIENT_ID
  @state = identity.STATE

  @initialize = ->
    distributorsPromise = DistributorsService.fetchAll()
    distributorsPromise.then (data) =>
      @distributors = data

  @selectDistributor = ->
    if @currentDistributor and @currentDistributor != null
      DistributorsService.currentDistributor = @currentDistributor

  @
