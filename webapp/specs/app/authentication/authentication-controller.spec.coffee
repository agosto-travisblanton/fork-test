'use strict'

describe 'AuthenticationCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  promise = undefined
  identity = {OAUTH_CLIENT_ID: 'CLIENT-ID', STATE: 'STATE'}
  $rootScope = undefined
  $scope = undefined
  $log = undefined
  $timeout = undefined
  identity = undefined
  sweet = undefined
  SessionsService = undefined
  ProgressBarService = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_,
                     _$state_,
                     _$rootScope_,
                     _$log_,
                     _$timeout_,
                     _sweet_,
                     _SessionsService_,
                     _ProgressBarService_) ->
    $controller = _$controller_
    $state = _$state_
    $rootScope = _$rootScope_
    $scope = _$rootScope_.$new()
    $log = _$log_
    $timeout = _$timeout_
    sweet = _sweet_
    SessionsService = _SessionsService_
    ProgressBarService = _ProgressBarService_
    spyOn($scope, '$on')
    controller = $controller 'AuthenticationCtrl', {
      $scope: $scope
      $log: $log
      $state: $state
      $timeout: $timeout
      identity: identity
      sweet: sweet
      SessionsService: SessionsService
      ProgressBarService: ProgressBarService
    }

  describe 'initialization', ->
    it "add listener for 'event:google-plus-signin-success' event", ->
      expect($scope.$on).toHaveBeenCalledWith 'event:google-plus-signin-success', jasmine.any(Function)

    it "add listener for 'event:google-plus-signin-failure' event", ->
      expect($scope.$on).toHaveBeenCalledWith 'event:google-plus-signin-failure', jasmine.any(Function)


  describe '.onGooglePlusSignInSuccess', ->
    authResult = {}
    event = {}
    loginResponse = {}
    promise = undefined

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock()
      spyOn(ProgressBarService, 'start')
      spyOn(SessionsService, 'login').and.callFake (authResult) -> return promise
      spyOn(controller, 'loginSuccess').and.callFake (response) ->
      spyOn(controller, 'loginFailure').and.callFake (response) ->

    describe "Google Plus sign in button clicked", ->
      beforeEach ->
        controller.googlePlusSignInButtonClicked = true
        controller.onGooglePlusSignInSuccess event, authResult

      it "do not start the progress bar", ->
        promise.resolve loginResponse
        expect(ProgressBarService.start).not.toHaveBeenCalled()

      it "call SessionsService.login to sign into Stormpath", ->
        promise.resolve loginResponse
        expect(SessionsService.login).toHaveBeenCalledWith authResult

      it "invoke loginSuccess when the login promise resolves successfully", ->
        promise.resolve loginResponse
        expect(controller.loginSuccess).toHaveBeenCalledWith loginResponse

      it "invoke loginFailure when the login promise fails to resolve", ->
        promise.reject loginResponse
        expect(controller.loginFailure).toHaveBeenCalledWith loginResponse


    describe "Google Plus sign in button not clicked", ->
      beforeEach ->
        controller.googlePlusSignInButtonClicked = false
        controller.onGooglePlusSignInSuccess event, authResult

      it "start the progress bar", ->
        promise.resolve loginResponse
        expect(ProgressBarService.start).toHaveBeenCalled()

      it "call SessionsService.login to sign into Stormpath", ->
        promise.resolve loginResponse
        expect(SessionsService.login).toHaveBeenCalledWith authResult

      it "invoke loginSuccess when the login promise resolves successfully", ->
        promise.resolve loginResponse
        expect(controller.loginSuccess).toHaveBeenCalledWith loginResponse

      it "invoke loginFailure when the login promise fails to resolve", ->
        promise.reject loginResponse
        expect(controller.loginFailure).toHaveBeenCalledWith loginResponse


  describe '.onGooglePlusSignInFailure', ->
    beforeEach ->

    it "", ->





