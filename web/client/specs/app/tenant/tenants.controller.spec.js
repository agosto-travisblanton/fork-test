import ProgressBarServiceClass from './../../../app/services/progressbar.service'
import TenantsServiceClass from './../../../app/services/tenants.service'
import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('TenantsCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let $state = undefined;
  let TenantsService = undefined;
  let promise = undefined;
  let ProgressBarService = undefined;
  let sweet = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(module(function ($provide) {
    $provide.service('TenantsService', TenantsServiceClass);
    $provide.service('ProgressBarService', ProgressBarServiceClass);
  }));


  beforeEach(inject(function (_$controller_, _TenantsService_, _$state_, _ProgressBarService_, _sweet_) {
    $controller = _$controller_;
    $state = _$state_;
    TenantsService = _TenantsService_;
    ProgressBarService = _ProgressBarService_;
    sweet = _sweet_;
    return controller = $controller('TenantsCtrl', {
      $state,
      TenantsService,
      ProgressBarService,
      sweet,
    });
  }));

  describe('initialization', () =>
    it('tenants should be an empty array', () => expect(angular.isArray(controller.tenants)).toBeTruthy())
  );

  describe('.initialize', function () {
    let tenants = {
      tenants: [
        {
          key: 'dhjad897d987fadafg708fg7d',
          name: 'Foobar1',
          created: '2015-05-10 22:15:10',
          updated: '2015-05-10 22:15:10'
        },
        {
          key: 'dhjad897d987fadafg708y67d',
          name: 'Foobar2',
          created: '2015-05-10 22:15:10',
          updated: '2015-05-10 22:15:10'
        },
        {
          key: 'dhjad897d987fadafg708hb55',
          name: 'Foobar3',
          created: '2015-05-10 22:15:10',
          updated: '2015-05-10 22:15:10'
        }
      ],
      total: 3,
      is_first_page: true,
      is_last_page: false
    };

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(TenantsService, 'fetchAllTenantsPaginated').and.returnValue(promise);
      spyOn(ProgressBarService, 'start');
      return spyOn(ProgressBarService, 'complete');
    });

    it('call TenantsService.fetchAllTenantsPaginated to retrieve all tenants', function () {
      controller.initialize();
      promise.resolve(tenants);
      return expect(TenantsService.fetchAllTenantsPaginated).toHaveBeenCalled();
    });

    return it("the 'then' handler caches the retrieved tenants in the controller", function () {
      controller.initialize();
      promise.resolve(tenants);
      return expect(controller.tenants).toBe(tenants.tenants);
    });
  });

  describe('.getFetchSuccess', function () {
    beforeEach(() => spyOn(ProgressBarService, 'complete'));

    return it('stops the progress bar', function () {
      let response = {tenants: [], total: 1, is_first_page: false, is_last_page: false};
      controller.getFetchSuccess(response);
      return expect(ProgressBarService.complete).toHaveBeenCalled();
    });
  });

  describe('.getFetchFailure', function () {
    let response = {status: 400, statusText: 'Bad request'};
    beforeEach(function () {
      spyOn(ProgressBarService, 'complete');
      return spyOn(sweet, 'show');
    });

    it('stops the progress bar', function () {
      controller.getFetchFailure(response);
      return expect(ProgressBarService.complete).toHaveBeenCalled();
    });

    return it('calls seet alert with error', function () {
      controller.getFetchFailure(response);
      return expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to fetch tenants. Error: 400 Bad request.', 'error');
    });
  });


  describe('.editItem', function () {
    let tenant = {key: 'dhjad897d987fadafg708hb55'};

    beforeEach(() => spyOn($state, 'go'));

    return it("route to the 'tenantDetails' named route, passing the supplied tenant key", function () {
      controller.editItem(tenant);
      return expect($state.go).toHaveBeenCalledWith('tenantDetails', {tenantKey: tenant.key});
    });
  });

  return describe('.deleteItem', function () {
    let tenant = {
      key: 'dhjad897d987fadafg708fg7d',
      name: 'Foobar3',
      created: '2015-05-10 22:15:10',
      updated: '2015-05-10 22:15:10'
    };

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(TenantsService, 'delete').and.returnValue(promise);
      spyOn(controller, 'initialize');
      return spyOn(sweet, 'show').and.callFake((options, callback) => callback());
    });

    it('call TenantsService.delete tenant', function () {
      controller.deleteItem(tenant);
      promise.resolve();
      return expect(TenantsService.delete).toHaveBeenCalledWith(tenant);
    });

    it("the 'then' handler calls initialize to re-fetch all tenants", function () {
      controller.deleteItem(tenant);
      promise.resolve();
      return expect(controller.initialize).toHaveBeenCalled;
    });

    return it("the SweetAlert confirmation should be shown", function () {
      controller.deleteItem(tenant);
      promise.resolve();
      return expect(sweet.show).toHaveBeenCalled;
    });
  });
});

