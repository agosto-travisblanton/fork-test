'use strict'

describe 'DistributorsCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  DistributorsService = undefined
  promise = undefined


  beforeEach module('skyKitProvisioning')

  beforeEach inject (_$controller_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
#    DistributorsService = _DistributorsService_
    controller = $controller 'DistributorsCtrl', {
      $state: $state
      #DistributorsService: DistributorsService
    }

  describe 'initialization', ->
    it 'distributors should be an empty array', ->
      expect(angular.isArray(controller.distributors)).toBeTruthy()

  describe '.initialize', ->
    distributors = [
#      {key: 'dhjad897d987fadafg708fg7d', name: 'Foobar1', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
#      {key: 'dhjad897d987fadafg708y67d', name: 'Foobar2', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
#      {key: 'dhjad897d987fadafg708hb55', name: 'Foobar3', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]

#    beforeEach ->
#      promise = new skyKitProvisioning.q.Mock
#      spyOn(DistributorsService, 'fetchAllDistributors').and.returnValue promise
#
#    it 'call DistributorsService.fetchAllDistributors to retrieve all distributors', ->
#      controller.initialize()
#      promise.resolve distributors
#      expect(DistributorsService.fetchAllDistributors).toHaveBeenCalled()
#
#    it "the 'then' handler caches the retrieved distributors in the controller", ->
#      controller.initialize()
#      promise.resolve distributors
#      expect(controller.distributors).toBe distributors
#
#  describe '.editItem', ->
#    distributor = {key: 'dhjad897d987fadafg708hb55'}
#
#    beforeEach ->
#      spyOn $state, 'go'
#
#    it "route to the 'editDistributor' named route, passing the supplied distributor key", ->
#      controller.editItem(distributor)
#      expect($state.go).toHaveBeenCalledWith 'editDistributor', {distributorKey: distributor.key}
#
#  describe '.deleteItem', ->
#    distributor = {
#      key: 'dhjad897d987fadafg708fg7d'
#      name: 'Foobar3'
#      created: '2015-05-10 22:15:10'
#      updated: '2015-05-10 22:15:10'
#    }
#
#    beforeEach ->
#      promise = new skyKitProvisioning.q.Mock
#      spyOn(DistributorsService, 'delete').and.returnValue promise
#      spyOn controller, 'initialize'
#
#    it 'call DistributorsService.delete distributor', ->
#      controller.deleteItem distributor
#      promise.resolve()
#      expect(DistributorsService.delete).toHaveBeenCalledWith distributor
#
#    it "the 'then' handler calls initialize to re-fetch all distributors", ->
#      controller.deleteItem distributor
#      promise.resolve()
#      expect(controller.initialize).toHaveBeenCalled
#
