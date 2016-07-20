export default class SessionsService {

  constructor($http, $log, StorageService, IdentityService, Restangular, $q) {
    this.$http = $http
    this.$log = $log
    this.StorageService = StorageService
    this.IdentityService = IdentityService
    this.Restangular = Restangular
    this.$q = $q
    this.setIdentity = this.setIdentity.bind(this);
    this.uriBase = 'v1/sessions';
  }

  setDistributors(distributors) {
    return this.StorageService.set('distributors', distributors);
  }

  setDistributorsAsAdmin(distributorsAsAdmin) {
    return this.StorageService.set('distributorsAsAdmin', distributorsAsAdmin);
  }

  setIsAdmin(isAdmin) {
    return this.StorageService.set('isAdmin', isAdmin);
  }

  setUserKey(value) {
    return this.StorageService.set('userKey', value);
  }

  setUserEmail(value) {
    return this.StorageService.set('userEmail', value);
  }

  setCurrentDistributorKey(value) {
    return this.StorageService.set('currentDistributorKey', value);
  }

  setCurrentDistributorName(value) {
    return this.StorageService.set('currentDistributorName', value);
  }

  getUserKey() {
    return this.StorageService.get('userKey');
  }

  getUserEmail() {
    return this.StorageService.get('userEmail');
  }

  getDistributors() {
    return this.StorageService.get('distributors');
  }

  getCurrentDistributorName() {
    return this.StorageService.get('currentDistributorName');
  }

  getCurrentDistributorKey() {
    return this.StorageService.get('currentDistributorKey');
  }

  getDistributorsAsAdmin() {
    return this.StorageService.get('distributorsAsAdmin');
  }

  getIsAdmin() {
    return this.StorageService.get('isAdmin');
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

    let promise = this.$http.post('/login', authenticationPayload);
    return promise.success(data => {
      this.setUserKey(data.user.key);
      return this.setIdentity()
        .then(() => data);
    });
  }

  setIdentity() {
    let deferred = this.$q.defer();
    let identityPromise = this.IdentityService.getIdentity();
    identityPromise.then(data => {
      this.setDistributors(data['distributors']);
      this.setDistributorsAsAdmin(data['distributors_as_admin']);
      this.setCurrentDistributorKey("null")
      this.setIsAdmin(data['is_admin']);
      this.setUserEmail(data['email']);
      this.setIsAdmin(data["is_admin"]);

      return deferred.resolve();
    });
    return deferred.promise;
  }

  removeUserInfo() {
    return this.StorageService.removeAll();
  }

  static create($http, $log, StorageService, IdentityService, Restangular, $q) {
    return new SessionsService($http, $log, StorageService, IdentityService, Restangular, $q)
  }
}

