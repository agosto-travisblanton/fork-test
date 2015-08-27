'use strict'

describe 'WelcomeCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  DistributorsService = undefined
  promise = undefined
  identity = {CLIENT_ID: 'CLIENT-ID', STATE: 'STATE'}
  $rootScope = undefined
  $scope = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _$state_, _$rootScope_, _DistributorsService_) ->
    $controller = _$controller_
    $state = _$state_
    $rootScope = _$rootScope_
    $scope = _$rootScope_.$new()
    DistributorsService = _DistributorsService_
    spyOn($scope, '$on')
    controller = $controller 'WelcomeCtrl', {
      $state: $state
      $scope: $scope
      DistributorsService: DistributorsService
      identity: identity
    }


  describe 'initialization', ->
    it 'currentDistributor is undefined', ->
      expect(controller.currentDistributor).toBeUndefined()

    it 'distributors should be an empty array', ->
      expect(angular.isArray(controller.distributors)).toBeTruthy()

    it "add listener for 'event:google-plus-signin-success' event", ->
      expect($scope.$on).toHaveBeenCalledWith 'event:google-plus-signin-success', jasmine.any(Function)

    it "add listener for 'event:google-plus-signin-failure' event", ->
      expect($scope.$on).toHaveBeenCalledWith 'event:google-plus-signin-failure', jasmine.any(Function)

  describe '.initialize', ->
    distributors = [
      {key: 'dhjad897d987fadafg708fg7d', name: 'Agosto, Inc.', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'dhjad897d987fadafg708y67d', name: 'Tierney Bros., Inc.', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DistributorsService, 'fetchAll').and.returnValue promise
      controller.initialize()
      promise.resolve distributors

    it 'call DistributorsService.fetchAll() to retrieve all distributors', ->
      expect(DistributorsService.fetchAll).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved distributors in the controller", ->
      expect(controller.distributors).toBe distributors

    it 'sets the clientId property on the controller', ->
      expect(controller.clientId).toBe identity.CLIENT_ID

    it 'sets the state property on the controller', ->
      expect(controller.state).toBe identity.STATE


  describe '.selectDistributor', ->
    distributor = {
      key: 'dhjad897d987fadafg708fg7d',
      name: 'Agosto, Inc.',
      created: '2015-05-10 22:15:10',
      updated: '2015-05-10 22:15:10'
    }

    beforeEach ->
      controller.currentDistributor = distributor

    it 'sets the current distributor on the DistributorsService', ->
      controller.selectDistributor()
      expect(DistributorsService.currentDistributor).toBe distributor
