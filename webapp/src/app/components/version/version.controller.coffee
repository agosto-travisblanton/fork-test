'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'VersionCtrl', ($scope, $stateParams, VersionService) ->
  @version = {
    number: undefined
    tag: undefined
  }

  initialize: ->
    versionPromise = VersionService.getVersion()
    versionPromise.then (data) =>
      debugger
      @version = data


  @
