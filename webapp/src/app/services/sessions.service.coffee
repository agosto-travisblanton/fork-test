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
      @distributors = undefined
      @distributorsAsAdmin = undefined
      @isAdmin = undefined


    typeIsArray = ( value ) ->
      value and
          typeof value is 'object' and
          value instanceof Array and
          typeof value.length is 'number' and
          typeof value.splice is 'function' and
          not ( value.propertyIsEnumerable 'length' )

    setDistributors: (distributors) =>
      $cookies.put('distributors', JSON.stringify distributors)
      @distributors = distributors

    setDistributorsAsAdmin: (distributorsAsAdmin) =>
      $cookies.put('distributorsAsAdmin', JSON.stringify distributorsAsAdmin)
      @distributorsAsAdmin = distributorsAsAdmin

    setIsAdmin: (isAdmin) =>
      $cookies.put('distributorsAsAdmin', isAdmin)
      @isAdmin = isAdmin

    getDistributors: (distributors) =>
      if @distributors
        @distributors

      else
        d = $cookies.get('distributors')
        if d
          JSON.parse d

        else false
          
    getCurrentDistributerName: () ->
      $cookies.get('currentDistributorName')
      
    getCurrentDistributerKey: () ->
      $cookies.get('currentDistributorKey')

    getDistributorsAsAdmin: () =>
      if @distributorsAsAdmin
        @distributorsAsAdmin
      else
        d = $cookies.get('distributorsAsAdmin')
        if d
          JSON.parse d
        else false

    getIsAdmin: () =>
      if @isAdmin
        @isAdmin
      else
        d = $cookies.get('isAdmin')
        if d
          true
        else
          false

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
      $cookies.put('userKey', userKey)
      identityPromise = IdentityService.getIdentity()
      identityPromise.then (data) =>
        @setDistributors(data['distributors'])
        @setDistributorsAsAdmin(data['distributors_as_admin'])
        @setIsAdmin(data['is_admin'])

        $cookies.put('userEmail', data['email'])
        $cookies.put('userAdmin', data["is_admin"])
        deferred.resolve()
      deferred.promise

    removeUserInfo: () ->
      $cookies.remove('userKey')
      $cookies.remove('distributors')
      $cookies.remove('distributorsAsAdmin')
      $cookies.remove('isAdmin')
      $cookies.remove('userEmail')
      $cookies.remove('userAdmin')
      $cookies.remove('currentDistributorKey')
      $cookies.remove('currentDistributorName')


