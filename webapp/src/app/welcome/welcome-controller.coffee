'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "WelcomeCtrl", ($scope, $log, DistributorsService, identity) ->
  @distributors = []
  @currentDistributor = undefined
  @clientId = identity.WEB_APP_CLIENT_ID
  @state = identity.STATE

  $scope.$on 'event:google-plus-signin-success', (event, authResult) ->
    # Send login to server or save into cookie
    $log.info "SUCCESS: Google+ sign in."

  $scope.$on 'event:google-plus-signin-failure', (event, authResult) ->
    # Auth failure or signout detected
    $log.error "FAILURE: Google+ sign in: #{JSON.stringify authResult}"


  @initialize = ->
    distributorsPromise = DistributorsService.fetchAll()
    distributorsPromise.then (data) =>
      @distributors = data

  @selectDistributor = ->
    if @currentDistributor and @currentDistributor != null
      DistributorsService.currentDistributor = @currentDistributor

  @
