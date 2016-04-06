'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "WelcomeCtrl", (VersionsService, $state, $cookies) ->
  vm = @
  vm.version_data = []

  @proceedToSignIn = ->
    $state.go 'sign_in'


  vm.initialize = ->
    vm.identity = {
      key: $cookies.get('userKey')
      email: $cookies.get('userEmail')
      distributorKey: $cookies.get('currentDistributorKey')
      distributorName: $cookies.get('currentDistributorName')
    }

    if !vm.identity.email
      $state.go "sign_in"
    
    else
      promise = VersionsService.getVersions()
      promise.then (data) ->
        vm.version_data = data

  vm
