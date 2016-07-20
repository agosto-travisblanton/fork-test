export default  class DomainsService {

  constructor(Restangular) {
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

  getDomainByKey(domainKey) {
    let promise = this.Restangular.oneUrl('domains', `api/v1/domains/${domainKey}`).get();
    return promise;
  }

  delete(domain) {
    if (domain.key !== undefined) {
      let promise = this.Restangular.one("domains", domain.key).remove();
      return promise;
    }
  }

  static domainServiceFactory(Restangular) {
    return new DomainsService(Restangular)
  }
}

DomainsService.domainServiceFactory.$inject = ["Restangular"]


