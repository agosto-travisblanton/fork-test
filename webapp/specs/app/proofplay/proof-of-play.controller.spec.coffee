'use strict'

describe 'ProofOfPlayCtrl', ->
  $controller = undefined
  controller = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_) ->
    $controller = _$controller_
    controller = $controller 'ProofOfPlayCtrl'

  describe 'at the start', ->
    it 'tab dict values should equal', ->
      resource = {
        title: 'Resource',

      }
      expect(angular.equals(resource, controller.resource)).toBeTruthy()
