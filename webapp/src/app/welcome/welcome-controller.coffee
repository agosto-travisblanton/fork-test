'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "WelcomeCtrl", (VersionsService) ->
  vm = @
  vm.version_data = []

  vm.initialize = ->
    promise = VersionsService.getVersions()
    promise.then (data) =>
      vm.version_data = data

  vm
