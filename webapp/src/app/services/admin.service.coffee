'use strict'

angular.module('skykitProvisioning')
.factory 'AdminService', ($http, Restangular) ->
  new class AdminService

    constructor: ->

    makeDistributor: (distributor, admin_email) ->
      payload = {
        distributor: distributor,
        admin_email: admin_email
      }

      SERVICE_NAME = "distributors"
      promise = Restangular.one("api/v1/users").customPost(payload)
      promise = Restangular.oneUrl(SERVICE_NAME, '/api/v1/distributors').customPOST(payload)
      promise

    addUserToDistributor: (userEmail, distributor, distributorAdmin) ->
      payload = {
        user_email: userEmail,
        distributor: distributor,
        distributor_admin: distributorAdmin
      }

      SERVICE_NAME = "users"
      promise = Restangular.one("api/v1/users").customPost(payload)
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{key}").customPOST(payload)
      promise

    getUsersOfDistributor: (distributorKey) ->
      SERVICE_NAME = "distributors"
      promise = Restangular.oneUrl(SERVICE_NAME, "/api/v1/analytics/distributors/#{distributorKey}/users").get()
      promise

    getAllDistributors: () ->
      SERVICE_NAME = "distributors"
      promise = Restangular.oneUrl(SERVICE_NAME, "/api/v1/distributors").get()
      promise
    
      
      

