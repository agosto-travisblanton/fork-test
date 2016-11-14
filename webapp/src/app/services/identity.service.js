export default class IdentityService {

  constructor(Restangular) {
    'ngInject';
    this.Restangular = Restangular;
  }

  getIdentity() {
    return this.Restangular.oneUrl('is_our_token_valid').get();
  }
}
