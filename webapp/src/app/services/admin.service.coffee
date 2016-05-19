'use strict'

angular.module('skykitProvisioning')
.factory 'AdminService', ($http) ->
  new class AdminService

    constructor: ->

    makeDistributor: (distributor, admin_email) ->
      url = '/api/v1/distributors'
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

    getUsersOfDistributor: (distributerKey) ->
      url = 'api/v1/distributors/analytics/users/' + distributerKey
      res = $http.get(url)

    getAllDistributers: () ->
      url = '/api/v1/distributors/analytics/all'
      res = $http.get(url)
    
      
      

