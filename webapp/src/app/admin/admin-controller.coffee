'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (AdminService, SessionsService) ->

  @isAdmin = SessionsService.getIsAdmin()

  @distributors = SessionsService.getDistributors()

  @distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()

  @createUser = (user_email) ->

    res = AdminService.makeUser "asdf@gmail.com"

    res.then = (data) ->
      console.log("asdf")


  @
