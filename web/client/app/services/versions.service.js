export default class VersionsService {
  /*@ngInject*/
  constructor(Restangular) {
    this.Restangular = Restangular
  }

  getVersions() {
    let promise = this.Restangular.oneUrl('versions').get();
    return promise;
  }

  static create(Restangular) {
    return new VersionsService(Restangular)
  }
}
