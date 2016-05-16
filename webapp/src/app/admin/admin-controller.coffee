'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (AdminService) ->

  @createUser = (user_email) =>
    res = AdminService.makeUser "asdf@gmail.com"

    res.then = (data) =>
      console.log("asdf")


  @
