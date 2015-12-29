'use strict'

appModule = angular.module('skyKitProvisioning')

appModule.factory 'VersionsService', (Restangular) ->
  new class VersionsService

    getVersions: () ->
      promise = Restangular.oneUrl('versions').get()
      promise
