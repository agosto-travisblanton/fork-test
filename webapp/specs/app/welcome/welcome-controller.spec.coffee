'use strict'

describe 'WelcomeCtrl', ->
  $controller = undefined
  controller = undefined
  $rootScope = undefined
  $scope = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _$rootScope_) ->
    $controller = _$controller_
    $rootScope = _$rootScope_
    $scope = _$rootScope_.$new()

  describe 'initialization', ->
    beforeEach ->
      controller = $controller 'WelcomeCtrl', {
        $scope: $scope
      }

    it 'controller is created', ->
      expect(controller).toBeDefined()
