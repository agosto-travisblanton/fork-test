export default class IdentityService {

  constructor(Restangular) {
    this.Restangular = Restangular
  }

  getIdentity() {
    return this.Restangular.oneUrl('identity').get();
  }

  static identityServiceFactory( Restangular) {
    return new IdentityService(Restangular)
  }
}

IdentityService.identityServiceFactory.$inject = [
  "Restangular"
]



