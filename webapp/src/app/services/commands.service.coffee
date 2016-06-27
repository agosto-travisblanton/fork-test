'use strict'

appModule = angular.module('skykitProvisioning')

appModule.factory 'CommandsService', (Restangular) ->
  new class CommandsService
    
    constructor: ->
      @SERVICE_NAME = 'devices'

    reset: (key) ->
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}/commands/reset").post()
      promise

    contentDelete: (key) ->
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}/commands/content-delete").post()
      promise

    contentUpdate: (key) ->
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}/commands/content-update").post()
      promise

    updateDevice: (key) ->
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}/commands/refresh-device-representation").post()
      promise

    powerOn: (key) ->
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}/commands/power-on").post()
      promise

    powerOff: (key) ->
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}/commands/power-off").post()
      promise

    volume: (key, volume) ->
      payload = {
        volume: volume
      }
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}").customPOST(payload, 'commands/volume')
      promise

    custom: (key, command) ->
      payload = {
        command: command
      }
      promise = Restangular.oneUrl(@SERVICE_NAME, "api/v1/devices/#{key}").customPOST(payload, 'commands/custom')
      promise
