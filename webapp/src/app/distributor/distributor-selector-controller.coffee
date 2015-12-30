'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DistributorSelectorCtrl", ($scope, $log, $state, $cookies, DistributorsService, SessionsService) ->
  @distributors = []
  @currentDistributor = undefined

  @initialize = ->
    distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.currentUserKey)
    if distributorsPromise
      distributorsPromise.then (data) =>
        @distributors = data
        if @distributors.length == 1
          @selectDistributor(@distributors[0])

  @selectDistributor = (distributor) =>
    @currentDistributor = distributor
    DistributorsService.currentDistributor = @currentDistributor
    $cookies.put('currentDistributorName', @currentDistributor.name)
    $cookies.put('currentDistributorKey', @currentDistributor.key)
    $state.go 'welcome'


  @
