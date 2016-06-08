'use strict'

angular.module('skykitProvisioning')
.factory 'AuthorizationService', (SessionsService, $q) ->
  new class AuthorizationService

    constructor: ->

    authenticated: () ->
      deferred = $q.defer()
      userKey = SessionsService.getUserKey()
      if userKey
        deferred.resolve(true)
      else
        deferred.reject(["authError", 'sign_in'])
      deferred.promise

    notAuthenticated: () ->
      deferred = $q.defer()
      userKey = SessionsService.getUserKey()
      if not userKey
        deferred.resolve(true)
      else
        deferred.reject(["authError", 'home'])
      deferred.promise

    isAdminOrDistributorAdmin: () ->
      deferred = $q.defer()
      admin = SessionsService.getIsAdmin()
      distributorAdmin = SessionsService.getDistributorsAsAdmin()
      if distributorAdmin and distributorAdmin.length < 0
        hasAtLeastOneDistributorAdmin = true
      userKey = SessionsService.getUserKey()
      if not userKey
        deferred.reject('sign_in')
      if not admin and not hasAtLeastOneDistributorAdmin
        deferred.reject(["authError", 'home'])
      else
        deferred.resolve(true)
      deferred.promise


