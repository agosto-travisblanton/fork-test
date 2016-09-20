export function appRun(Restangular, $location, $injector, $rootScope, $timeout) {
  "ngInject";

  let stateChangeWatch = function () {
    let state = $injector.get('$state');
    return $rootScope.$on('$stateChangeError', function (event, toState, toParams, fromState, fromParams, error) {
      if (error[0] === "authError") {
        return state.go(error[1]);
      }
    });
  };

  $timeout(stateChangeWatch, 500);

  let requestInterceptor = function () {
    Restangular.addRequestInterceptor(function (elem, operation, what, url) {
      let StorageService = $injector.get('StorageService')

      let authToken = '6C346588BD4C6D722A1165B43C51C';
      if ($location.host().indexOf('provisioning-gamestop') > -1) {
        authToken = '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g';
      }
      Restangular.setDefaultHeaders({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': authToken,
        'X-Provisioning-User': StorageService.get('userKey'),
        'X-Provisioning-Distributor': StorageService.get('currentDistributorKey')
      });

      if (operation === 'remove') {
        return undefined;
      }

      return elem;
    })
  }

  $timeout(requestInterceptor, 500);

}


