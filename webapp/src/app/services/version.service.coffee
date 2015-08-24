'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'VersionService', ($http, $log, Restangular) ->

  class VersionService

    getVersion: ->
      Restangular.oneUrl('version').get()

  new VersionService()
