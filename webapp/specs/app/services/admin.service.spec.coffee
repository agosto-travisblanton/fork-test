'use strict'

describe 'AdminService', ->
  beforeEach module 'skykitProvisioning'
  Restangular = undefined
  key = undefined
  AdminService = undefined
  value = undefined
  restangularService = undefined
  
  beforeEach inject (_AdminService_, _Restangular_) ->
    Restangular = _Restangular_
    AdminService = _AdminService_
    key = "jim"
    value = "dwight"

  describe 'Restangular API', ->
    beforeEach ->
      restangularService = {
        customPOST: (payload) ->
          
        get: () ->
      }

      spyOn(Restangular, 'oneUrl').and.returnValue restangularService


    it '.makeDistributor', ->
      AdminService.makeDistributor('distributor', 'admin@gmail.com')
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'distributors', "/api/v1/distributors"

      
    it '.addUserToDistributor', ->
      AdminService.addUserToDistributor('admin@gmail.com', 'distributor', true)
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'users', '/api/v1/users'

      
    it '.getUsersOfDistributor', ->
      distributorKey = 'distributorKey'
      AdminService.getUsersOfDistributor(distributorKey)
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'distributors', "/api/v1/analytics/distributors/#{distributorKey}/users"

    it '.getUsersOfDistributor', ->
      AdminService.getAllDistributors()
      expect(Restangular.oneUrl).toHaveBeenCalledWith 'distributors', "/api/v1/distributors"
