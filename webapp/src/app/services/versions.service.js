angular.module('skykitProvisioning').factory('VersionsService', Restangular =>
    new class VersionsService {
        constructor() {
        }

        getVersions() {
            let promise = Restangular.oneUrl('versions').get();
            return promise;
        }
    }()
);
