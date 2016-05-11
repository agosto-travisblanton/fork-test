'use strict'

appModule = angular.module('skykitProvisioning')

appModule.factory 'CommandsService', (Restangular,  $cookies) ->
  new class CommandsService
    SERVICE_NAME = 'devices'

    reset: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(
        { userIdentifier:  getUserIdentifier()}, 'commands/reset')
      promise

    contentDelete: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(
        { userIdentifier:  getUserIdentifier()}, 'commands/content-delete')
      promise

    contentUpdate: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(
        { userIdentifier:  getUserIdentifier()}, 'commands/content-update')
      promise

    updateDevice: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(
        { userIdentifier:  getUserIdentifier()},
        'commands/refresh-device-representation')
      promise

    powerOn: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(
        { userIdentifier:  getUserIdentifier()}, 'commands/power-on')
      promise

    powerOff: (key) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(
        { userIdentifier:  getUserIdentifier()}, 'commands/power-off')
      promise

    volume: (key, volume) ->
      payload = {
        volume: volume,
        userIdentifier:  getUserIdentifier()
      }
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(payload, 'commands/volume')
      promise

    custom: (key, command) ->
      payload = {
        command: command,
        userIdentifier:  getUserIdentifier()
      }
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(payload, 'commands/custom')
      promise

    getUserIdentifier = ->
      userEmail = undefined
      if $cookies.get('userEmail')
        userEmail = $cookies.get('userEmail')
      userEmail
