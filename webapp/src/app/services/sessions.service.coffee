'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'SessionsService', ($http, $log, Restangular) ->
  new class SessionsService
    SERVICE_NAME = 'sessions'
    @uriBase = 'v1/sessions'

    getIdentity: ->
      Restangular.oneUrl('api/v1/devices').get()

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
      $log.info "Authentication payload: #{JSON.stringify authenticationPayload}"
      promise = $http.post '/login', authenticationPayload
      promise


