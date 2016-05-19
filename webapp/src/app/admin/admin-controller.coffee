'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (AdminService, SessionsService, ToastsService) ->
  @isAdmin = SessionsService.getIsAdmin()
  @distributors = SessionsService.getDistributors()
  @distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()
  @currentDistributorName = SessionsService.getCurrentDistributerName()
  console.log @currentDistributorName

  @addUserToDistributor = (userEmail, distributor, distributorAdmin) ->
    res = AdminService.addUserToDistributor(userEmail, distributor, distributorAdmin)

    res.then (data) ->
      console.log("asdf")

  @makeDistributor = (distributorName, adminEmail) ->
    res = AdminService.makeDistributor distributorName, adminEmail
    res.then (data) ->
      ToastsService.showSuccessToast data.data.message

    res.catch (data) ->
      ToastsService.showErrorToast data.data.message


  @getUsersOfDistributer = () ->
    @loadingUsersOfDistributer = true
    u = AdminService.getUsersOfDistributor(SessionsService.getCurrentDistributerKey())
    u.then (data) =>
      @loadingUsersOfDistributer = false
      @usersOfDistributer = data.data

  @getUsersOfDistributer()


  @
