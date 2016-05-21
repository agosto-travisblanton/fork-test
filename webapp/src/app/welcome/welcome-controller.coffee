'use strict'
appModule = angular.module 'skykitProvisioning'
appModule.controller "WelcomeCtrl", (VersionsService, $state, StorageService, DistributorsService, SessionsService) ->
  @version_data = []
  @loading = true

  @proceedToSignIn = ->
    $state.go 'sign_in'

  @capitalizeFirstLetter = (string) ->
    string.charAt(0).toUpperCase() + string.slice(1)

  @giveOptionToChangeDistributor = () =>
    distributorsPromise = DistributorsService.fetchAllByUser(StorageService.get('userKey'))
    distributorsPromise.then (data) =>
      @has_multiple_distributors = data.length > 1
      @loading = false

  @changeDistributor = () ->
    $state.go 'distributor_selection'

  @setIdentity = () =>
    @identity.first_name = @capitalizeFirstLetter(@identity.email.split("@")[0].split(".")[0])
    @identity.last_name = @capitalizeFirstLetter(@identity.email.split("@")[0].split(".")[1])
    @identity.full_name = @identity.first_name + " " + @identity.last_name

  @getVersion = () =>
    promise = VersionsService.getVersions()
    promise.then (data) =>
      @version_data = data

  @initialize = ->
    @identity = {
      key: StorageService.get('userKey')
      email: StorageService.get('userEmail')
      distributorKey: StorageService.get('currentDistributorKey')
      distributorName: StorageService.get('currentDistributorName')
    }

    @giveOptionToChangeDistributor()

    if !@identity.email
      $state.go "sign_in"

    else
      @setIdentity()
      @getVersion()
  @
