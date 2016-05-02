'use strict'
appModule = angular.module 'skykitProvisioning'
appModule.controller "WelcomeCtrl", (VersionsService, $state, $cookies, DistributorsService, SessionsService) ->
  vm = @
  vm.version_data = []
  vm.loading = true

  @proceedToSignIn = ->
    $state.go 'sign_in'

  @capitalizeFirstLetter = (string) ->
    string.charAt(0).toUpperCase() + string.slice(1)

  vm.giveOptionToChangeDistributor = () =>
    distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.currentUserKey)
    distributorsPromise.then (data) =>
      vm.has_multiple_distributors = data.length > 1
      vm.loading = false



  @changeDistributor = () ->
    $state.go 'distributor_selection'

  vm.initialize = ->
    vm.identity = {
      key: $cookies.get('userKey')
      email: $cookies.get('userEmail')
      distributorKey: $cookies.get('currentDistributorKey')
      distributorName: $cookies.get('currentDistributorName')
    }

    vm.giveOptionToChangeDistributor()

    if !vm.identity.email
      $state.go "sign_in"

    else
      vm.identity.first_name = @capitalizeFirstLetter(vm.identity.email.split("@")[0].split(".")[0])
      vm.identity.last_name = @capitalizeFirstLetter(vm.identity.email.split("@")[0].split(".")[1])
      vm.identity.full_name = vm.identity.first_name + " " + vm.identity.last_name
      promise = VersionsService.getVersions()
      promise.then (data) ->
        vm.version_data = data

  vm
