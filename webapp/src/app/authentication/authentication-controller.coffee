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
    vm = @

    vm.onGooglePlusSignInSuccess = (event, authResult) ->
      unless vm.googlePlusSignInButtonClicked
        ProgressBarService.start()
      promise = SessionsService.login(authResult)
      promise.then vm.loginSuccess, vm.loginFailure


    vm.onGooglePlusSignInFailure = (event, authResult) ->
      if vm.googlePlusSignInButtonClicked
        ProgressBarService.complete()
        sweet.show('Oops...', 'Unable to authenticate to Google+.', 'error')

    $scope.$on 'event:google-plus-signin-success', vm.onGooglePlusSignInSuccess
    $scope.$on 'event:google-plus-signin-failure', vm.onGooglePlusSignInFailure

    vm.initializeSignIn = ->
      vm.clientId = identity.OAUTH_CLIENT_ID
      vm.state = identity.STATE
      vm.googlePlusSignInButtonClicked = false

    vm.initializeSignOut = ->
      SessionsService.removeUserInfo()
      $timeout vm.proceedToSignedOut, 1500

    vm.loginSuccess = (response) ->
      ProgressBarService.complete()
      ProofPlayService.proofplayCache.removeAll()
      TenantsService.tenantCache.removeAll()
      DevicesService.deviceCache.removeAll()
      DevicesService.deviceByTenantCache.removeAll()
      $state.go 'distributor_selection'

    vm.loginFailure = () ->
      ProgressBarService.complete()
      sweet.show('Oops...', 'Unable to authenticate to Stormpath.', 'error')


    vm.proceedToSignedOut = ->
      $state.go 'signed_out'

    vm.proceedToSignIn = ->
      $state.go 'sign_in'

    vm.onClickGooglePlusSignIn = ->
      vm.googlePlusSignInButtonClicked = true
      ProgressBarService.start()

    vm
