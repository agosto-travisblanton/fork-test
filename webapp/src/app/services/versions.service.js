export default class VersionsService {

  constructor(Restangular) {
    'ngInject';
    this.Restangular = Restangular
  }

  getVersions() {
    let promise = this.Restangular.oneUrl('versions').get();
    return promise;
  }
}
