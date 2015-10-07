'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.factory 'CommandsService', (Restangular) ->
  new class CommandsService
    SERVICE_NAME = 'devices'

    reset: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/reset").post()
      promise

    volume: (key, volume) ->
      volumeCommand = {
        volume: volume
      }
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/volume").customPOST(volumeCommand)
      promise

    custom: (key, command) ->
      customCommand = {
        command: command
      }
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/custom").customPOST(customCommand)
      promise



