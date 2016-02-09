'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "ProofOfPlayCtrl", ($state, $log, $timeout, ProofPlayService) ->
  @tab = {title: "One-Resource"}
  @tab2 = {title: "Multi-Resource"}

  @
