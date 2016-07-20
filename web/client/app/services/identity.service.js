export default class IdentityService {

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

IdentityService.create.$inject = [
  "Restangular"
]



