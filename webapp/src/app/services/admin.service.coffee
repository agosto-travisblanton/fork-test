'use strict'

angular.module('skykitProvisioning')
.factory 'AdminService', ($http) ->
  new class AdminService

    constructor: ->


    makeUser: (user_email) ->
      url = "/api/v1/make_user"
      res = $http.post(url, {
        user_email: user_email
      })

    makeDistributor: (distributor, admin_email) ->
      url = '/api/v1/identity/make_distributor'
      res = $http.post(url, {
        distributor: distributor,
        admin_email: admin_email
      })

    addUserToDistributor: (userEmail, distributor, distributorAdmin) ->
      url = '/api/v1/identity/add_user_to_distributor'
      res = $http.post(url, {
        user_email: userEmail,
        distributor: distributor,
        distributor_admin: distributorAdmin
      })
    
      
      

