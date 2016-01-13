'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "VersionsCtrl", ($state, $log, VersionsService) ->
  @version_data = []

  @initialize = ->
    promise = VersionsService.getVersions()
    promise.then (data) =>
      @version_data = data

  @
