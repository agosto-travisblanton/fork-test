import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject
let controller = undefined;

describe('TenantLogsCtrl', function () {
  let scope = undefined;
  let $timeout = undefined;
  let $controller = undefined;
  let $state = undefined;
  let $stateParams = undefined;
  let TenantsService = undefined;
  let serviceInjection = undefined;
  let tenantsServicePromise = undefined;
  let IntegrationEvents = undefined;
  let ProgressBarService = undefined;
  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_,
                              _$timeout_,
                              _$q_,
                              _TenantsService_,
                              _DevicesService_,
                              _ProgressBarService_,
                              _DateManipulationService_,
                              _$state_,
                              _IntegrationEvents_,
                              _$rootScope_) {
    $controller = _$controller_;
    $state = _$state_;
    $stateParams = {};
    let $rootScope = _$rootScope_;
    TenantsService = _TenantsService_;
    IntegrationEvents = _IntegrationEvents_;
    DevicesService = _DevicesService_;
    ProgressBarService = _ProgressBarService_;
    $timeout = _$timeout_;
    scope = $rootScope.$new();
    serviceInjection = {
      $scope: scope,
      $stateParams,
      IntegrationEvents,
      TenantsService,
      DevicesService,
      ProgressBarService
    };
    $q = _$q_;
    controller = $controller('TenantLogsCtrl', serviceInjection);

  }));

  describe('TenantOverlaysCtrl', function () {
    beforeEach(function () {
      tenantsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(ProgressBarService, 'start')
      spyOn(ProgressBarService, 'complete')

      spyOn(IntegrationEvents, 'getTenantCreateEvents').and.returnValue(tenantsServicePromise);
      spyOn(TenantsService, 'getTenantByKey')

    });

    describe('getTenantCreateEvents', function () {
      it('gets tenant create events', function () {
        controller.getTenantCreateEvents()
        let toResolve = [
          {"blah": true},
          {"gah": false}
        ]
        tenantsServicePromise.resolve(toResolve)
        expect(controller.tenantCreateEvents).toEqual(toResolve);
      })
    });
  });
})
;
