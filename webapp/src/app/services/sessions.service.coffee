'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'SessionsService', ($http, $log, $cookies, Restangular) ->
  new class SessionsService

    constructor: ->
      @uriBase = 'v1/sessions'
      @currentUserKey = undefined

    login: (credentials) ->
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
      promise

    setUserKey: (loginResponse)->
      $cookies.put('user_key', loginResponse.data.user.key)

    removeUserKey: ()->
      $cookies.remove('user_key')

