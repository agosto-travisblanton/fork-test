'use strict'

describe 'DisplaysListingCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  DisplaysService = undefined
  promise = undefined
  displays = [
    {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]


  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _DisplaysService_, _$stateParams_) ->
    $controller = _$controller_
    $stateParams = _$stateParams_
    DisplaysService = _DisplaysService_

  describe 'initialization', ->
    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DisplaysService, 'getDisplays').and.returnValue promise
      controller = $controller 'DisplaysListingCtrl', {$stateParams: $stateParams, DisplaysService: DisplaysService}

    it 'displays should be an empty array', ->
      expect(angular.isArray(controller.displays)).toBeTruthy()

    it 'call DisplaysService.getDisplays to retrieve all displays', ->
      expect(DisplaysService.getDisplays).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved displays in the controller", ->
      promise.resolve displays
      expect(controller.displays).toBe displays

