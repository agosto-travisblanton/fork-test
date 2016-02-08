'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", ($state, $log) ->
  vm = this;
  vm.something = "test"

  vm.tabs = [
    {title: "One-Resource", content: "test2"},
    {title: "Multi-Resource", content: "test4"}
  ]

  console.log vm.tabs

  vm.test = "test"

  vm.onTabSelected = (tab) =>
    console.log(tab)

  vm.removeTab = (tab) =>
    console.log(tab)

  return vm


