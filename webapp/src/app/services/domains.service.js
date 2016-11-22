export default  class DomainsService {

  constructor(Restangular) {
    'ngInject';
    this.Restangular = Restangular
  }

  save(domain) {
    if (domain.key !== undefined) {
      var promise = domain.put();
    } else {
      var promise = this.Restangular.service('domains').post(domain);
    }
    return promise;
  }

  fetchAllDomains() {
    let promise = this.Restangular.all('domains').getList();
    return promise;
  }

  getDomainByKey(key) {
    let promise = this.Restangular.one('domains', key).get();
    return promise;
  }

  getDirectoryApiConnectivityInformation(key) {
    let promise = this.Restangular.oneUrl('domains', `/internal/v1/domains/${key}/directory_api`).get();
    return promise;
  }

  delete(domain) {
    if (domain.key !== undefined) {
      let promise = this.Restangular.one('domains', domain.key).remove();
      return promise;
    }
  }
}


