'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "AuthenticationCtrl", ($scope, $log, $state, $timeout,
                                            identity,
                                            sweet,
                                            SessionsService,
                                            ProgressBarService) ->
  @initializeSignIn = ->
    @clientId = identity.OAUTH_CLIENT_ID
    @state = identity.STATE
    @googlePlusSignInButtonClicked = false

  @initializeSignOut = ->
    $timeout @proceedToSignIn, 1500

  $scope.$on 'event:google-plus-signin-success', (event, authResult) =>
    unless @googlePlusSignInButtonClicked
      ProgressBarService.start()
    promise = SessionsService.login(authResult)
    promise.then @loginSuccess, @loginFailure

  $scope.$on 'event:google-plus-signin-failure', (event, authResult) =>
    if @googlePlusSignInButtonClicked
      ProgressBarService.complete()
      sweet.show('Oops...', 'Unable to authenticate to Google+.', 'error')

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
