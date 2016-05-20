'use strict'

angular.module('skykitProvisioning').factory 'SessionsService', ($http,
  $log,
  $cookies,
  IdentityService,
  Restangular,
  $q) ->
  new class SessionsService

    constructor: ->
      @uriBase = 'v1/sessions'
      @currentUserKey = undefined or Lockr.get('userKey')

    setDistributors: (distributors) =>
      Lockr.set('distributors', distributors)

    setDistributorsAsAdmin: (distributorsAsAdmin) =>
      Lockr.set('distributorsAsAdmin', distributorsAsAdmin)

    setIsAdmin: (isAdmin) =>
      Lockr.set('isAdmin', isAdmin)

    getDistributors: () =>
      Lockr.get('distributors')

    getCurrentDistributorName: () ->
      Lockr.get('currentDistributorName')

    getCurrentDistributorKey: () ->
      Lockr.get('currentDistributorKey')

    getDistributorsAsAdmin: () =>
      Lockr.get('distributorsAsAdmin')

    getIsAdmin: () =>
      Lockr.get('isAdmin')

    login: (credentials) ->
      deferred = $q.defer()
      authenticationPayload = {
        access_token: _.clone(credentials.access_token)
        authuser: _.clone(credentials.authuser)
        client_id: _.clone(credentials.client_id)
        code: _.clone(credentials.code),
        id_token: _.clone(credentials.id_token)
        scope: _.clone(credentials.scope)
        session_state: _.clone(credentials.session_state)
        state: _.clone(credentials.state)
        status: _.clone(credentials.status)
      }

      if credentials.email and credentials.password
        authenticationPayload = credentials

      promise = $http.post('/login', authenticationPayload)
      promise.success (data) =>
        @currentUserKey = data.user.key
        @setIdentity(@currentUserKey)
        .then ->
          deferred.resolve(data)

      deferred.promise

    setIdentity: (userKey) =>
      deferred = $q.defer()
      Lockr.set('userKey', userKey)
      identityPromise = IdentityService.getIdentity()
      identityPromise.then (data) =>
        console.log data
        @setDistributors(data['distributors'])
        @setDistributorsAsAdmin(data['distributors_as_admin'])
        @setIsAdmin(data['is_admin'])

        Lockr.set('userEmail', data['email'])
        Lockr.set('userAdmin', data["is_admin"])
        deferred.resolve()
      deferred.promise

    removeUserInfo: () ->
      Lockr.rm('userKey')
      Lockr.rm('distributors')
      Lockr.rm('distributorsAsAdmin')
      Lockr.rm('isAdmin')
      Lockr.rm('userEmail')
      Lockr.rm('currentDistributorKey')
      Lockr.rm('currentDistributorName')


