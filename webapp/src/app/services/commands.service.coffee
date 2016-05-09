'use strict'

appModule = angular.module('skykitProvisioning')

appModule.factory 'CommandsService', (Restangular) ->
  new class CommandsService
    SERVICE_NAME = 'devices'

    reset: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/reset").post()
      promise

    contentDelete: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/content-delete").post()
      promise

    contentUpdate: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/content-update").post()
      promise

    updateDevice: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/refresh-device-representation").post()
      promise

    volume: (key, volume) ->
      volumeCommand = {
        volume: volume
      }
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(volumeCommand, 'commands/volume')
      promise

    custom: (key, command) ->
      customCommand = {
        command: command
      }
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(customCommand, 'commands/custom')
      promise

    powerOn: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/power-on").post()
      promise

    powerOff: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}/commands/power-off").post()
      promise

