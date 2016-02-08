'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", ($state, $log, $scope, ProofPlayService) ->
  @something = "test"

  @tabs = [
    {title: "One-Resource", content: "test2"},
    {title: "Multi-Resource", content: "test4"}
  ]

  @onTabSelected = (tab) =>
    console.log(tab)

  @removeTab = (tab) =>
    console.log(tab)


  console.log(ProofPlayService.test())