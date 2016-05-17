'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (AdminService, SessionsService, ToastsService) ->

  @isAdmin = SessionsService.getIsAdmin()
  @distributors = SessionsService.getDistributors()
  @distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()

  @makeUser = (user_email) ->

    res = AdminService.makeUser "asdf@gmail.com"

    res.then (data) ->
      console.log("asdf")

  @makeDistributor = (distributorName, adminEmail) ->
    res = AdminService.makeDistributor distributorName, adminEmail
    res.then (data) ->
      ToastsService.showSuccessToast data.data.message

    res.catch (data) ->
      ToastsService.showErrorToast data.data.message


  @
