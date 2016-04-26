'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DistributorSelectorCtrl", ($scope, $log, $state, $cookies, DistributorsService, SessionsService, ToastsService) ->
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
    if @distributors.length == 1
      ToastsService.showSuccessToast @distributors[0].name + " is the only distributor associated with this account. Automatically choosing " + @distributors[0].name + " as your distributor."
    else
      ToastsService.showSuccessToast "Distributor " + @distributors[0].name + " selected!"
    $state.go 'welcome'

  @
