'use strict'

describe 'AppController', ->
  $controller = undefined
  controller = undefined
  $mdSidenav = undefined
  $state = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _$state_, _$mdSidenav_) ->
    $controller = _$controller_
    $state = _$state_
    $mdSidenav = _$mdSidenav_

#  vm.goTo = (stateName, id) ->
#    $state.go stateName, {id: id}
#    $mdSidenav('left').close() if $mdSidenav('left').isOpen()


  describe '.goTo', ->
    stateName = 'devices'
    id = 5
    idParam = ({id: id})

    beforeEach ->
      spyOn($state, 'go')
      spyOn($mdSidenav('left'), 'isOpen').and.returnValue false
      spyOn($mdSidenav('left'), 'close')
      controller = $controller 'AppController'
      controller.goTo stateName, id

    it "navigates to route with stateName and id", ->
      expect($state.go).toHaveBeenCalledWith stateName, idParam
