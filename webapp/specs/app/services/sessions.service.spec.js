describe('SessionsService', function() {
  let SessionsService = undefined;
  let Restangular = undefined;
  let $http = undefined;
  let $httpBackend = undefined;
  let q = undefined;
  let $cookies = undefined; 

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function(_$httpBackend_, _$q_, _SessionsService_, _$http_, _Restangular_, _$cookies_) {
    SessionsService = _SessionsService_;
    Restangular = _Restangular_;
    $http = _$http_;
    $httpBackend = _$httpBackend_;
    q = _$q_;
    return $cookies = _$cookies_;
  }));


  describe('initialization', function() {
    it('sets @uriBase variable', () => expect(SessionsService.uriBase).toEqual('v1/sessions'));

    return it('sets @currentUserKey variable to undefined', () => expect(SessionsService.currentUserKey).toBeUndefined());
  });

  return describe('.login', function() {
    let expectedCredentials = {
      access_token: 'foobar_access_token',
      authuser: 'foobar_authuser',
      client_id: 'foobar_client_id',
      code: 'foobar_code',
      id_token: 'foobar_id_token',
      scope: 'foobar_scope',
      session_state: 'foobar_session_state',
      state: 'foobar_state',
      status: 'foobar_status',
      email: 'foobar_email',
      password: 'foobar_password'
    };
    let deferred = undefined;
    let result = undefined;
    let expectedCallbackResponse = {
      user: {
        key: '2837488f70g98708g9af678f6ga7df'
      }
    };

    beforeEach(() => deferred = q.defer());

    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      return $httpBackend.verifyNoOutstandingRequest();
    });

    return it('logs in to Stormpath and sets identity', function() {
      deferred.resolve(expectedCallbackResponse);
      $httpBackend.expectPOST('/login', expectedCredentials).respond(expectedCallbackResponse);
      let identityResponse = {email: "dwight.schrute@agosto.com"};
      $httpBackend.expectGET('/api/v1/identity').respond(identityResponse);
      result = SessionsService.login(expectedCredentials);
      $httpBackend.flush();
      return result.then(data => {
        return expect(SessionsService.getUserKey()).toEqual(expectedCallbackResponse.user.key);
      });
    });
  });
});
