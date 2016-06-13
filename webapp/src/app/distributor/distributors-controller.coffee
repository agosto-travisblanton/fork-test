'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DistributorsCtrl", ($state) ->
  vm = @
  vm.distributors = []

  vm
