'use strict'

angular.module('skykitProvisioning')
.factory 'AdminService', (Restangular) ->
  new class AdminService

    constructor: ->
      @USER_SERVICE = "users"
      @DISTRIBUTOR_SERVICE = "distributors"

    makeDistributor: (distributor, admin_email) ->
      payload = {
        distributor: distributor,
        admin_email: admin_email
      }

      promise = Restangular.oneUrl(@DISTRIBUTOR_SERVICE, '/api/v1/distributors').customPOST(payload)
      promise

    addUserToDistributor: (userEmail, distributor, distributorAdmin) ->
      payload = {
        user_email: userEmail,
        distributor: distributor,
        distributor_admin: distributorAdmin
      }

      promise = Restangular.oneUrl(@USER_SERVICE, "/api/v1/users").customPOST(payload)
      promise

    getUsersOfDistributor: (distributorKey) ->
      promise = Restangular.oneUrl(@DISTRIBUTOR_SERVICE, "/api/v1/analytics/distributors/#{distributorKey}/users").get()
      promise

    getAllDistributors: () ->
      promise = Restangular.oneUrl(@DISTRIBUTOR_SERVICE, "/api/v1/distributors").get()
      promise
    
      
      

