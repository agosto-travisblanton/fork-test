export default class AuthorizationService {

  constructor(SessionsService, $q, $window) {
    'ngInject';
    this.$q = $q
    this.$window = $window
    this.SessionsService = SessionsService
  }

  authenticated() {
    let deferred = this.$q.defer();
    let userKey = this.SessionsService.getUserKey();
    let userJWT = this.SessionsService.getJWT();
    if (userKey) {
      if (userKey && userJWT) {
        deferred.resolve(true);
      } else {
        this.SessionsService.removeUserInfo();
        this.$window.location.href = "#/redirect"
      }
    } else {
      deferred.reject(["authError", 'sign_in']);
    }
    return deferred.promise;
  }

  notAuthenticated() {
    let deferred = this.$q.defer();
    let userKey = this.SessionsService.getUserKey();
    if (!userKey) {
      deferred.resolve(true);
    } else {
      deferred.reject(["authError", 'home']);
    }
    return deferred.promise;
  }

  isAdminOrDistributorAdmin() {
    let deferred = this.$q.defer();
    let admin = this.SessionsService.getIsAdmin();
    let distributorAdmin = this.SessionsService.getDistributorsAsAdmin();
    let hasAtLeastOneDistributorAdmin = false;
    if (distributorAdmin && distributorAdmin.length > 0) {
      hasAtLeastOneDistributorAdmin = true;
    }
    let userKey = this.SessionsService.getUserKey();
    let userJWT = this.SessionsService.getJWT();
    if (userKey) {
      if (!userJWT) {
        this.SessionsService.removeUserInfo();
        this.$window.location.href = "#/redirect"
      }
    }

    if (!userKey) {
      deferred.reject('sign_in');
    } else if (!admin && !hasAtLeastOneDistributorAdmin) {
      deferred.reject(["authError", 'home']);
    } else {
      deferred.resolve(true);
    }
    return deferred.promise;
  }
}

