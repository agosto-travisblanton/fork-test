export default class VersionsService {
  constructor(Restangular) {
    this.Restangular = Restangular
  }

  getVersions() {
    let promise = this.Restangular.oneUrl('versions').get();
    return promise;
  }

}

VersionsService.$inject = [
  "Restangular"
]
