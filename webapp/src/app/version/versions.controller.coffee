'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "VersionsCtrl", ($state, $log, VersionsService) ->
  @versions = []

  @initialize = ->
    promise = VersionsService.getVersions()
    promise.then (data) =>
      @versions = data

  @
