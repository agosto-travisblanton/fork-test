'use strict'

describe 'DistributorsService', ->
  DistributorsService = undefined
  Restangular = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_DistributorsService_, _Restangular_) ->
    DistributorsService = _DistributorsService_
    Restangular = _Restangular_
    promise = new skykitDisplayDeviceManagement.q.Mock

  describe 'service initialization', ->
    it 'the current distributor is undefined', ->
      expect(DistributorsService.currentDistributor).toBeUndefined()

  describe '.save', ->
    describe 'existing distributor', ->
      distributor = undefined
      result = undefined

      beforeEach ->
        distributor = {
          key: 'kdfalkdsjfakjdf98ad87fa87df0'
          put: ->
        }
        spyOn(distributor, 'put').and.returnValue promise
        result = DistributorsService.save distributor

      it 'calls put() on existing distributor', ->
        expect(distributor.put).toHaveBeenCalled()

      it 'returns a promise', ->
        expect(result).toBe promise

    describe 'new distributor', ->
      distributor = undefined
      result = undefined
      distributorRestangularService = undefined

      beforeEach ->
        distributor = {
          key: undefined
        }
        distributorRestangularService = { post: (distributor) -> }
        spyOn(Restangular, 'service').and.returnValue distributorRestangularService
        spyOn(distributorRestangularService, 'post').and.returnValue promise
        result = DistributorsService.save distributor

      it 'obtains Restangular service for distributors', ->
        expect(Restangular.service).toHaveBeenCalledWith 'distributors'

      it 'calls post(distributor) on Restangular service for distributors', ->
        expect(distributorRestangularService.post).toHaveBeenCalledWith distributor

      it 'returns a promise', ->
        expect(result).toBe promise

  describe '.fetchAll', ->
    distributorRestangularService = undefined
    result = undefined

    beforeEach ->
      distributorRestangularService = { getList: -> }
      spyOn(Restangular, 'all').and.returnValue distributorRestangularService
      spyOn(distributorRestangularService, 'getList').and.returnValue promise
      result = DistributorsService.fetchAll()

    it 'obtains Restangular service for distributors', ->
      expect(Restangular.all).toHaveBeenCalledWith 'distributors'

    it 'obtains a list of distributors from the Restangular service', ->
      expect(distributorRestangularService.getList).toHaveBeenCalled()

    it 'returns a promise', ->
      expect(result).toBe promise

  describe '.getByKey', ->
    distributorRestangularService = undefined
    result = undefined
    distributorKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67'

    beforeEach ->
      distributorRestangularService = { get: -> }
      spyOn(Restangular, 'oneUrl').and.returnValue distributorRestangularService
      spyOn(distributorRestangularService, 'get').and.returnValue promise
      result = DistributorsService.getByKey(distributorKey)

    it 'obtains Restangular service for distributors', ->
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'distributors', "distributors/#{distributorKey}"

    it 'obtains the distributor from the Restangular service', ->
      expect(distributorRestangularService.get).toHaveBeenCalled()

    it 'returns a promise', ->
      expect(result).toBe promise

  describe '.delete', ->
    distributorRestangularService = undefined
    result = undefined
    distributor = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'Foobar'}

    beforeEach ->
      distributorRestangularService = { remove: -> }
      spyOn(Restangular, 'one').and.returnValue distributorRestangularService
      spyOn(distributorRestangularService, 'remove').and.returnValue promise
      result = DistributorsService.delete distributor

    it 'obtains Restangular service for the particular distributor', ->
      expect(Restangular.one).toHaveBeenCalledWith 'distributors', distributor.key

    it 'removes the distributor via the Restangular service', ->
      expect(distributorRestangularService.remove).toHaveBeenCalled()

    it 'returns a promise', ->
      expect(result).toBe promise
