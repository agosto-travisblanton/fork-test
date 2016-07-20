export default class IdentityService {
/*@ngInject*/
  constructor(Restangular) {
    this.Restangular = Restangular
  }

  getIdentity() {
    return this.Restangular.oneUrl('identity').get();
  }

  static create( Restangular) {
    return new IdentityService(Restangular)
  }
}


