import jwt_decode from 'jwt-decode'

export default class SessionsService {

  constructor($http, $log, StorageService, IdentityService, Restangular, $q, sweet) {
    'ngInject';
    this.$http = $http
    this.$log = $log
    this.StorageService = StorageService
    this.IdentityService = IdentityService
    this.Restangular = Restangular
    this.$q = $q
    this.uriBase = 'v1/sessions';
  }

  setJWT(JWT){
    return this.StorageService.set("JWT", JWT)
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

  getJWT() {
    return this.StorageService.get("JWT")
  }

  login(credentials) {
    // request interceptor checks this
    this.StorageService.set('oAuth', credentials.id_token)

    let promise = this.$http({url: '/internal/v1/login', method: 'GET'})
    return promise.then((res) => {
      let data = jwt_decode(res.data.token);
      this.setJWT(res.data.token)
      this.setDistributors(data['distributors']);
      this.setDistributorsAsAdmin(data['distributors_as_admin']);
      this.setIsAdmin(data['is_admin']);
      this.setUserEmail(data['email']);
      this.setUserKey(data['key']);
    })
    return promise.catch((res) => {
      sweet.show('Oops...', "We couldn't log you in :(. Please try again or contact support", 'error');
    })
  }

  removeUserInfo() {
    this.StorageService.removeAll();
  }
}

