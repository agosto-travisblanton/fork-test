'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'DevicesService', ($http, $log, Restangular) ->

  class DevicesService
    @uriBase = 'v1/devices'

    all: ->
      devices = Restangular.all @uriBase
      devices

  new DevicesService()
