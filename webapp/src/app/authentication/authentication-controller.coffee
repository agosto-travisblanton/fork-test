'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AuthenticationCtrl", ($scope, $log, $state, $timeout,
  identity,
  sweet,
  SessionsService,
  ProgressBarService,
  ProofPlayService,
  DevicesService,
  TenantsService) ->
  # I don't know how to fix the errors in the style guide here
  @onGooglePlusSignInSuccess = (event, authResult) =>
    unless @googlePlusSignInButtonClicked
      ProgressBarService.start()
    promise = SessionsService.login(authResult)
    promise.then @loginSuccess, @loginFailure


  @onGooglePlusSignInFailure = (event, authResult) =>
    if @googlePlusSignInButtonClicked
      ProgressBarService.complete()
      sweet.show('Oops...', 'Unable to authenticate to Google+.', 'error')

  $scope.$on 'event:google-plus-signin-success', @onGooglePlusSignInSuccess
  $scope.$on 'event:google-plus-signin-failure', @onGooglePlusSignInFailure

  @initializeSignIn = ->
    @clientId = identity.OAUTH_CLIENT_ID
    @state = identity.STATE
    @googlePlusSignInButtonClicked = false

  @initializeSignOut = ->
    SessionsService.removeUserInfo()
    $timeout @proceedToSignedOut, 1500

  @loginSuccess = (response) ->
    ProgressBarService.complete()
    ProofPlayService.proofplayCache.removeAll()
    TenantsService.tenantCache.removeAll()
    DevicesService.deviceCache.removeAll()
    DevicesService.deviceByTenantCache.removeAll()
    $state.go 'distributor_selection'

  @loginFailure = () ->
    ProgressBarService.complete()
    sweet.show('Oops...', 'Unable to authenticate to Stormpath.', 'error')


  @proceedToSignedOut = ->
    $state.go 'signed_out'

  @proceedToSignIn = ->
    $state.go 'sign_in'

  @onClickGooglePlusSignIn = =>
    @googlePlusSignInButtonClicked = true
    ProgressBarService.start()

  @
