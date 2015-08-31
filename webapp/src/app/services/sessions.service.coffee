'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'SessionsService', ($http, $log, Restangular) ->

  new class SessionsService
    SERVICE_NAME = 'sessions'
    @uriBase = 'v1/sessions'

    getIdentity: ->
      Restangular.oneUrl('api/v1/devices').get()



