'use strict'

appModule = angular.module 'skyKitProvisioning'

appModule.controller "VersionsCtrl", ($state, $log, VersionsService) ->
  @versions = []

  @initialize = ->
    promise = VersionsService.getVersions()
    promise.then (data) =>
      @versions = data

  @
