'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (
  $scope,
  $log,
  $state,
  $timeout,
  SessionsService,
  ProgressBarService,
  ProofPlayService,
  DevicesService,
  TenantsService,
  AdminService) ->


  @createUser = (user_email) =>
    res = AdminService.makeUser "asdf@gmail.com"

    res.then = (data) =>
      console.log("asdf")


  @
