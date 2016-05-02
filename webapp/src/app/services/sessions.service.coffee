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
      @currentUserKey = undefined or $cookies.get('userKey')

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
        a = @setIdentity(@currentUserKey)
        .then ->
          deferred.resolve(data)

      deferred.promise

    setIdentity: (userKey)->
      deferred = $q.defer()
      $cookies.put('userKey', userKey)
      identityPromise = IdentityService.getIdentity()
      identityPromise.then (data) ->
        $cookies.put('userEmail', data['email'])
        deferred.resolve()
      deferred.promise

    removeUserInfo: ()->
      $cookies.remove('userKey')
      $cookies.remove('userEmail')
      $cookies.remove('currentDistributorKey')
      $cookies.remove('currentDistributorName')

