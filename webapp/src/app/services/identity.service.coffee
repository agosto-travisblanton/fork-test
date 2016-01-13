'use strict'

angular.module('skykitProvisioning').factory 'IdentityService', ($log, Restangular) ->

  new class IdentityService

    getIdentity: ->
      Restangular.oneUrl('identity').get()

