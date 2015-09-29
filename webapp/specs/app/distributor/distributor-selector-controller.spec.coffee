'use strict'

describe 'DistributorSelectorCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  promise = undefined
  $rootScope = undefined
  $scope = undefined
  $log = undefined
  SessionsService = undefined
  DistributorsService = undefined


  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_,
                     _$state_,
                     _$rootScope_,
                     _$log_,
                     _DistributorsService_,
                     _SessionsService_) ->
    $controller = _$controller_
    $state = _$state_
    $rootScope = _$rootScope_
    $scope = _$rootScope_.$new()
    $log = _$log_
    DistributorsService = _DistributorsService_
    SessionsService = _SessionsService_
    controller = $controller 'DistributorSelectorCtrl', {
      $scope: $scope
      $log: $log
      $state: $state
      DistributorsService: DistributorsService
      SessionsService: SessionsService
    }

  describe 'initialization', ->
    it 'distributors should be an empty array', ->
      expect(angular.isArray(controller.distributors)).toBeTruthy()

    it 'currentDistributor should be undefined', ->
      expect(controller.currentDistributor).toBeUndefined()


  describe '.initialize', ->
    promise = undefined
    expectedCurrentUserKey = '32748092734827340'

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock()
      SessionsService.currentUserKey = expectedCurrentUserKey
      spyOn(DistributorsService, 'fetchAllByUser').and.callFake (currentUserKey) -> return promise
      spyOn(controller, 'selectDistributor')
      controller.initialize()

    describe 'when distributors array is not a length of 1', ->
      distributors = [
        {key: 'dsifuyadfya7a8sdf678a6dsf9', name: ''}
        {key: 'dsifuyadfya7a8sdf678a6dff7', name: ''}
      ]

      it 'invokes DistributorsService.fetchAllByUser', ->
        expect(DistributorsService.fetchAllByUser).toHaveBeenCalledWith expectedCurrentUserKey

      it 'sets distributors on the controller with the result from the promise', ->
        promise.resolve distributors
        expect(controller.distributors).toEqual distributors

      it 'does not call selectDistributor()', ->
        promise.resolve distributors
        expect(controller.selectDistributor).not.toHaveBeenCalled()

    describe 'when distributors array is a length of 1', ->
      distributors = [{key: 'dsifuyadfya7a8sdf678a6dsf9', name: ''}]

      it 'invokes DistributorsService.fetchAllByUser', ->
        expect(DistributorsService.fetchAllByUser).toHaveBeenCalledWith expectedCurrentUserKey

      it 'sets distributors on the controller with the result from the promise', ->
        promise.resolve distributors
        expect(controller.distributors).toEqual distributors

      it 'calls selectDistributor() to select the only distributor returned from the backend', ->
        promise.resolve distributors
        expect(controller.selectDistributor).toHaveBeenCalledWith distributors[0]


  describe '.selectDistributor', ->
    distributor = {key: 'd78f9a0d89f7a0876ga7f6ga786g5a78df57d6f5a6dsf'}

    beforeEach ->
      spyOn($state, 'go')
      controller.selectDistributor(distributor)

    it 'sets the currentDistributor property', ->
      expect(controller.currentDistributor).toEqual distributor

    it 'sets the currentDistributor property on DistributorService', ->
      expect(DistributorsService.currentDistributor).toEqual distributor

    it 'calls $state.go to route to the welcome view', ->
      expect($state.go).toHaveBeenCalledWith 'welcome'
