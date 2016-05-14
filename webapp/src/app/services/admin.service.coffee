'use strict'

angular.module('skykitProvisioning')
.factory 'AdminService', ($http, $q, $window, $cookies, $stateParams, $state, ToastsService, CacheFactory) ->
  new class AdminService

    constructor: ->
    

    makeUser: (user_email) =>
      url = "/api/v1/make_user"
      res = $http.post(url, {
        user_email: user_email
      })


#    makeHTTPRequest: (where_to_go, tenant) =>
#      deferred = $q.defer()
#      url = @makeHTTPURL where_to_go, tenant
#
#      if not @proofplayCache.get(url)
#        res = $http.get(url)
#
#        res.then (data) =>
#          @proofplayCache.put(url, data)
#          deferred.resolve(data)
#
#        res.catch (err) ->
#          deferred.reject(err)
#
#      else
#        deferred.resolve(@proofplayCache.get(url))
#
#      deferred.promise
