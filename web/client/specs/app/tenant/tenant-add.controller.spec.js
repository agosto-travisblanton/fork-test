import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject


describe('TenantAddCtrl', function () {
  let $cookies = undefined;
  let controllerFactory = undefined;
  let controller = undefined;
  let controllerGameStop = undefined;
  let DistributorsService = undefined;
  let TimezonesService = undefined;
  let distributorKey = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldml0aXR5R3JvdXAMCxILRGlzdHJpYnV0b3IYgICAgMCcggoM';
  let distributorPromise = undefined;
  let distributorDomainsPromise = undefined;
  let timezonesPromise = undefined;
  let TenantsService = undefined;
  let StorageService = undefined;
  let tenantsServicePromise = undefined;
  let progressBarService = undefined;
  let $state = undefined;
  let sweet = undefined;
  let $log = undefined;
  let $location = undefined;

  beforeEach(function () {
    angular.mock.module('skykitProvisioning');

    return inject(function (_$controller_, _DistributorsService_, _TimezonesService_, _StorageService_, _TenantsService_, _$state_, _sweet_,
                            _$log_, _$location_) {
      controllerFactory = _$controller_;
      DistributorsService = _DistributorsService_;
      TimezonesService = _TimezonesService_;
      TenantsService = _TenantsService_;
      $state = _$state_;
      sweet = _sweet_;
      $log = _$log_;
      StorageService = _StorageService_;
      $location = _$location_;
      progressBarService = {
        start() {
        },
        complete() {
        }
      };
      controller = controllerFactory('TenantAddCtrl',
        {
          StorageService,
          DistributorsService,
          TenantsService,
          ProgressBarService: progressBarService,
          $location: {
            host() {
              return 'localhost';
            }
          }
        }
      );
      controllerGameStop = controllerFactory('TenantAddCtrl',
        {
          $location: {
            host() {
              return 'provisioning-gamestop';
            }
          }
        }
      );
      return;
    });
  });

  describe('upon instantiation', function () {
    it('sets gameStopServer false unless on GameStop host', function () {
      expect(controller.gameStopServer).toBeFalsy();
      return expect(controllerGameStop.gameStopServer).toBeTruthy();
    });

    it('declares a currentTenant who is active and has proof of play turned off', function () {
      expect(controller.currentTenant).toBeDefined();
      expect(controller.currentTenant.active).toBeTruthy();
      return expect(controller.currentTenant.proof_of_play_logging).toBeFalsy();
    });

    it('declares a currentTenant that has content_manager_url declared but not defined', () => expect(controller.currentTenant.content_manager_url).toBeUndefined());

    it('declares a currentTenant that has player_content_url declared but not defined', () => expect(controller.currentTenant.player_content_url).toBeUndefined());

    it('declares a selectedDomain', () => expect(controller.selectedDomain).toBeUndefined());

    it('declares distributorDomains as an empty array', function () {
      expect(angular.isArray(controller.distributorDomains)).toBeTruthy();
      return expect(controller.distributorDomains.length).toBe(0);
    });

    it('declares timezones as an empty array', function () {
      expect(angular.isArray(controller.timezones)).toBeTruthy();
      return expect(controller.timezones.length).toBe(0);
    });

    return it('sets a selectedTimezone', () => expect(controller.selectedTimezone).toBe('America/Chicago'));
  });

  describe('.initialize', function () {
    beforeEach(function () {
      spyOn(StorageService, 'get').and.returnValue(distributorKey);
      distributorPromise = new skykitProvisioning.q.Mock();
      timezonesPromise = new skykitProvisioning.q.Mock();
      spyOn(DistributorsService, 'getByKey').and.returnValue(distributorPromise);
      distributorDomainsPromise = new skykitProvisioning.q.Mock();
      spyOn(DistributorsService, 'getDomainsByKey').and.returnValue(distributorDomainsPromise);
      spyOn(TimezonesService, 'getCustomTimezones').and.returnValue(timezonesPromise);
      return controller.initialize();
    });

    it('calls TimezonesService.getUsTimezones to retrieve US timezones', function () {
      controller.initialize();
      return expect(TimezonesService.getCustomTimezones).toHaveBeenCalled();
    });

    it('invokes StorageService to obtain the currentDistributorKey', () => expect(StorageService.get).toHaveBeenCalledWith('currentDistributorKey'));

    it('sets the currentDistributorKey from StorageService', () => expect(controller.currentDistributorKey).toBe(distributorKey));

    it('calls DistributorsService with distributorKey to get the distributor', () => expect(DistributorsService.getByKey).toHaveBeenCalledWith(distributorKey));

    return it('calls DistributorsService with distributorKey to get the distributor domains', () => expect(DistributorsService.getDomainsByKey).toHaveBeenCalledWith(distributorKey));
  });

  describe('.onClickSaveButton', function () {
    let domain_key = undefined;

    beforeEach(function () {
      tenantsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(TenantsService, 'save').and.returnValue(tenantsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      spyOn(sweet, 'show');
      domain_key = 'ahf39fnNreWtpdC1kaXNwbGF5LWRlxXml0aXR8R3UvdXAMCxILRGlzdHJpYnV0b3IYgICAgMCc09oM';
      controller.selectedDomain = {key: domain_key};
      return controller.onClickSaveButton();
    });

    it('sets the domain_key on the current tenant from the selected domain', () => expect(controller.currentTenant.domain_key).toEqual(domain_key));

    it('starts the progress bar animation', () => expect(progressBarService.start).toHaveBeenCalled());

    it('calls TenantsService.save with the current tenant', () => expect(TenantsService.save).toHaveBeenCalledWith(controller.currentTenant));

    describe('.onSuccessTenantSave', function () {
      beforeEach(function () {
        spyOn($state, 'go');
        return controller.onSuccessTenantSave();
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it("the 'then' handler routes navigation back to 'tenants'", () => expect($state.go).toHaveBeenCalledWith('tenants'));
    });

    describe('.onFailureTenantSave 409 conflict', function () {
      beforeEach(function () {
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
      let errorObject = undefined;

      beforeEach(function () {
        spyOn($log, 'error');
        errorObject = {status: 400};
        return controller.onFailureTenantSave(errorObject);
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());

      it('logs the error', () => expect($log.error).toHaveBeenCalledWith(errorObject));

      return it("show the error dialog", function () {
        let expectedError = 'Unable to save the tenant.';
        return expect(sweet.show).toHaveBeenCalledWith('Oops...', expectedError, 'error');
      });
    });
  });

  return describe('.autoGenerateTenantCode', function () {
    it('generates a new tenant code when key is undefined', function () {
      controller.currentTenant.key = undefined;
      controller.currentTenant.name = 'Foobar Inc.';
      controller.autoGenerateTenantCode();
      return expect(controller.currentTenant.tenant_code).toBe('foobar_inc');
    });

    return it('skips generating a new tenant code when key is defined', function () {
      controller.currentTenant.key = 'd8ad97ad87afg897f987g0f8';
      controller.currentTenant.name = 'Foobar Inc.';
      controller.currentTenant.tenant_code = 'foobar_inc';
      controller.autoGenerateTenantCode();
      return expect(controller.currentTenant.tenant_code).toBe('foobar_inc');
    });
  });
});
