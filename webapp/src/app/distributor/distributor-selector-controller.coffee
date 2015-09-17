'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "DistributorSelectorCtrl", ($scope, $log, $state, DistributorsService, SessionsService) ->
  @distributors = []
  @currentDistributor = undefined

  @initialize = ->
    distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.currentUserKey)
    if distributorsPromise
      distributorsPromise.then (data) =>
        @distributors = data

  @selectDistributor = (distributor) =>
    @currentDistributor = distributor
    DistributorsService.currentDistributor = @currentDistributor
    $state.go 'welcome'


  @
