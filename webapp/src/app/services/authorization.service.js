angular.module('skykitProvisioning')
    .factory('AuthorizationService', (SessionsService, $q) =>
        new class AuthorizationService {

            constructor() {
            }

            authenticated() {
                let deferred = $q.defer();
                let userKey = SessionsService.getUserKey();
                if (userKey) {
                    deferred.resolve(true);
                } else {
                    deferred.reject(["authError", 'sign_in']);
                }
                return deferred.promise;
            }

            notAuthenticated() {
                let deferred = $q.defer();
                let userKey = SessionsService.getUserKey();
                if (!userKey) {
                    deferred.resolve(true);
                } else {
                    deferred.reject(["authError", 'home']);
                }
                return deferred.promise;
            }

            isAdminOrDistributorAdmin() {
                let deferred = $q.defer();
                let admin = SessionsService.getIsAdmin();
                let distributorAdmin = SessionsService.getDistributorsAsAdmin();
                let hasAtLeastOneDistributorAdmin = false;
                if (distributorAdmin && distributorAdmin.length > 0) {
                    hasAtLeastOneDistributorAdmin = true;
                }
                let userKey = SessionsService.getUserKey();
                if (!userKey) {
                    deferred.reject('sign_in');
                } else if (!admin && !hasAtLeastOneDistributorAdmin) {
                    deferred.reject(["authError", 'home']);
                } else {
                    deferred.resolve(true);
                }
                return deferred.promise;
            }
        }()
    );


