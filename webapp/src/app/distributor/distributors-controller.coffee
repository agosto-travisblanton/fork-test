'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DistributorsCtrl", ($state) ->
  @distributors = []

  @
