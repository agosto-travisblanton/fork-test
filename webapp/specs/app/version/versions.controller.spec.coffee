'use strict'

describe 'VersionsCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  VersionsService = undefined
  promise = undefined


  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _VersionsService_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    VersionsService = _VersionsService_
    controller = $controller 'VersionsCtrl', {$state: $state, VersionsService: VersionsService}

  describe 'initialization', ->
    it 'versions should be an empty array', ->
      expect(angular.isArray(controller.versions)).toBeTruthy()

  describe '.initialize', ->
    versions = [
      {web_module_name: '18_aksdfjalksdfj'}
    ]

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(VersionsService, 'getVersions').and.returnValue promise

    it 'call VersionsService.getVersions to retrieve module versions', ->
      controller.initialize()
      promise.resolve versions
      expect(VersionsService.getVersions).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved versions in the controller", ->
      controller.initialize()
      promise.resolve versions
      expect(controller.versions).toBe versions
