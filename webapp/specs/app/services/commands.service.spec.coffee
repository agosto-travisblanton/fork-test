'use strict'

describe 'CommandsService', ->
  CommandsService = undefined
  Restangular = undefined
  promise = undefined
  $cookies = undefined
  userEmail = 'bob.macneal@agosto.com'
  key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
  payload = {
    userIdentifier: userEmail
  }

  beforeEach module('skykitProvisioning')

  beforeEach inject (_CommandsService_, _Restangular_, _$cookies_) ->
    CommandsService = _CommandsService_
    Restangular = _Restangular_
    $cookies = _$cookies_
    promise = new skykitProvisioning.q.Mock
    spyOn($cookies, 'get').and.returnValue userEmail

  describe '.reset', ->
    it 'prepares a device reset command, returning a promise', ->
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.reset key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/reset"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.powerOn', ->
    it 'prepares a power on command, returning a promise', ->
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.powerOn key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/power-on"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.powerOff', ->
    it 'prepares a power on command, returning a promise', ->
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.powerOff key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/power-off"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.contentDelete', ->
    it 'prepares a content delete command, returning a promise', ->
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.contentDelete key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/content-delete"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.volume', ->
    it 'prepares a device volume command, returning a promise', ->
      commandsRestangularService = {customPOST: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'customPOST').and.returnValue promise
      volume = 6
      payload = {
        volume: volume      }
      actual = CommandsService.volume key, volume
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}"
      expect(commandsRestangularService.customPOST).toHaveBeenCalledWith(payload, 'commands/volume')
      expect(actual).toBe promise

  describe '.custom', ->
    it 'prepares a device custom command, returning a promise', ->
      commandsRestangularService = {customPOST: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'customPOST').and.returnValue promise
      update_something = 'skykit.com/skdchromeapp/update/something'
      payload = {
        command: update_something
      }
      actual = CommandsService.custom key, update_something
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}"
      expect(commandsRestangularService.customPOST).toHaveBeenCalledWith(payload, 'commands/custom')
      expect(actual).toBe promise

