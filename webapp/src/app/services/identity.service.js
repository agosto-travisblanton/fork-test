angular.module('skykitProvisioning').factory('IdentityService', ($log, Restangular) =>
  new class IdentityService {

    constructor() {
    }

    getIdentity() {
      return Restangular.oneUrl('identity').get();
    }
  }()
);

