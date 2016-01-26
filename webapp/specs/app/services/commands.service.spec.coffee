'use strict'

describe 'CommandsService', ->
  CommandsService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_CommandsService_, _Restangular_) ->
    CommandsService = _CommandsService_
    Restangular = _Restangular_
    promise = new skykitProvisioning.q.Mock

  describe '.reset', ->
    it 'prepares a device reset command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.reset key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/reset"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.volume', ->
    it 'prepares a device volume command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = {customPOST: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'customPOST').and.returnValue promise
      volume = 6
      volumeCommand = {
        volume: volume
      }
      actual = CommandsService.volume key, volume
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}"
      expect(commandsRestangularService.customPOST).toHaveBeenCalledWith(volumeCommand, 'commands/volume')
      expect(actual).toBe promise

  describe '.custom', ->
    it 'prepares a device custom command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = {customPOST: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'customPOST').and.returnValue promise
      channel_change = 'skykit.com/skdchromeapp/channel/2'
      customCommand = {
        command: channel_change
      }
      actual = CommandsService.custom key, channel_change
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}"
      expect(commandsRestangularService.customPOST).toHaveBeenCalledWith(customCommand, 'commands/custom')
      expect(actual).toBe promise

  describe '.powerOn', ->
    it 'prepares a power on command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.powerOn key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/power-on"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.powerOff', ->
    it 'prepares a power off command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.powerOff key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/power-off"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.contentDelete', ->
    it 'prepares a power off command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = {post: ->}
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.contentDelete key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/content-delete"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise
