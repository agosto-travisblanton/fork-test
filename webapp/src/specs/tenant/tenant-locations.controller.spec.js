import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('TenantLocationsCtrl', function () {
  let scope = undefined;
  let $controller = undefined;
  let $state = undefined;
  let $stateParams = undefined;
  let TenantsService = undefined;
  let LocationsService = undefined;
  let serviceInjection = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _TenantsService_, _LocationsService_, _$state_, _$rootScope_) {
    $controller = _$controller_;
    $state = _$state_;
    $stateParams = {};
    let $rootScope = _$rootScope_;
    TenantsService = _TenantsService_;
    LocationsService = _LocationsService_;
    scope = $rootScope.$new();
    return serviceInjection = {
      $scope: scope,
      $stateParams,
      TenantsService,
      LocationsService
    };
  }));

  describe('.initialize', function () {
    let tenantKey = 'some key';
    return beforeEach(function () {
      let tenantsServicePromise = new skykitProvisioning.q.Mock();
      let locationsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise);
      spyOn(LocationsService, 'getLocationsByTenantKey').and.returnValue(locationsServicePromise);
      let controller = $controller('TenantLocationsCtrl', serviceInjection);
      controller.tenantKey = tenantKey;
      controller.initialize();

      it('calls TenantsService.getTenantByKey with tenantKey', () => expect(TenantsService.getTenantByKey).toHaveBeenCalledWith(tenantKey));

      return it('calls LocationsService.getLocationsByTenantKey with tenantKey', () => expect(LocationsService.getLocationsByTenantKey).toHaveBeenCalledWith(tenantKey));
    });
  });
});

