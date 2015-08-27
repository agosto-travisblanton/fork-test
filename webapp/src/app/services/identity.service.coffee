'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'IdentityService', ($log, Restangular) ->

  new class IdentityService

    getIdentity: ->
      Restangular.oneUrl('identity').get()



