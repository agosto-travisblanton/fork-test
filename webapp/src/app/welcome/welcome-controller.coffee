'use strict'
appModule = angular.module 'skykitProvisioning'
appModule.controller "WelcomeCtrl", (VersionsService, $state, DistributorsService, SessionsService) ->
  vm = @
  vm.version_data = []
  vm.loading = true

  vm.proceedToSignIn = ->
    $state.go 'sign_in'

  vm.capitalizeFirstLetter = (string) ->
    string.charAt(0).toUpperCase() + string.slice(1)

  vm.giveOptionToChangeDistributor = () ->
    distributorsPromise = DistributorsService.fetchAllByUser(SessionsService.getUserKey())
    distributorsPromise.then (data) ->
      vm.has_multiple_distributors = data.length > 1
      vm.loading = false

  vm.changeDistributor = () ->
    $state.go 'distributor_selection'

  vm.getVersion = () ->
    promise = VersionsService.getVersions()
    promise.then (data) ->
      vm.version_data = data

  vm.initialize = ->
    vm.identity = {
      key: SessionsService.getUserKey()
      email: SessionsService.getUserEmail()
      distributorKey: SessionsService.getCurrentDistributorKey()
      distributorName: SessionsService.getCurrentDistributorName()
    }

    vm.giveOptionToChangeDistributor()

    if !vm.identity.email
      $state.go "sign_in"

    else
      vm.getVersion()
  vm
