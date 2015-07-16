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

#  describe '.fetchAllDistributors', ->
#    it 'retrieve all distributors, returning a promise', ->
#      distributorRestangularService = { getList: -> }
#      spyOn(Restangular, 'all').and.returnValue distributorRestangularService
#      spyOn(distributorRestangularService, 'getList').and.returnValue promise
#      actual = DistributorsService.fetchAllDistributors()
#      expect(Restangular.all).toHaveBeenCalledWith 'distributors'
#      expect(distributorRestangularService.getList).toHaveBeenCalled()
#      expect(actual).toBe promise
#
#  describe '.getDistributorByKey', ->
#    it 'retrieve distributor by key, returning a promise', ->
#      distributorKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67'
#      distributorRestangularService = { get: -> }
#      spyOn(Restangular, 'oneUrl').and.returnValue distributorRestangularService
#      spyOn(distributorRestangularService, 'get').and.returnValue promise
#      actual = DistributorsService.getDistributorByKey distributorKey
#      expect(Restangular.oneUrl).toHaveBeenCalledWith 'distributors', "api/v1/distributors/#{distributorKey}"
#      expect(distributorRestangularService.get).toHaveBeenCalled()
#      expect(actual).toBe promise
#
#  describe '.delete', ->
#    it 'delete distributor, returning a promise', ->
#      distributor = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'Foobar'}
#      distributorRestangularService = { remove: -> }
#      spyOn(Restangular, 'one').and.returnValue distributorRestangularService
#      spyOn(distributorRestangularService, 'remove').and.returnValue promise
#      actual = DistributorsService.delete distributor
#      expect(Restangular.one).toHaveBeenCalledWith 'distributors', distributor.key
#      expect(distributorRestangularService.remove).toHaveBeenCalled()
#      expect(actual).toBe promise
