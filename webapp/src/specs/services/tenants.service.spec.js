import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('TenantsService', function () {
  let TenantsService = undefined;
  let Restangular = undefined;
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_TenantsService_, _Restangular_) {
    TenantsService = _TenantsService_;
    Restangular = _Restangular_;
    return promise = new skykitProvisioning.q.Mock();
  }));

  describe('.save', function () {
    it('update an existing tenant, returning a promise', function () {
      let tenant = {
        key: 'kdfalkdsjfakjdf98ad87fa87df0',
        put() {
        }
      };
      spyOn(tenant, 'put').and.returnValue(promise);
      let actual = TenantsService.save(tenant);
      expect(tenant.put).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    });

    return it('insert a new tenant, returning a promise', function () {
      let tenant = {name: 'Foobar'};
      let tenantRestangularService = {
        post(tenant) {
        }
      };
      spyOn(Restangular, 'service').and.returnValue(tenantRestangularService);
      spyOn(tenantRestangularService, 'post').and.returnValue(promise);
      let actual = TenantsService.save(tenant);
      expect(Restangular.service).toHaveBeenCalledWith('tenants');
      expect(tenantRestangularService.post).toHaveBeenCalledWith(tenant);
      return expect(actual).toBe(promise);
    });
  });

  describe('.fetchAllTenants', () =>
    it('retrieve all tenants, returning a promise', function () {
      let tenantRestangularService = {
        getList() {
        }
      };
      spyOn(Restangular, 'all').and.returnValue(tenantRestangularService);
      spyOn(tenantRestangularService, 'getList').and.returnValue(promise);
      let actual = TenantsService.fetchAllTenants();
      expect(Restangular.all).toHaveBeenCalledWith('tenants');
      expect(tenantRestangularService.getList).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );


  describe('.searchAllTenantsByName', () =>
    it('fetch all tenants by name, returning a promise', function () {
      let tenantRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(tenantRestangularService);
      spyOn(tenantRestangularService, 'get').and.returnValue(promise);
      let tenant_name = "someTenant"
      let url = `/api/v1/tenants?tenant_name=${tenant_name}`;
      let actual = TenantsService.searchAllTenantsByName(tenant_name);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('tenants', url);
      expect(tenantRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );


  describe('.getTenantByKey', () =>
    it('retrieve tenant by key, returning a promise', function () {
      let tenantKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';
      let tenantRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(tenantRestangularService);
      spyOn(tenantRestangularService, 'get').and.returnValue(promise);
      let actual = TenantsService.getTenantByKey(tenantKey);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('tenants', `api/v1/tenants/${tenantKey}`);
      expect(tenantRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  return describe('.delete', () =>
    it('delete tenant, returning a promise', function () {
      let tenant = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'Foobar'};
      let tenantRestangularService = {
        remove() {
        }
      };
      spyOn(Restangular, 'one').and.returnValue(tenantRestangularService);
      spyOn(tenantRestangularService, 'remove').and.returnValue(promise);
      let actual = TenantsService.delete(tenant);
      expect(Restangular.one).toHaveBeenCalledWith('tenants', tenant.key);
      expect(tenantRestangularService.remove).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );
});
