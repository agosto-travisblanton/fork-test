'use strict'

describe 'WelcomeCtrl', ->
  controller = undefined
  promise = undefined
  otherPromise = undefined
  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _VersionsService_, _$state_, _StorageService_, _SessionsService_, _DistributorsService_) ->
    controller = _$controller_ 'WelcomeCtrl', {
      VersionsService: _VersionsService_,
      StorageService: _StorageService_,
      SessionsService: _SessionsService_,
      $stateParams: {},
      $state: _$state_,
      DistributorsService: _DistributorsService_
    }

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
      otherPromise = new skykitProvisioning.q.Mock
      spyOn($state, 'go')
      StorageService.removeAll()
      spyOn(VersionsService, 'getVersions').and.returnValue promise
      spyOn(DistributorsService, 'fetchAllByUser').and.returnValue otherPromise

    it 'call VersionsService.getVersions to retrieve module version with auth', ->
      StorageService.set("userEmail", "some.user@demo.agosto.com")
      controller.initialize()
      otherPromise.resolve versionData
      expect(VersionsService.getVersions).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved version data on the controller with auth", ->
      StorageService.set("userEmail", "some.user@demo.agosto.com")
      controller.initialize()
      otherPromise.resolve versionData
      promise.resolve versionData
      expect(controller.version_data).toBe versionData

    it 'call VersionsService.getVersions to retrieve module version without auth', ->
      controller.initialize()
      expect($state.go).toHaveBeenCalledWith('sign_in')


    it "goes to sign in view when hit", ->
      controller.proceedToSignIn()
      expect($state.go).toHaveBeenCalledWith('sign_in')
