(function () {

    let app = angular.module('skykitProvisioning');

    app.run(function (StorageService, Restangular, $location, $injector, $rootScope, $timeout) {
        app.constant("moment", moment);

        let stateChangeWatch = function () {
            let state = $injector.get('$state');
            return $rootScope.$on('$stateChangeError', function (event, toState, toParams, fromState, fromParams, error) {
                if (error[0] === "authError") {
                    return state.go(error[1]);
                }
            });
        };

        $timeout(stateChangeWatch, 500);

        return Restangular.addRequestInterceptor(function (elem, operation, what, url) {
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
        });
    });


    app.factory('RequestInterceptor', function (StorageService, $location) {
        let interceptor = {
            request(config) {
                let gs = '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g';
                let prod = '6C346588BD4C6D722A1165B43C51C';
                config.headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': $location.host().indexOf('provisioning-gamestop') > -1 ? gs : prod,
                    'X-Provisioning-User': StorageService.get('userKey'),
                    'X-Provisioning-User-Identifier': StorageService.get('userEmail'),
                    'X-Provisioning-Distributor': StorageService.get('currentDistributorKey')
                };
                return config;
            }
        };
        return interceptor;
    });


    app.config($httpProvider => $httpProvider.interceptors.push('RequestInterceptor'));
})
();