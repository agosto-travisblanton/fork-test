angular.module('skykitProvisioning').factory('SessionsService', ($http,
                                                                 $log,
                                                                 StorageService,
                                                                 IdentityService,
                                                                 Restangular,
                                                                 $q) =>
  new class SessionsService {

    constructor() {
      this.setIdentity = this.setIdentity.bind(this);
      this.uriBase = 'v1/sessions';
    }

    setDistributors(distributors) {
      return StorageService.set('distributors', distributors);
    }

    setDistributorsAsAdmin(distributorsAsAdmin) {
      return StorageService.set('distributorsAsAdmin', distributorsAsAdmin);
    }

    setIsAdmin(isAdmin) {
      return StorageService.set('isAdmin', isAdmin);
    }

    setUserKey(value) {
      return StorageService.set('userKey', value);
    }

    setUserEmail(value) {
      return StorageService.set('userEmail', value);
    }

    setCurrentDistributorKey(value) {
      return StorageService.set('currentDistributorKey', value);
    }

    setCurrentDistributorName(value) {
      return StorageService.set('currentDistributorName', value);
    }

    getUserKey() {
      return StorageService.get('userKey');
    }

    getUserEmail() {
      return StorageService.get('userEmail');
    }

    getDistributors() {
      return StorageService.get('distributors');
    }

    getCurrentDistributorName() {
      return StorageService.get('currentDistributorName');
    }

    getCurrentDistributorKey() {
      return StorageService.get('currentDistributorKey');
    }

    getDistributorsAsAdmin() {
      return StorageService.get('distributorsAsAdmin');
    }

    getIsAdmin() {
      return StorageService.get('isAdmin');
    }

    login(credentials) {
      let authenticationPayload = {
        access_token: _.clone(credentials.access_token),
        authuser: _.clone(credentials.authuser),
        client_id: _.clone(credentials.client_id),
        code: _.clone(credentials.code),
        id_token: _.clone(credentials.id_token),
        scope: _.clone(credentials.scope),
        session_state: _.clone(credentials.session_state),
        state: _.clone(credentials.state),
        status: _.clone(credentials.status)
      };

      if (credentials.email && credentials.password) {
        authenticationPayload = credentials;
      }

      let promise = $http.post('/login', authenticationPayload);
      return promise.success(data => {
        this.setUserKey(data.user.key);
        return this.setIdentity()
          .then(() => data);
      });
    }

    setIdentity() {
      let deferred = $q.defer();
      let identityPromise = IdentityService.getIdentity();
      identityPromise.then(data => {
        this.setDistributors(data['distributors']);
        this.setDistributorsAsAdmin(data['distributors_as_admin']);
        this.setIsAdmin(data['is_admin']);
        this.setUserEmail(data['email']);
        this.setIsAdmin(data["is_admin"]);

        return deferred.resolve();
      });
      return deferred.promise;
    }

    removeUserInfo() {
      return StorageService.removeAll();
    }
  }()
);
