'use strict'

angular.module('skykitProvisioning')
.factory 'AdminService', ($http, $cookies) ->
  new class AdminService

    constructor: ->


    makeUser: (user_email) ->
      url = "/api/v1/make_user"
      res = $http.post(url, {
        user_email: user_email
      })
      
    
      
      

