'use strict'

angular.module("skykitDisplayDeviceManagement").controller "NavbarCtrl", (VersionService) ->

  @version = {
    name: undefined
  }
  versionPromise = VersionService.getVersion()
  versionPromise.then (data) =>
    @version = data

  @

