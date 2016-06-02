'use strict'

angular.module('skykitProvisioning').factory 'SessionsService', ($http,
  $log,
  StorageService,
  IdentityService,
  Restangular,
  $q) ->
    new class SessionsService

      constructor: ->
        @uriBase = 'v1/sessions'

      setDistributors: (distributors) ->
        StorageService.set('distributors', distributors)

      setDistributorsAsAdmin: (distributorsAsAdmin)->
        StorageService.set('distributorsAsAdmin', distributorsAsAdmin)

      setIsAdmin: (isAdmin) ->
        StorageService.set('isAdmin', isAdmin)

      setUserKey: (value) ->
        StorageService.set('userKey', value)

      setUserEmail: (value) ->
        StorageService.set('userEmail', value)

      setCurrentDistributorKey: (value) ->
        StorageService.set('currentDistributorKey', value)

      setCurrentDistributorName: (value) ->
        StorageService.set('currentDistributorName', value)

      getUserKey: () ->
        StorageService.get('userKey')

      getUserEmail: () ->
        StorageService.get('userEmail')

      getDistributors: () ->
        StorageService.get('distributors')

      getCurrentDistributorName: () ->
        StorageService.get('currentDistributorName')

      getCurrentDistributorKey: () ->
        StorageService.get('currentDistributorKey')

      getDistributorsAsAdmin: () ->
        StorageService.get('distributorsAsAdmin')

      getIsAdmin: () ->
        StorageService.get('isAdmin')

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
          @setUserKey(data.user.key)
          @setIdentity()
          .then ->
            data

      setIdentity: () =>
        deferred = $q.defer()
        identityPromise = IdentityService.getIdentity()
        identityPromise.then (data) =>
          @setDistributors(data['distributors'])
          @setDistributorsAsAdmin(data['distributors_as_admin'])
          @setIsAdmin(data['is_admin'])
          @setUserEmail data['email']
          @setIsAdmin data["is_admin"]

          deferred.resolve()
        deferred.promise

      removeUserInfo: () ->
        StorageService.removeAll()
