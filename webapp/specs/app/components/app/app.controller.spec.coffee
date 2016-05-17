'use strict'

describe 'AppController', ->
  beforeEach module('skykitProvisioning')

  $controller = undefined
  controller = undefined
  $window = undefined
  $mdSidenav = undefined
  $state = undefined
  SessionsService = undefined

  sideNavFunction = {
    toggle: ->
    close: ->
    isOpen: -> true
  }

  beforeEach module ($provide) ->
    $provide.decorator '$mdSidenav', ($delegate) ->
      sideNavSpy = jasmine.createSpy($delegate).and.returnValue sideNavFunction
      sideNavSpy


  beforeEach inject (_$controller_, _$state_, _$mdSidenav_, _$window_, _SessionsService_) ->
    $controller = _$controller_
    $state = _$state_
    $mdSidenav = _$mdSidenav_
    $window = _$window_
    SessionsService = _SessionsService_

  describe '.initialize', ->
    beforeEach ->
      controller = $controller 'AppController', {SessionsService: SessionsService}
      spyOn(controller, 'getIdentity')
      controller.initialize()

    it 'calls getIdentity', ->
      expect(controller.getIdentity).toHaveBeenCalled()

    it 'determines isCurrentURLDistributorSelector', ->
      a = controller.isCurrentURLDistributorSelector()
      expect(a).toBe false


  describe '.toggleSidenav', ->
    beforeEach ->
      controller = $controller 'AppController'
      spyOn(sideNavFunction, 'toggle')
      controller.toggleSidenav()

    it 'invokes $mdSidenav with direction left', ->
      expect($mdSidenav).toHaveBeenCalledWith 'left'

    it 'invokes the toggle function on result of $mdSidenav', ->
      expect(sideNavFunction.toggle).toHaveBeenCalled()

  describe '.goTo', ->
    stateName = 'devices'
    id = 5
    idParam = ({id: id})

    beforeEach ->
      spyOn($state, 'go')
      spyOn(sideNavFunction, 'close')
      controller = $controller 'AppController'

    it 'navigates to route with stateName and id', ->
      controller.goTo stateName, id
      expect($state.go).toHaveBeenCalledWith stateName, idParam

    it 'invokes $mdSidenav.close when $mdSidenav.isOpen is true', ->
      controller.goTo stateName, id
      expect(sideNavFunction.close).toHaveBeenCalled()

    it 'will not invoke $mdSidenav.close when $mdSidenav.isOpen is false', ->
      spyOn(sideNavFunction, 'isOpen').and.returnValue false
      controller.goTo stateName, id
      expect(sideNavFunction.close).not.toHaveBeenCalled()
