'use strict'

angular.module("skykitDisplayDeviceManagement").controller "NavbarCtrl", (VersionService) ->

  @version = {
    number: undefined
    tag: undefined
  }
  versionPromise = VersionService.getVersion()
  versionPromise.then (data) =>
    @version = data

  @

