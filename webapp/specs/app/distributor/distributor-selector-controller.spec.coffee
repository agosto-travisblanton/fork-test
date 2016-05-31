'use strict'

describe 'DistributorSelectorCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  promise = undefined
  $rootScope = undefined
  StorageService = undefined
  $scope = undefined
  $log = undefined
  ToastsService = undefined
  SessionsService = undefined
  DistributorsService = undefined
  DevicesService = undefined
  ProofPlayService = undefined
  TenantsService = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_,
    _$state_,
    _StorageService_
    _$rootScope_,
    _$log_,
    _DistributorsService_,
    _SessionsService_,
    _ToastsService_,
    _DevicesService_
    _ProofPlayService_
    _TenantsService_) ->
    $controller = _$controller_
    $state = _$state_
    StorageService = _StorageService_
    $rootScope = _$rootScope_
    $scope = _$rootScope_.$new()
    ToastsService = _ToastsService_
    $log = _$log_
    DistributorsService = _DistributorsService_
    SessionsService = _SessionsService_
    DevicesService = _DevicesService_
    ProofPlayService = _ProofPlayService_
    TenantsService = _TenantsService_
    controller = $controller 'DistributorSelectorCtrl', {
      $scope: $scope
      StorageService: _StorageService_
      $log: $log
      $state: $state
      ToastsService: ToastsService
      DistributorsService: DistributorsService
      SessionsService: SessionsService
      DevicesService: DevicesService
      ProofPlayService: ProofPlayService
      TenantsService: TenantsService
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
      promise = new skykitProvisioning.q.Mock()
      SessionsService.setUserKey(expectedCurrentUserKey)
      spyOn(DistributorsService, 'fetchAllByUser').and.callFake (currentUserKey) -> return promise
      spyOn(controller, 'selectDistributor')
      DevicesService.deviceCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }

      DevicesService.deviceByTenantCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }

      ProofPlayService.proofplayCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }

      TenantsService.tenantCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }
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
    distributor = {key: 'd78f9a0d89f7a0876ga7f6ga786g5a78df57d6f5a6dsf', name: 'some_distro'}

    beforeEach ->
      DevicesService.deviceCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }

      DevicesService.deviceByTenantCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }

      ProofPlayService.proofplayCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }

      TenantsService.tenantCache = {
        get: () ->

        put: () ->

        removeAll: () ->
      }
      spyOn($state, 'go')
      spyOn(ToastsService, 'showErrorToast')
      spyOn(DistributorsService, 'switchDistributor')
      spyOn(ToastsService, 'showSuccessToast')
      controller.selectDistributor(distributor)

    it 'sets the currentDistributor property', ->
      expect(DistributorsService.switchDistributor).toHaveBeenCalledWith distributor
      
