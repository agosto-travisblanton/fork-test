'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", ($state, $log, $scope, ProofPlayService) ->
  @something = "test"

  @tab = {title: "One-Resource", content: "test2"}

  @tab2 = {title: "Multi-Resource", content: "test2"}

  @radioButtonChoices = {
      group1 : 'By Location',
      group2 : 'By Date',
    };

  @onTabSelected = (tab) =>
    console.log(tab)

#  ProofPlayService.getAllResources()
#    .then (data) =>
#      console.log(data)
#





  @
