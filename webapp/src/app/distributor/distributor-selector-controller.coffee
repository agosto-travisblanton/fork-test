'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DistributorSelectorCtrl", ($scope, $log, $state, $cookies, DistributorsService, SessionsService, ToastsService) ->
  @distributors = []
  @currentDistributor = undefined
  @loading = true

  @initialize = ->
    @loading = true
    distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.currentUserKey)
    distributorsPromise.then (data) =>
      @distributors = data
      if @distributors.length == 1
        @selectDistributor(@distributors[0])
      else
        @loading = false


  @selectDistributor = (distributor) =>
    @currentDistributor = distributor
    DistributorsService.currentDistributor = @currentDistributor
    $cookies.put('currentDistributorName', @currentDistributor.name)
    $cookies.put('currentDistributorKey', @currentDistributor.key)
    if not @distributors.length == 1
      ToastsService.showSuccessToast "Distributor #{distributor.name} selected!"
    $state.go 'welcome'

  @
