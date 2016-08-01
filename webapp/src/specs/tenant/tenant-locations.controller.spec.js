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
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _TenantsService_, _LocationsService_, _$state_, _$rootScope_) {
    $controller = _$controller_;
    $state = _$state_;
    $stateParams = {};
    let $rootScope = _$rootScope_;
    TenantsService = _TenantsService_;
    LocationsService = _LocationsService_;
    scope = $rootScope.$new();
    serviceInjection = {
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

      it('calls LocationsService.getLocationsByTenantKey with tenantKey', () => expect(LocationsService.getLocationsByTenantKey).toHaveBeenCalledWith(tenantKey));
    });
  });


  describe('.searchAllTenantLocationsByName', function () {
    let tenants = [
      {
        key: 'dhjad897d987fadafg708fg7d',
        customerLocationName: 'Foobar1',
        created: '2015-05-10 22:15:10',
        updated: '2015-05-10 22:15:10'
      },
      {
        key: 'dhjad897d987fadafg708y67d',
        customerLocationName: 'Foobar2',
        created: '2015-05-10 22:15:10',
        updated: '2015-05-10 22:15:10'
      },
      {
        key: 'dhjad897d987fadafg708hb55',
        customerLocationName: 'Foobar3',
        created: '2015-05-10 22:15:10',
        updated: '2015-05-10 22:15:10'
      }
    ]

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(LocationsService, 'searchAllTenantLocationsByName').and.returnValue(promise);
    });

    it('call LocationsService.searchAllTenantLocationsByName to retrieve all tenant locations with matching name', function () {
      let controller = $controller('TenantLocationsCtrl', serviceInjection);

      controller.searchedTenantLocations = tenants;
      controller.searchAllTenantLocationsByName('Foobar');
      controller.searchedTenantLocations = tenants;
      promise.resolve(tenants);
      expect(LocationsService.searchAllTenantLocationsByName).toHaveBeenCalled();
    });

    return it("isTenantLocationValid changes searchDisabled based on if the tenant is valid", function () {
      let controller = $controller('TenantLocationsCtrl', serviceInjection);
      let tenant_name = "Foobar1"
      controller.isTenantLocationValid(tenant_name);
      promise.resolve(tenants);
      expect(controller.searchDisabled).toBe(false);
    });
  });

});


