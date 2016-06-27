'use strict'

angular.module('skykitProvisioning').factory 'IdentityService', ($log, Restangular) ->
  new class IdentityService

    constructor: ->

    getIdentity: ->
      Restangular.oneUrl('identity').get()

