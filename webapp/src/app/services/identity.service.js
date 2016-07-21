export default class IdentityService {

  constructor(Restangular) {
    'ngInject';
    this.Restangular = Restangular;
  }

  getIdentity() {
    return this.Restangular.oneUrl('identity').get();
  }
}
