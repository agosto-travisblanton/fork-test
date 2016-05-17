'use strict'

angular.module('skykitProvisioning').factory 'SessionsService', ($http,
  $log,
  $cookies,
  IdentityService,
  Restangular,
  AdminService,
  $q) ->
  new class SessionsService

    constructor: ->
      @uriBase = 'v1/sessions'
      @currentUserKey = undefined or $cookies.get('userKey')
      @distributors = undefined
      @distributorsAsAdmin = undefined
      @isAdmin = undefined

    deSerialize: (data) ->
      if "," in data
        data.split ","

      else
        data


    setDistributors: (distributors) ->
      $cookies.put('distributors', distributors)
      @distributors = distributors

    setDistributorsAsAdmin: (distributorsAsAdmin) ->
      $cookies.put('distributorsAsAdmin', distributorsAsAdmin)
      @distributorsAsAdmin = distributorsAsAdmin

    setIsAdmin: (isAdmin) ->
      @isAdmin = isAdmin

    getDistributors: (distributors) ->
      if @distributors then @distributors else @deSerialize $cookies.get('distributors')

    getDistributorsAsAdmin: (distributorsAsAdmin) ->
      if @distributorsAsAdmin then @distributorsAsAdmin else @deSerialize $cookies.get('distributorsAsAdmin')

    getIsAdmin: (isAdmin) ->
      if @isAdmin then @isAdmin else @deSerialize $cookies.get('isAdmin')

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

    setIdentity: (userKey)->
      deferred = $q.defer()
      $cookies.put('userKey', userKey)
      identityPromise = IdentityService.getIdentity()
      identityPromise.then (data) ->
        @setDistributors(data['distributors'])
        @setDistributorsAsAdmin(data['distributors_as_admin'])
        @setIsAdmin(data['is_admin'])

        $cookies.put('userEmail', data['email'])
        $cookies.put('userAdmin', data["is_admin"])
        deferred.resolve()
      deferred.promise

    removeUserInfo: ()->
      $cookies.remove('userKey')
      $cookies.remove('userEmail')
      $cookies.remove('userAdmin')
      $cookies.remove('currentDistributorKey')
      $cookies.remove('currentDistributorName')

