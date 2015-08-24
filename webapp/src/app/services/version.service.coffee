'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'VersionService', (Restangular) ->
  class VersionService

    getVersion: () ->
      Restangular.oneUrl('version').get()

  new VersionService()
