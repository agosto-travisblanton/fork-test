import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject


describe('DomainsService', function () {
  let DomainsService = undefined;
  let Restangular = undefined;
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_DomainsService_, _Restangular_) {
    DomainsService = _DomainsService_;
    Restangular = _Restangular_;
    return promise = new skykitProvisioning.q.Mock();
  }));

  describe('.save', function () {
    it('update an existing domain, returning a promise', function () {
      let domain = {
        key: 'kdfalkdsjfakjdf98ad87fa87df0',
        put() {
        }
      };
      spyOn(domain, 'put').and.returnValue(promise);
      let actual = DomainsService.save(domain);
      expect(domain.put).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    });

    return it('insert a new domain, returning a promise', function () {
      let domain = {name: 'bob.agosto.com'};
      let domainRestangularService = {
        post(domain) {
        }
      };
      spyOn(Restangular, 'service').and.returnValue(domainRestangularService);
      spyOn(domainRestangularService, 'post').and.returnValue(promise);
      let actual = DomainsService.save(domain);
      expect(Restangular.service).toHaveBeenCalledWith('domains');
      expect(domainRestangularService.post).toHaveBeenCalledWith(domain);
      return expect(actual).toBe(promise);
    });
  });

  describe('.fetchAllDomains', () =>
    it('retrieve all domains, returning a promise', function () {
      let domainRestangularService = {
        getList() {
        }
      };
      spyOn(Restangular, 'all').and.returnValue(domainRestangularService);
      spyOn(domainRestangularService, 'getList').and.returnValue(promise);
      let actual = DomainsService.fetchAllDomains();
      expect(Restangular.all).toHaveBeenCalledWith('domains');
      expect(domainRestangularService.getList).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.getDomainByKey', () =>
    it('retrieve domain by key, returning a promise', function () {
      let domainKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';
      let domainRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'one').and.returnValue(domainRestangularService);
      spyOn(domainRestangularService, 'get').and.returnValue(promise);
      let actual = DomainsService.getDomainByKey(domainKey);
      expect(Restangular.one).toHaveBeenCalledWith('domains', `/internal/v1/domains/${domainKey}`);
      expect(domainRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.getDirectoryApiConnectivityInformation', () =>
    it('retrieve connectivity information for a domain, returning a promise', function () {
      let domainKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';
      let domainRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(domainRestangularService);
      spyOn(domainRestangularService, 'get').and.returnValue(promise);
      let actual = DomainsService.getDirectoryApiConnectivityInformation(domainKey);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('domains', `/internal/v1/domains/${domainKey}/directory_api`);
      expect(domainRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  return describe('.delete', () =>
    it('delete domain, returning a promise', function () {
      let domain = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'dev.agosto.com'};
      let domainRestangularService = {
        remove() {
        }
      };
      spyOn(Restangular, 'one').and.returnValue(domainRestangularService);
      spyOn(domainRestangularService, 'remove').and.returnValue(promise);
      let actual = DomainsService.delete(domain);
      expect(Restangular.one).toHaveBeenCalledWith('domains', domain.key);
      expect(domainRestangularService.remove).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );
});
