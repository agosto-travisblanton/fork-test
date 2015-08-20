'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'VersionService', ($http, $log, Restangular) ->

  class VersionService
    @uriBase = 'v1/version'

    getVersion: ->
      Restangular.oneUrl('api/v1/version').get()

  new VersionService()
