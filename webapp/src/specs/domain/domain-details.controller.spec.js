import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject


describe('DomainDetailsCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let $stateParams = undefined;
  let $state = undefined;
  let $log = undefined;
  let DomainsService = undefined;
  let ToastsService = undefined;
  let domainsServicePromise = undefined;
  let progressBarService = undefined;
  let sweet = undefined;
  let serviceInjection = undefined;

  let domain = {
    key: 'ahjad897d987fadafg708fg71',
    name: 'bob.agosto.com',
    impersonation_admin_email_address: 'bob.macneal@skykit.com',
    created: '2015-09-08 12:15:08',
    updated: '2015-09-08 12:15:08'
  };

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _DomainsService_, _sweet_, _ToastsService_, _$log_) {
    $controller = _$controller_;
    $stateParams = {};
    $state = {};
    $log = _$log_;
    DomainsService = _DomainsService_;
    progressBarService = {
      start() {
      },
      complete() {
      }
    };
    sweet = _sweet_;
    ToastsService = _ToastsService_;
    let scope = {};
    return serviceInjection = {
      $scope: scope,
      $stateParams,
      ProgressBarService: progressBarService,
      DomainsService,
      ToastsService,
      $log
    };
  }));

  describe('initialization', function () {
    beforeEach(function () {
      domainsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(DomainsService, 'getDomainByKey').and.returnValue(domainsServicePromise);
    });

    describe('new mode', function () {
      beforeEach(() => controller = $controller('DomainDetailsCtrl', serviceInjection));

      return it('currentDomain property should be defined', () => expect(controller.currentDomain).toBeDefined());
    });

    return describe('edit mode', function () {
      beforeEach(function () {
        $stateParams.domainKey = 'fkasdhfjfa9s8udyva7dygoudyg';
        return controller = $controller('DomainDetailsCtrl', serviceInjection);
      });

      it('currentDomain.organization_unit_path property should be set to default value', () =>
        expect(controller.currentDomain.organization_unit_path).toBe('/skykit'));

      it('devicesAccess property should be false', () => expect(controller.devicesAccess).toBeFalsy());

      it('orgUnitsAccess property should be false', () => expect(controller.orgUnitsAccess).toBeFalsy());

      it('usersAccess property should be false', () => expect(controller.usersAccess).toBeFalsy());

      it('currentDomain property should be defined', () => expect(controller.currentDomain).toBeDefined());

      it('call DomainsService.getDomainByKey to retrieve the selected domain', () => expect(DomainsService.getDomainByKey).toHaveBeenCalledWith($stateParams.domainKey));

      return it("the 'then' handler caches the retrieved domain in the controller", function () {
        domainsServicePromise.resolve(domain);
        return expect(controller.currentDomain).toBe(domain);
      });
    });
  });

  describe('.onSaveDomain', function () {
    beforeEach(function () {
      domainsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(DomainsService, 'save').and.returnValue(domainsServicePromise);
      spyOn(progressBarService, 'start');
      controller = $controller('DomainDetailsCtrl', serviceInjection);
      return controller.onSaveDomain();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call DevicesService.save with the current device', () => expect(DomainsService.save).toHaveBeenCalledWith(controller.currentDomain));

    describe('.onSuccessSaveDomain', function () {
      beforeEach(function () {
        spyOn(progressBarService, 'complete');
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onSuccessSaveDomain();
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it("displays a success toast", () => expect(ToastsService.showSuccessToast).toHaveBeenCalledWith('We saved your update.'));
    });

    return describe('.onFailureSaveDomain', function () {
      let errorObject = {status: 409, statusText: 'Conflict'};

      beforeEach(() => spyOn(progressBarService, 'complete'));

      it('stops the progress bar', function () {
        controller.onFailureSaveDomain(errorObject);
        return expect(progressBarService.complete).toHaveBeenCalled();
      });

      describe('409 conflict returned from server', function () {
        beforeEach(function () {
          spyOn(sweet, 'show');
          spyOn($log, 'info');
          return controller.onFailureSaveDomain(errorObject);
        });

        it('displays a sweet alert when domain conflicts with existing domain', () =>
          expect(sweet.show).toHaveBeenCalledWith('Oops...',
            'This domain name already exist. Please enter a unique domain name.', 'error')
        );

        return it('logs info to the console when domain conflicts with existing domain', function () {
          let infoMessage = `Failure saving domain. Domain already exists: ${errorObject.status} ${errorObject.statusText}`;
          return expect($log.info).toHaveBeenCalledWith(infoMessage);
        });
      });

      return describe('general error returned from server', function () {
        let generalError = {status: 400, statusText: 'Some error'};

        beforeEach(function () {
          spyOn($log, 'error');
          spyOn(ToastsService, 'showErrorToast');
          return controller.onFailureSaveDomain(generalError);
        });

        it('logs error to the console', function () {
          let errorMessage = `Failure saving domain: ${generalError.status} ${generalError.statusText}`;
          return expect($log.error).toHaveBeenCalledWith(errorMessage);
        });

        return it('displays a toast regarding failure to save the domain', function () {
          let toastMessage = 'Oops. We were unable to save your updates at this time.';
          return expect(ToastsService.showErrorToast).toHaveBeenCalledWith(toastMessage);
        });
      });
    });
  });

  describe('.onSuccessDeterminingConnectivity', function () {
    let exception = 'unauthorized_client'
    let response = {
      'devicesAccess': true,
      'orgUnitsAccess': false,
      'usersAccess': true,
      'orgUnitsAccessException': exception};

    beforeEach(function () {
      spyOn(progressBarService, 'complete');
      controller = $controller('DomainDetailsCtrl', serviceInjection);
      return controller.onSuccessDeterminingConnectivity(response);
    });

    it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

    it('sets devicesAccess', () => expect(controller.devicesAccess).toBeTruthy());

    it('sets usersAccess', () => expect(controller.usersAccess).toBeTruthy());

    it('sets orgUnitsAccessException', () => expect(controller.orgUnitsAccessException).toBe(exception));

    it('does not set devicesAccessException', () => expect(controller.devicesAccessException).toBeUndefined());

    it('does not set usersAccessException', () => expect(controller.usersAccessException).toBeUndefined());

    return it('sets orgUnitsAccess', () => expect(controller.orgUnitsAccess).toBeFalsy());

  });

  describe('.onFailureDeterminingConnectivity', function () {
    let response = {'status': 400, 'statusText': 'Something horrific'};

    beforeEach(function () {
      spyOn(progressBarService, 'complete');
      controller = $controller('DomainDetailsCtrl', serviceInjection);
      spyOn($log, 'error');
      spyOn(ToastsService, 'showErrorToast');
      return controller.onFailureDeterminingConnectivity(response);
    });

    it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

    it('logs detailed error to console', () => expect($log.error).toHaveBeenCalledWith('Failure determining directory API connectivity: 400 Something horrific'));

    return it('displays a toast regarding failure to determine device connectivity', function () {
      let toastMessage = 'Oops. We were unable determine your device connectivity at this time.';
      return expect(ToastsService.showErrorToast).toHaveBeenCalledWith(toastMessage);
    });
  });

  return describe('.initialize', function () {
    let domainUrlSafeKey = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyEwsSBkRvbWFpbhiAgICgvIm8Cww';

    beforeEach(function () {
      domainsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(DomainsService, 'getDirectoryApiConnectivityInformation').and.returnValue(domainsServicePromise);
      spyOn(progressBarService, 'start');
      controller = $controller('DomainDetailsCtrl', serviceInjection);
      $stateParams.domainKey = domainUrlSafeKey;
      controller.editMode = true;
      return controller.initialize();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    return it('calls DevicesService.getDirectoryApiConnectivityInformation', () => expect(DomainsService.getDirectoryApiConnectivityInformation).toHaveBeenCalledWith(domainUrlSafeKey));
  });
});
