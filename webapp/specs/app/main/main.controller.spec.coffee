'use strict'

describe 'MainCtrl', ->
  scope = undefined
  $rootScope = undefined
  controller = undefined

  beforeEach module('skyKitProvisioning')

  beforeEach inject (_$controller_, _$rootScope_) ->
    $rootScope = _$rootScope_
    scope = $rootScope.$new()
    controller = _$controller_('MainCtrl', $scope: scope)

  it 'should define more than 5 awesome things', ->
    expect(angular.isArray(scope.awesomeThings)).toBeTruthy()
    expect(scope.awesomeThings.length > 5).toBeTruthy()

