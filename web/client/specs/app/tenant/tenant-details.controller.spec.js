import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

import TenantsServiceClass from './../../../app/services/tenants.service'
import DistributorServiceClass from './../../../app/services/distributors.service'
import DomainsServiceClass from './../../../app/services/domains.service'
import TimezonesServiceClass from './../../../app/services/timezones.service'

describe('TenantDetailsCtrl', function () {
  let $scope = undefined;
  let $controller = undefined;
  let controller = undefined;
  let $state = undefined;
  let $stateParams = undefined;
  let TenantsService = undefined;
  let DomainsService = undefined;
  let TimezonesService = undefined;
  let DistributorsService = undefined;
  let progressBarService = undefined;
  let tenantsServicePromise = undefined;
  let distributorsServicePromise = undefined;
  let distributorsDomainsServicePromise = undefined;
  let domainsServicePromise = undefined;
  let timezoneServicePromise = undefined;
  let sweet = undefined;
  let serviceInjection = undefined;

  beforeEach(module('skykitProvisioning'));

  //
  // beforeEach(module(function ($provide) {
  //   $provide.service('TenantsService', TenantsServiceClass);
  //   $provide.service('DomainsService', DomainsServiceClass);
  //   $provide.service('TimezonesService', TimezonesServiceClass);
  //   $provide.service('DistributorsService', DistributorServiceClass);
  // }));


  beforeEach(inject(function (_$controller_,
                              _TenantsService_,
                              _DomainsService_,
                              _TimezonesService_,
                              _DistributorsService_,
                              _$state_, _sweet_) {
    $controller = _$controller_;
    $state = _$state_;
    $stateParams = {};
    TenantsService = _TenantsService_;
    DomainsService = _DomainsService_;
    TimezonesService = _TimezonesService_;
    DistributorsService = _DistributorsService_;
    progressBarService = {
      start() {
      },
      complete() {
      }
    };
    sweet = _sweet_;
    $scope = {
      $watch() {
      }
    };
    return serviceInjection = {
      $scope,
      $stateParams,
      ProgressBarService: progressBarService
    };
  }));

  describe('initialization', function () {
    beforeEach(function () {
      tenantsServicePromise = new skykitProvisioning.q.Mock();
      distributorsServicePromise = new skykitProvisioning.q.Mock();
      distributorsDomainsServicePromise = new skykitProvisioning.q.Mock();
      domainsServicePromise = new skykitProvisioning.q.Mock();
      timezoneServicePromise = new skykitProvisioning.q.Mock();
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise);
      spyOn(DistributorsService, 'getDomainsByKey').and.returnValue(distributorsDomainsServicePromise);
      spyOn(DomainsService, 'getDomainByKey').and.returnValue(domainsServicePromise);
      return spyOn(TimezonesService, 'getCustomTimezones').and.returnValue(timezoneServicePromise);
    });

    it('gameStopServer should be set', function () {
      controller = $controller('TenantDetailsCtrl', serviceInjection);
      return expect(controller.gameStopServer).toBeDefined();
    });

    it('currentTenant should be set', function () {
      controller = $controller('TenantDetailsCtrl', serviceInjection);
      expect(controller.currentTenant).toBeDefined();
      return expect(controller.currentTenant.active).toBeTruthy();
    });

    it('selectedDomain should be defined', function () {
      controller = $controller('TenantDetailsCtrl', serviceInjection);
      return expect(controller.selectedDomain).toBeUndefined();
    });

    it('distributorDomains property should be defined', function () {
      controller = $controller('TenantDetailsCtrl', serviceInjection);
      return expect(controller.distributorDomains).toBeDefined();
    });

    describe('editing an existing tenant', function () {
      beforeEach(function () {
        $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'};
        return serviceInjection = {
          $scope,
          $stateParams,
          ProgressBarService: progressBarService
        };
      });

      it('editMode should be set to true', function () {
        controller = $controller('TenantDetailsCtrl', serviceInjection);
        return expect(controller.editMode).toBeTruthy();
      });

      return it('retrieve tenant by key from TenantsService', function () {
        controller = $controller('TenantDetailsCtrl', serviceInjection);
        let tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'};
        tenantsServicePromise.resolve(tenant);
        expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey);
        return expect(controller.currentTenant).toBe(tenant);
      });
    });

    describe('creating a new tenant', function () {
      it('editMode should be set to false', function () {
        $stateParams = {};
        controller = $controller('TenantDetailsCtrl', serviceInjection);
        return expect(controller.editMode).toBeFalsy();
      });

      return it('do not call TenantsService.getTenantByKey', function () {
        $stateParams = {};
        controller = $controller('TenantDetailsCtrl', serviceInjection);
        return expect(TenantsService.getTenantByKey).not.toHaveBeenCalled();
      });
    });

    describe('.initialize', function () {
      beforeEach(function () {
        controller = $controller('TenantDetailsCtrl', serviceInjection);
        return controller.currentDistributorKey = 'some-key';
      });

      it('calls TimezonesService.getUsTimezones to retrieve US timezones', function () {
        controller.initialize();
        return expect(TimezonesService.getCustomTimezones).toHaveBeenCalled();
      });

      return it('calls DistributorsService.getDomainsByKey to retrieve distributor domains', function () {
        controller.initialize();
        return expect(DistributorsService.getDomainsByKey).toHaveBeenCalledWith(controller.currentDistributorKey);
      });
    });

    return describe('.onSuccessResolvingTenant', function () {
      let tenant = {domain_key: 'some_key'};
      beforeEach(() => controller = $controller('TenantDetailsCtrl', serviceInjection));

      return it('calls DomainsService.getDomainByKey to retrieve domain', function () {
        controller.onSuccessResolvingTenant(tenant);
        return expect(DomainsService.getDomainByKey).toHaveBeenCalledWith(tenant.domain_key);
      });
    });
  });

  describe('.onClickSaveButton', function () {
    let domain_key = undefined;

    beforeEach(function () {
      tenantsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(TenantsService, 'save').and.returnValue(tenantsServicePromise);
      spyOn($state, 'go');
      $stateParams = {};
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('TenantDetailsCtrl', serviceInjection);
      domain_key = '1231231231312';
      controller.selectedDomain = {key: domain_key};
      controller.onClickSaveButton();
      return tenantsServicePromise.resolve();
    });

    it('sets the domain_key on the current tenant from the selected domain', () => expect(controller.currentTenant.domain_key).toEqual(domain_key));

    it('starts the progress bar animation', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call TenantsService.save, pass the current tenant', () => expect(TenantsService.save).toHaveBeenCalledWith(controller.currentTenant));

    describe('.onSuccessTenantSave', function () {
      beforeEach(() => controller.onSuccessTenantSave());

      return it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());
    });


    describe('.onFailureTenantSave 409 conflict', function () {
      beforeEach(function () {
        spyOn(sweet, 'show');
        let errorObject = {status: 409};
        return controller.onFailureTenantSave(errorObject);
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());


      return it("show the error dialog", function () {
        let expectedError = 'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.';
        return expect(sweet.show).toHaveBeenCalledWith('Oops...', expectedError, 'error');
      });
    });

    return describe('.onFailureTenantSave general error', function () {
      beforeEach(function () {
        spyOn(sweet, 'show');
        this.errorObject = {status: 400};
        return controller.onFailureTenantSave(this.errorObject);
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it("show the error dialog", function () {
        let expectedError = 'Unable to save the tenant.';
        return expect(sweet.show).toHaveBeenCalledWith('Oops...', expectedError, 'error');
      });
    });
  });

  return describe('.autoGenerateTenantCode', function () {
    beforeEach(() => controller = $controller('TenantDetailsCtrl', serviceInjection));

    it('generates a new tenant code when key is undefined', function () {
      controller.currentTenant.key = undefined;
      controller.currentTenant.name = 'Super Duper Foobar Inc.';
      controller.autoGenerateTenantCode();
      return expect(controller.currentTenant.tenant_code).toBe('super_duper_foobar_inc');
    });

    return it('skips generating a new tenant code when key is defined', function () {
      controller.currentTenant.key = 'd8ad97ad87afg897f987g0f8';
      controller.currentTenant.name = 'Foobar Inc.';
      controller.currentTenant.tenant_code = 'barfoo_company';
      controller.autoGenerateTenantCode();
      return expect(controller.currentTenant.tenant_code).toBe('barfoo_company');
    });
  });
});
