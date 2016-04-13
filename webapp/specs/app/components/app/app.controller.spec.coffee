'use strict'

describe 'AppController', ->
  $controller = undefined
  controller = undefined
  $mdSidenav = undefined
  mock_nav = () ->
    {
      close: ->
        true
      isOpen: ->
        true
    }
  $state = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    $mdSidenav = mock_nav()

#  vm.goTo = (stateName, id) ->
#    $state.go stateName, {id: id}
#    $mdSidenav('left').close() if $mdSidenav('left').isOpen()
#  spyOn could not find an object to spy upon for isOpen()
#$mdSidenav('left').isOpen()

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
