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
      tab = {
        title: 'One-Resource',

      }
      tab2 = {
        title: "Multi-Resource"
      }
      expect(angular.equals(tab, controller.tab)).toBeTruthy()
      expect(angular.equals(tab2, controller.tab2)).toBeTruthy()