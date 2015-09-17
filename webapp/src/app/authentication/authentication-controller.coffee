'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "AuthenticationCtrl", ($scope, $log, $state, $timeout,
                                            identity,
                                            sweet,
                                            SessionsService,
                                            ProgressBarService) ->


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
    $timeout @proceedToSignIn, 1500

  @loginSuccess = (response) ->
    ProgressBarService.complete()
    $state.go 'distributor_selection'

  @loginFailure = (response) ->
    ProgressBarService.complete()
    sweet.show('Oops...', 'Unable to authenticate to Stormpath.', 'error')

  @proceedToSignIn = ->
    $state.go 'sign_in'

  @onClickGooglePlusSignIn = =>
    @googlePlusSignInButtonClicked = true
    ProgressBarService.start()

  @
