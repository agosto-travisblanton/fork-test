'use strict'

describe 'WelcomeCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  DistributorsService = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _$state_, _DistributorsService_) ->
    $controller = _$controller_
    $state = _$state_
    DistributorsService = _DistributorsService_
    controller = $controller 'WelcomeCtrl', {$state: $state, DistributorsService: DistributorsService}

  describe 'initialization', ->
    it 'controller is defined', ->
      expect(controller).toBeDefined()

    it 'distributors should be an empty array', ->
      expect(angular.isArray(controller.distributors)).toBeTruthy()

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



