'use strict';
describe('AuthenticationCtrl', function () {
  var $controller, $log, $rootScope, $scope, $state, $timeoutMock, DevicesService, ProgressBarService, ProofPlayService, SessionsService, TenantsService, controller, identity, promise, sweet;
  $controller = void 0;
  controller = void 0;
  $state = void 0;
  promise = void 0;
  identity = {
    OAUTH_CLIENT_ID: 'CLIENT-ID',
    STATE: 'STATE'
  };
  $rootScope = void 0;
  $scope = void 0;
  $log = void 0;
  DevicesService = void 0;
  ProofPlayService = void 0;
  TenantsService = void 0;
  $timeoutMock = {
    timeout: function (callback, lapse) {
      return setTimeout(callback, lapse);
    }
  };
  sweet = void 0;
  SessionsService = void 0;
  ProgressBarService = void 0;
  beforeEach(module('skykitProvisioning'));
  beforeEach(module(function ($provide) {
    return $provide.decorator('$timeout', function ($delegate) {
      return function (callback, lapse) {
        $timeoutMock.timeout(callback, lapse);
        return $delegate.apply(this, arguments);
      };
    });
  }));
  beforeEach(inject(function (_$controller_, _$state_, _$rootScope_, _$log_, _sweet_, _SessionsService_, _ProgressBarService_, _DevicesService_, _ProofPlayService_, _TenantsService_) {
    $controller = _$controller_;
    $state = _$state_;
    $rootScope = _$rootScope_;
    $scope = _$rootScope_.$new();
    $log = _$log_;
    sweet = _sweet_;
    SessionsService = _SessionsService_;
    ProgressBarService = _ProgressBarService_;
    DevicesService = _DevicesService_;
    ProofPlayService = _ProofPlayService_;
    TenantsService = _TenantsService_;
    spyOn($scope, '$on');
    return controller = $controller('AuthenticationCtrl', {
      $scope: $scope,
      $log: $log,
      $state: $state,
      identity: identity,
      sweet: sweet,
      SessionsService: SessionsService,
      ProgressBarService: ProgressBarService,
      DevicesService: DevicesService,
      ProofPlayService: ProofPlayService,
      TenantsService: TenantsService
    });
  }));
  describe('initialization', function () {
    it("add listener for 'event:google-plus-signin-success' event", function () {
      return expect($scope.$on).toHaveBeenCalledWith('event:google-plus-signin-success', jasmine.any(Function));
    });
    return it("add listener for 'event:google-plus-signin-failure' event", function () {
      return expect($scope.$on).toHaveBeenCalledWith('event:google-plus-signin-failure', jasmine.any(Function));
    });
  });
  describe('.onGooglePlusSignInSuccess', function () {
    var authResult, event, loginResponse;
    authResult = {};
    event = {};
    loginResponse = {};
    promise = void 0;
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(ProgressBarService, 'start');
      spyOn(SessionsService, 'login').and.callFake(function (authResult) {
        return promise;
      });
      spyOn(controller, 'loginSuccess').and.callFake(function (response) {
      });
      return spyOn(controller, 'loginFailure').and.callFake(function (response) {
      });
    });
    describe("Google Plus sign in button clicked", function () {
      beforeEach(function () {
        controller.googlePlusSignInButtonClicked = true;
        return controller.onGooglePlusSignInSuccess(event, authResult);
      });
      it("do not start the progress bar", function () {
        promise.resolve(loginResponse);
        return expect(ProgressBarService.start).not.toHaveBeenCalled();
      });
      it("call SessionsService.login to sign into Stormpath", function () {
        promise.resolve(loginResponse);
        return expect(SessionsService.login).toHaveBeenCalledWith(authResult);
      });
      it("invoke loginSuccess when the login promise resolves successfully", function () {
        promise.resolve(loginResponse);
        return expect(controller.loginSuccess).toHaveBeenCalledWith(loginResponse);
      });
      return it("invoke loginFailure when the login promise fails to resolve", function () {
        promise.reject(loginResponse);
        return expect(controller.loginFailure).toHaveBeenCalledWith(loginResponse);
      });
    });
    return describe("Google Plus sign in button not clicked", function () {
      beforeEach(function () {
        controller.googlePlusSignInButtonClicked = false;
        return controller.onGooglePlusSignInSuccess(event, authResult);
      });
      it("start the progress bar", function () {
        promise.resolve(loginResponse);
        return expect(ProgressBarService.start).toHaveBeenCalled();
      });
      it("call SessionsService.login to sign into Stormpath", function () {
        promise.resolve(loginResponse);
        return expect(SessionsService.login).toHaveBeenCalledWith(authResult);
      });
      it("invoke loginSuccess when the login promise resolves successfully", function () {
        promise.resolve(loginResponse);
        return expect(controller.loginSuccess).toHaveBeenCalledWith(loginResponse);
      });
      return it("invoke loginFailure when the login promise fails to resolve", function () {
        promise.reject(loginResponse);
        return expect(controller.loginFailure).toHaveBeenCalledWith(loginResponse);
      });
    });
  });
  describe('.onGooglePlusSignInFailure', function () {
    var authResult, event, loginResponse;
    authResult = {};
    event = {};
    loginResponse = {};
    promise = void 0;
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(ProgressBarService, 'complete');
      return spyOn(sweet, 'show');
    });
    describe("Google Plus sign in button clicked", function () {
      beforeEach(function () {
        controller.googlePlusSignInButtonClicked = true;
        return controller.onGooglePlusSignInFailure(event, authResult);
      });
      it("complete the progress bar", function () {
        return expect(ProgressBarService.complete).toHaveBeenCalled();
      });
      return it("show the error dialog", function () {
        return expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to authenticate to Google+.', 'error');
      });
    });
    return describe("Google Plus sign in button not clicked", function () {
      beforeEach(function () {
        controller.googlePlusSignInButtonClicked = false;
        return controller.onGooglePlusSignInFailure(event, authResult);
      });
      it("does not complete the progress bar", function () {
        return expect(ProgressBarService.complete).not.toHaveBeenCalled();
      });
      return it("does not show the error dialog", function () {
        return expect(sweet.show).not.toHaveBeenCalled();
      });
    });
  });
  describe('.initializeSignIn', function () {
    beforeEach(function () {
      return controller.initializeSignIn();
    });
    it("initializes the clientId variable with identity OAuth client ID", function () {
      return expect(controller.clientId).toBe(identity.OAUTH_CLIENT_ID);
    });
    it("initializes the state variable with identity state", function () {
      return expect(controller.state).toBe(identity.STATE);
    });
    return it("initializes the googlePlusSignInButtonClicked variable to false", function () {
      return expect(controller.googlePlusSignInButtonClicked).toBeFalsy();
    });
  });
  describe('.initializeSignOut', function () {
    beforeEach(function () {
      spyOn(SessionsService, 'removeUserInfo');
      spyOn($timeoutMock, 'timeout').and.callFake(function (callback) {
        return callback();
      });
      spyOn(controller, 'proceedToSignIn').and.callFake(function () {
      });
      spyOn(controller, 'proceedToSignedOut').and.callFake(function () {
      });
      return controller.initializeSignOut();
    });
    it("calls SessionsService.removeUserInfo ", function () {
      return expect(SessionsService.removeUserInfo).toHaveBeenCalled();
    });
    it("calls $timeout with the proceed with signed out function and delay", function () {
      return expect($timeoutMock.timeout).toHaveBeenCalledWith(controller.proceedToSignedOut, 50);
    });
    return it("calls proceedToSignedOut after timeout delay", function () {
      return expect(controller.proceedToSignedOut).toHaveBeenCalled();
    });
  });
  describe('.loginSuccess', function () {
    var response;
    response = {};
    beforeEach(function () {

      spyOn(ProgressBarService, 'complete');
      spyOn(SessionsService, 'setIdentity');
      spyOn($state, 'go').and.callFake(function (name) {
      });
      return controller.loginSuccess(response);
    });
    it("completes the progress bar", function () {
      return expect(ProgressBarService.complete).toHaveBeenCalled();
    });
    return it("routes to the distributor selection route", function () {
      return expect($state.go).toHaveBeenCalledWith('distributor_selection');
    });
  });
  describe('.loginFailure', function () {
    var response;
    response = {};
    beforeEach(function () {
      spyOn(ProgressBarService, 'complete');
      spyOn(sweet, 'show');
      return controller.loginFailure(response);
    });
    it("completes the progress bar", function () {
      return expect(ProgressBarService.complete).toHaveBeenCalled();
    });
    return it("show error dialog", function () {
      return expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to authenticate to Stormpath.', 'error');
    });
  });
  describe('.proceedToSignIn', function () {
    beforeEach(function () {
      spyOn($state, 'go').and.callFake(function (name) {
      });
      return controller.proceedToSignIn();
    });
    return it("specifies ui-router go to the sign in route", function () {
      return expect($state.go).toHaveBeenCalledWith('sign_in');
    });
  });
  return describe('.onClickGooglePlusSignIn', function () {
    beforeEach(function () {
      controller.googlePlusSignInButtonClicked = false;
      spyOn(ProgressBarService, 'start');
      return controller.onClickGooglePlusSignIn();
    });
    it("sets the googlePlusSignInButtonClicked instance variable to true", function () {
      return expect(controller.googlePlusSignInButtonClicked).toBeTruthy();
    });
    return it("starts the progress bar animation", function () {
      return expect(ProgressBarService.start).toHaveBeenCalled();
    });
  });
});

// ---
// generated by coffee-script 1.9.2
