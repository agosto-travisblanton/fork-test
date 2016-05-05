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
  $timeoutMock = {
    timeout: (callback, lapse) ->
      setTimeout(callback, lapse)
  }
  sweet = undefined
  SessionsService = undefined
  ProgressBarService = undefined

  beforeEach module('skykitProvisioning')

  beforeEach module(($provide) ->
    $provide.decorator '$timeout',
      ($delegate) ->
        (callback, lapse) ->
          $timeoutMock.timeout callback, lapse
          $delegate.apply(this, arguments)
  )

  beforeEach inject (_$controller_,
    _$state_,
    _$rootScope_,
    _$log_,
    _sweet_,
    _SessionsService_,
    _ProgressBarService_) ->
    $controller = _$controller_
    $state = _$state_
    $rootScope = _$rootScope_
    $scope = _$rootScope_.$new()
    $log = _$log_
    sweet = _sweet_
    SessionsService = _SessionsService_
    ProgressBarService = _ProgressBarService_
    spyOn($scope, '$on')
    controller = $controller 'AuthenticationCtrl', {
      $scope: $scope
      $log: $log
      $state: $state
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
      promise = new skykitProvisioning.q.Mock()
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
    authResult = {}
    event = {}
    loginResponse = {}
    promise = undefined

    beforeEach ->
      promise = new skykitProvisioning.q.Mock()
      spyOn(ProgressBarService, 'complete')
      spyOn(sweet, 'show')

    describe "Google Plus sign in button clicked", ->
      beforeEach ->
        controller.googlePlusSignInButtonClicked = true
        controller.onGooglePlusSignInFailure event, authResult

      it "complete the progress bar", ->
        expect(ProgressBarService.complete).toHaveBeenCalled()

      it "show the error dialog", ->
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', 'Unable to authenticate to Google+.', 'error'

    describe "Google Plus sign in button not clicked", ->
      beforeEach ->
        controller.googlePlusSignInButtonClicked = false
        controller.onGooglePlusSignInFailure event, authResult

      it "does not complete the progress bar", ->
        expect(ProgressBarService.complete).not.toHaveBeenCalled()

      it "does not show the error dialog", ->
        expect(sweet.show).not.toHaveBeenCalled()


  describe '.initializeSignIn', ->
    beforeEach ->
      controller.initializeSignIn()

    it "initializes the clientId variable with identity OAuth client ID", ->
      expect(controller.clientId).toBe identity.OAUTH_CLIENT_ID

    it "initializes the state variable with identity state", ->
      expect(controller.state).toBe identity.STATE

    it "initializes the googlePlusSignInButtonClicked variable to false", ->
      expect(controller.googlePlusSignInButtonClicked).toBeFalsy()


  describe '.initializeSignOut', ->
    beforeEach ->
      spyOn(SessionsService, 'removeUserInfo')
      spyOn($timeoutMock, 'timeout').and.callFake (callback) -> callback()
      spyOn(controller, 'proceedToSignIn').and.callFake ->
      spyOn(controller, 'proceedToSignedOut').and.callFake ->
      controller.initializeSignOut()

    it "calls SessionsService.removeUserInfo ", ->
      expect(SessionsService.removeUserInfo).toHaveBeenCalled()

    it "calls $timeout with the proceed with signed out function and delay", ->
      expect($timeoutMock.timeout).toHaveBeenCalledWith controller.proceedToSignedOut, 1500

    it "calls proceedToSignedOut after timeout delay", ->
      expect(controller.proceedToSignedOut).toHaveBeenCalled()


  describe '.loginSuccess', ->
    response = {}

    beforeEach ->
      spyOn(ProgressBarService, 'complete')
      spyOn(SessionsService, 'setIdentity')
      spyOn($state, 'go').and.callFake (name) ->
      controller.loginSuccess(response)

    it "completes the progress bar", ->
      expect(ProgressBarService.complete).toHaveBeenCalled()

    it "routes to the distributor selection route", ->
      expect($state.go).toHaveBeenCalledWith 'distributor_selection'


  describe '.loginFailure', ->
    response = {}

    beforeEach ->
      spyOn(ProgressBarService, 'complete')
      spyOn(sweet, 'show')
      controller.loginFailure(response)

    it "completes the progress bar", ->
      expect(ProgressBarService.complete).toHaveBeenCalled()

    it "show error dialog", ->
      expect(sweet.show).toHaveBeenCalledWith 'Oops...', 'Unable to authenticate to Stormpath.', 'error'


  describe '.proceedToSignIn', ->
    beforeEach ->
      spyOn($state, 'go').and.callFake (name) ->
      controller.proceedToSignIn()

    it "specifies ui-router go to the sign in route", ->
      expect($state.go).toHaveBeenCalledWith 'sign_in'


  describe '.onClickGooglePlusSignIn', ->
    beforeEach ->
      controller.googlePlusSignInButtonClicked = false
      spyOn(ProgressBarService, 'start')
      controller.onClickGooglePlusSignIn()

    it "sets the googlePlusSignInButtonClicked instance variable to true", ->
      expect(controller.googlePlusSignInButtonClicked).toBeTruthy()

    it "starts the progress bar animation", ->
      expect(ProgressBarService.start).toHaveBeenCalled()
