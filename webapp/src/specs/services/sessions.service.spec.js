import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject


describe('SessionsService', function () {
  let SessionsService = undefined;
  let Restangular = undefined;
  let $http = undefined;
  let $httpBackend = undefined;
  let q = undefined;
  let $cookies = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$httpBackend_, _$q_, _SessionsService_, _$http_, _Restangular_, _$cookies_) {
    SessionsService = _SessionsService_;
    Restangular = _Restangular_;
    $http = _$http_;
    $httpBackend = _$httpBackend_;
    q = _$q_;
    return $cookies = _$cookies_;
  }));


  describe('initialization', function () {
    it('sets @uriBase variable', () => expect(SessionsService.uriBase).toEqual('v1/sessions'));

    return it('sets @currentUserKey variable to undefined', () => expect(SessionsService.currentUserKey).toBeUndefined());
  });

  describe('.login', function () {
    let deferred = undefined;
    let expectedCallbackResponse = {
      data: {
        token: 'eyJleHAiOjQ2MjQyMTAyNzMsImlhdCI6MTQ3OTI1MDI3MywiYWxnIjoiSFMyNTYifQ.eyJpc19sb2dnZWRfaW4iOnRydWUsImtleSI6ImFoMWtaWFotYzJ0NWEybDBMV1JwYzNCc1lYa3RaR1YyYVdObExXbHVkSElqQ3hJRVZYTmxjaUlaWkdGdWFXVnNMblJsY201NVlXdEFZV2R2YzNSdkxtTnZiUXciLCJpc19hZG1pbiI6dHJ1ZSwiZGlzdHJpYnV0b3JzIjpbIk1pZmZsaW4iLCJEdW5kZXIiLCJTY3JhbnRvbiJdLCJlbWFpbCI6ImRhbmllbC50ZXJueWFrQGFnb3N0by5jb20iLCJkaXN0cmlidXRvcnNfYXNfYWRtaW4iOlsiTWlmZmxpbiIsIkR1bmRlciIsIlNjcmFudG9uIl19.HBspomnaabOvV4j0jPv6NNUMWoUa2PptTmExQv9kaC0'
      }
    };

    beforeEach(() => deferred = q.defer());

    afterEach(function () {
      $httpBackend.verifyNoOutstandingExpectation();
      return $httpBackend.verifyNoOutstandingRequest();
    });

    it('exchanges oAuth for JWT', function () {
      $httpBackend.when('GET', '/api/v1/login').respond(() => expectedCallbackResponse);
      let result = SessionsService.login({
        id_token: '2lk34jl3k4j2l34jjkl2433k4'
      });

      $httpBackend.flush();
      result.then(() => {
        expect(SessionsService.getIsAdmin()).toBeTruthy()
        expect(SessionsService.getUserEmail()).toEqual('daniel.ternyak@agosto.com')
      })
    });
  });
});
