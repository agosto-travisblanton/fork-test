'use strict'

angular.module('skykitProvisioning')
.factory 'AdminService', ($http) ->
  new class AdminService

    constructor: ->
    
    makeUser: (user_email) =>
      url = "/api/v1/make_user"
      res = $http.post(url, {
        user_email: user_email
      })

