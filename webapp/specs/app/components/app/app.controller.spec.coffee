'use strict'

describe 'AppController', ->
  $controller = undefined
  controller = undefined
  $mdSidenav('left').isOpen
  $state = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _$state_) ->
    $controller = _$controller_
    $state = _$state_

  describe '.goTo', ->
    stateName = 'devices'
    id = 5
    idParam = ({id: id})

    beforeEach ->
      spyOn($state, 'go')
      controller = $controller 'AppController'
      controller.goTo stateName, id

    it "navigates to route with stateName and id", ->
      expect($state.go).toHaveBeenCalledWith stateName, idParam
