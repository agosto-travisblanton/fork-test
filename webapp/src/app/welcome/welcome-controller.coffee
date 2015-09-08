'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "WelcomeCtrl", ($scope, $log, DistributorsService, identity, sweet, SessionsService) ->
  @distributors = []
  @currentDistributor = undefined
  # Following variables used in the template
  @clientId = identity.OAUTH_CLIENT_ID
  @state = identity.STATE

  $scope.$on 'event:google-plus-signin-success', (event, authResult) =>
    $log.info "SUCCESS: Google+ sign in. #{JSON.stringify authResult}"
    promise = SessionsService.login(authResult)
    promise.then @loginSuccess, @loginFailure

  $scope.$on 'event:google-plus-signin-failure', (event, authResult) ->
    $log.error "FAILURE: Google+ sign in: #{JSON.stringify authResult}"
    sweet.show('Oops...', 'Unable to authenticate to Google+.', 'error')

  @initialize = ->
    distributorsPromise = DistributorsService.fetchAll()
    distributorsPromise.then (data) =>
      @distributors = data

  @selectDistributor = ->
    if @currentDistributor and @currentDistributor != null
      DistributorsService.currentDistributor = @currentDistributor

  @loginSuccess = (response) ->
    $log.info "SUCCESS: Stormpath login: #{JSON.stringify response}"

  @loginFailure = (response) ->
    $log.error "FAILURE: Stormpath login: #{JSON.stringify response}"
    sweet.show('Oops...', 'Unable to authenticate to Stormpath.', 'error')

  @
