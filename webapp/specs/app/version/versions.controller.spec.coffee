'use strict'

describe 'VersionsCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  VersionsService = undefined
  promise = undefined
  versionData = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _VersionsService_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    VersionsService = _VersionsService_
    controller = $controller 'VersionsCtrl', {$state: $state, VersionsService: VersionsService}

  describe 'initialization', ->
    it 'version_data should be an empty array', ->
      expect(angular.isArray(controller.version_data)).toBeTruthy()

  describe '.initialize', ->
    versionData = [
      {
        web_version_name: 'snapshot',
        web_module_name: 'default',
        current_instance_id: '7bedeb21a1a3191ca8c5cd3dea9c99c0abee',
        default_version: 'snapshot',
        hostname: '127.0.0.1:8080'
      }
    ]

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(VersionsService, 'getVersions').and.returnValue promise

    it 'call VersionsService.getVersions to retrieve module version', ->
      controller.initialize()
      expect(VersionsService.getVersions).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved version data in the controller", ->
      controller.initialize()
      promise.resolve versionData
      expect(controller.version_data).toBe versionData
