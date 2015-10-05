'use strict'

describe 'CommandsService', ->
  CommandsService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_CommandsService_, _Restangular_) ->
    CommandsService = _CommandsService_
    Restangular = _Restangular_
    promise = new skykitDisplayDeviceManagement.q.Mock

  describe '.reset', ->
    it 'prepares a device reset command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = { post: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      actual = CommandsService.reset key
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/reset"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.volume', ->
    it 'prepares a device volume command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = { post: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      payload = {'volume': 5}
      actual = CommandsService.volume key, payload
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/volume"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise

  describe '.custom', ->
    it 'prepares a device custom command, returning a promise', ->
      key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw'
      commandsRestangularService = { post: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue commandsRestangularService
      spyOn(commandsRestangularService, 'post').and.returnValue promise
      payload = {'command': 'skykit.com/skdchromeapp/channel/2'}
      actual = CommandsService.custom key, payload
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'devices', "api/v1/devices/#{key}/commands/custom"
      expect(commandsRestangularService.post).toHaveBeenCalled()
      expect(actual).toBe promise
