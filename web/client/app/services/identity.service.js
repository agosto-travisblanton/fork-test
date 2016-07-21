export default class IdentityService {

  constructor(Restangular) {
    this.Restangular = Restangular
  }

  getIdentity() {
    return this.Restangular.oneUrl('identity').get();
  }
  
}

IdentityService.$inject = [
  "Restangular"
]



