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
      params =  {
        user_email: userEmail,
        distributor: distributor,
        distributor_admin: distributorAdmin
      }
      res = $http.post(url, params)

    getUsersOfDistributor: (distributorKey) ->
      url = 'api/v1/distributors/analytics/users/' + distributorKey
      res = $http.get(url)

    getAllDistributors: () ->
      url = '/api/v1/distributors/analytics/all'
      res = $http.get(url)
    
      
      

