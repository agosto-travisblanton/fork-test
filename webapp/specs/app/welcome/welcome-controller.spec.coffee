'use strict'

describe 'WelcomeCtrl', ->
  $controller = undefined
  controller = undefined
  VersionsService = undefined
  promise = undefined
  versionData = undefined
  cookieMock = undefined
  $stateParams = undefined
  $state = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _VersionsService_, _$state_) ->
    $controller = _$controller_
    VersionsService = _VersionsService_
    $stateParams = {}
    $state = {}
    $state = _$state_
    cookieMock = {
      storage: {},
      put: (key, value) ->
        this.storage[key] = value
      get: (key) ->
        return this.storage[key]
    }
    controller = $controller 'WelcomeCtrl', {
      VersionsService: VersionsService,
      $cookies: cookieMock,
      $stateParams: $stateParams,
      $state: $state
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
      spyOn($state, 'go')
      spyOn(VersionsService, 'getVersions').and.returnValue promise

    it 'call VersionsService.getVersions to retrieve module version with auth', ->
      cookieMock.put("userEmail", "some.user@demo.agosto.com")
      controller.initialize()
      expect(VersionsService.getVersions).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved version data on the controller with auth", ->
      cookieMock.put("userEmail", "some.user@demo.agosto.com")
      controller.initialize()
      promise.resolve versionData
      expect(controller.version_data).toBe versionData

    it 'call VersionsService.getVersions to retrieve module version without auth', ->
      controller.initialize()
      expect($state.go).toHaveBeenCalledWith('sign_in')


    it "the 'then' handler caches the retrieved version data on the controller without auth", ->
      controller.initialize()
      expect($state.go).toHaveBeenCalledWith('sign_in')


    it "goes to sign in view when hit", ->
      controller.proceedToSignIn()
      expect($state.go).toHaveBeenCalledWith('sign_in')
