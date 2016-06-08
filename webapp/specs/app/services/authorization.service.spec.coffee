'use strict'

describe 'AuthorizationService', ->
  beforeEach module 'skykitProvisioning'
  SessionsService = undefined
  AuthorizationService = undefined
  $q = undefined
  promise = undefined

  beforeEach inject (_SessionsService_, _$q_, _AuthorizationService_) ->
    SessionsService = _SessionsService_
    $q = _$q_
    AuthorizationService = _AuthorizationService_

  describe 'AuthorizationService as Admin User', ->
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(SessionsService, 'getUserKey').and.returnValue true
      spyOn(SessionsService, 'getDistributorsAsAdmin').and.returnValue true
      spyOn(SessionsService, 'getIsAdmin').and.returnValue true

    it '.authenticated resolves', ->
      toResolve = AuthorizationService.authenticated()
      toResolve.then (data) ->
        expect(data).toEqual true

    it '.notAuthenticated rejects', ->
      toResolve = AuthorizationService.notAuthenticated()
      toResolve.then (data) ->
        expect(data).toEqual ["authError", 'home']
        

    it '.notAuthenticated resolves', ->
      toResolve = AuthorizationService.isAdminOrDistributorAdmin()
      toResolve.then (data) ->
        expect(data).toEqual true
        
  describe 'AuthorizationService as logged out', ->
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(SessionsService, 'getUserKey').and.returnValue false
      spyOn(SessionsService, 'getDistributorsAsAdmin').and.returnValue false
      spyOn(SessionsService, 'getIsAdmin').and.returnValue false

    it '.authenticated resolves', ->
      toResolve = AuthorizationService.authenticated()
      toResolve.then (data) ->
        expect(data).toEqual ["authError", 'sign_in']

    it '.notAuthenticated rejects', ->
      toResolve = AuthorizationService.notAuthenticated()
      toResolve.then (data) ->
        expect(data).toEqual true
        

    it '.notAuthenticated resolves', ->
      toResolve = AuthorizationService.isAdminOrDistributorAdmin()
      toResolve.then (data) ->
        expect(data).toEqual ["authError", 'sign_in']