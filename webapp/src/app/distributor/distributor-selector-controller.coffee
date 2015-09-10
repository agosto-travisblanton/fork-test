'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "DistributorSelectorCtrl", ($scope, $log, $state, DistributorsService) ->
  @distributors = []
#  @currentDistributor = undefined

  @initialize = ->
    @distributors = [
      {name: 'Agosto, Inc.', key: '832742837409187234872304'}
      {name: 'Tierney Brothers, Inc.', key: '832742837409187234879887'}
      {name: 'Samsung', key: '832742837409187234877658'}
    ]
#    distributorsPromise = DistributorsService.fetchAll()
#    distributorsPromise.then (data) =>
#      @distributors = data

  @selectDistributor = ->
#    if @currentDistributor and @currentDistributor != null
#      DistributorsService.currentDistributor = @currentDistributor
    $state.go 'welcome'


  @
