'use strict'

appModule = angular.module('skykitProvisioning')

appModule.factory 'VersionsService', (Restangular) ->
  new class VersionsService

    getVersions: () ->
      promise = Restangular.oneUrl('versions').get()
      promise
