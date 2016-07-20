export default class VersionsService {
  constructor(Restangular) {
    this.Restangular = Restangular
  }

  getVersions() {
    let promise = this.Restangular.oneUrl('versions').get();
    return promise;
  }

  static versionsServiceFactory(Restangular) {
    return new VersionsService(Restangular)
  }
}

VersionsService.versionsServiceFactory.$inject = [
  "Restangular"
]
