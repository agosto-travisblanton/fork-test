let appModule = angular.module('skykitProvisioning');

appModule.factory('DomainsService', Restangular =>
  new class DomainsService {
    
    constructor() {}

    save(domain) {
      if (domain.key !== undefined) {
        var promise = domain.put();
      } else {
        var promise = Restangular.service('domains').post(domain);
      }
      return promise;
    }

    fetchAllDomains() {
      let promise = Restangular.all('domains').getList();
      return promise;
    }

    getDomainByKey(domainKey) {
      let promise = Restangular.oneUrl('domains', `api/v1/domains/${domainKey}`).get();
      return promise;
    }

    delete(domain) {
      if (domain.key !== undefined) {
        let promise = Restangular.one("domains", domain.key).remove();
        return promise;
      }
    }
  }()
);
