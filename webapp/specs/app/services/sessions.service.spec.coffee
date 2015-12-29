'use strict'

describe 'SessionsService', ->
  SessionsService = undefined
  Restangular = undefined
  $http = undefined
  $httpBackend = undefined
  q = undefined

  beforeEach module('skyKitProvisioning')

  beforeEach inject (_$httpBackend_, _$q_, _SessionsService_, _$http_, _Restangular_) ->
    SessionsService = _SessionsService_
    Restangular = _Restangular_
    $http = _$http_
    $httpBackend = _$httpBackend_
    q = _$q_


  describe 'initialization', ->
    it 'sets @uriBase variable', ->
      expect(SessionsService.uriBase).toEqual 'v1/sessions'

    it 'sets @currentUserKey variable to undefined', ->
      expect(SessionsService.currentUserKey).toBeUndefined()

  describe '.login', ->
    expectedCredentials = {
      access_token: 'foobar_access_token'
      authuser: 'foobar_authuser'
      client_id: 'foobar_client_id'
      code: 'foobar_code'
      id_token: 'foobar_id_token'
      scope: 'foobar_scope'
      session_state: 'foobar_session_state'
      state: 'foobar_state'
      status: 'foobar_status'
      email: 'foobar_email'
      password: 'foobar_password'
    }
    deferred = undefined
    result = undefined
    expectedCallbackResponse = {
      user:
        key: '2837488f70g98708g9af678f6ga7df'
    }

    beforeEach ->
      deferred = q.defer()

    afterEach () ->
      $httpBackend.verifyNoOutstandingExpectation()
      $httpBackend.verifyNoOutstandingRequest()

    it 'logs in to Stormpath', ->
      deferred.resolve expectedCallbackResponse
      $httpBackend.expectPOST('/login', expectedCredentials).respond(expectedCallbackResponse)
      result = SessionsService.login expectedCredentials
      $httpBackend.flush()
      expect(SessionsService.currentUserKey).toEqual expectedCallbackResponse.user.key
