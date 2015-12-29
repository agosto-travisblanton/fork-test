'use strict'

angular.module('skyKitProvisioning').factory 'IdentityService', ($log, Restangular) ->

  new class IdentityService

    getIdentity: ->
      Restangular.oneUrl('identity').get()

