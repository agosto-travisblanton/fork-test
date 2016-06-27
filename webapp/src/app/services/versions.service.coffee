'use strict'

angular.module('skykitProvisioning').factory 'VersionsService', (Restangular) ->
  new class VersionsService
    constructor: ->

    getVersions: () ->
      promise = Restangular.oneUrl('versions').get()
      promise
