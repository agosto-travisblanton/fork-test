(function () {


  let app = angular.module('skykitProvisioning');

  app.controller("AuthenticationCtrl", function ($scope, $log, $state, $timeout,
                                                 identity,
                                                 sweet,
                                                 SessionsService,
                                                 ProgressBarService,
                                                 ProofPlayService,
                                                 DevicesService,
                                                 TenantsService) {
    let vm = this;

    vm.onGooglePlusSignInSuccess = function (event, authResult) {
      if (!vm.googlePlusSignInButtonClicked) {
        ProgressBarService.start();
      }
      let promise = SessionsService.login(authResult);
      return promise.then(vm.loginSuccess, vm.loginFailure);
    };


    vm.onGooglePlusSignInFailure = function (event, authResult) {
      if (vm.googlePlusSignInButtonClicked) {
        ProgressBarService.complete();
        return sweet.show('Oops...', 'Unable to authenticate to Google+.', 'error');
      }
    };

    $scope.$on('event:google-plus-signin-success', vm.onGooglePlusSignInSuccess);
    $scope.$on('event:google-plus-signin-failure', vm.onGooglePlusSignInFailure);

    vm.initializeSignIn = function () {
      vm.clientId = identity.OAUTH_CLIENT_ID;
      vm.state = identity.STATE;
      return vm.googlePlusSignInButtonClicked = false;
    };

    vm.initializeSignOut = function () {
      SessionsService.removeUserInfo();
      return $timeout(vm.proceedToSignedOut, 50);
    };

    vm.loginSuccess = function (response) {
      ProgressBarService.complete();
      ProofPlayService.proofplayCache.removeAll();
      TenantsService.tenantCache.removeAll();
      DevicesService.deviceCache.removeAll();
      DevicesService.deviceByTenantCache.removeAll();
      return $state.go('distributor_selection');
    };

    vm.loginFailure = function () {
      ProgressBarService.complete();
      return sweet.show('Oops...', 'Unable to authenticate to Stormpath.', 'error');
    };


    vm.proceedToSignedOut = () => $state.go('signed_out');

    vm.proceedToSignIn = () => $state.go('sign_in');

    vm.onClickGooglePlusSignIn = function () {
      vm.googlePlusSignInButtonClicked = true;
      return ProgressBarService.start();
    };

    return vm;
  });
})
();
