'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'CommandsService', (Restangular) ->
  new class CommandsService
    SERVICE_NAME = 'devices'

    reset: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/reset").post()
      promise

    volume: (key, volume) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/volume").post({'volume': volume})
      promise

    custom: (key, command) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/custom").post({'command': command})
      promise



