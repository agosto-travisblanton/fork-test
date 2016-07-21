import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

import ToastsServiceClass from './../../../app/services/toasts.service'
import TenantsServiceClass from './../../../app/services/tenants.service'
import LocationsServiceClass from './../../../app/services/locations.service'


describe('TenantLocationCtrl', function () {
  let scope = undefined;
  let sweet = undefined;
  let $controller = undefined;
  let controller = undefined;
  let $state = undefined;
  let $stateParams = undefined;
  let TenantsService = undefined;
  let LocationsService = undefined;
  let ToastsService = undefined;
  let serviceInjection = undefined;
  let tenantsServicePromise = undefined;
  let locationsServicePromise = undefined;

  beforeEach(module('skykitProvisioning'));

  // beforeEach(module(function ($provide) {
  //   $provide.service('TenantsService', TenantsServiceClass);
  //   $provide.service('ToastsService', ToastsServiceClass);
  //   $provide.service('LocationsService', LocationsServiceClass);
  // }));

  beforeEach(inject(function (_$controller_, _TenantsService_, _LocationsService_, _$state_, _$rootScope_, _sweet_,
                              _ToastsService_) {
    $controller = _$controller_;
    $state = _$state_;
    sweet = _sweet_;
    $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'};
    let $rootScope = _$rootScope_;
    TenantsService = _TenantsService_;
    LocationsService = _LocationsService_;
    ToastsService = _ToastsService_;
    scope = $rootScope.$new();
    return serviceInjection = {
      $scope: scope,
      $stateParams
    };
  }));

  describe('initialization', function () {
    controller = undefined;

    beforeEach(function () {
      tenantsServicePromise = new skykitProvisioning.q.Mock();
      locationsServicePromise = new skykitProvisioning.q.Mock();
      return controller = $controller('TenantLocationCtrl', serviceInjection);
    });

    it('should set tenantKey to $stateParams.tenantKey', () => expect(controller.tenantKey).toBe($stateParams.tenantKey));

    describe('editing an existing location', function () {
      beforeEach(function () {
        $stateParams = {locationKey: 'fahdsfyudsyfauisdyfoiusydfu'};
        serviceInjection = {
          $scope: scope,
          $stateParams,
          TenantsService,
          LocationsService
        };
        spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise);
        spyOn(LocationsService, 'getLocationByKey').and.returnValue(locationsServicePromise);
        return controller = $controller('TenantLocationCtrl', serviceInjection);
      });

      it('should set editMode to true', () => expect(controller.editMode).toBeTruthy());

      return it('should call LocationsService.getLocationByKey', () => expect(LocationsService.getLocationByKey).toHaveBeenCalledWith($stateParams.locationKey));
    });

    return describe('.initialize', () =>
      beforeEach(function () {
        serviceInjection = {
          $scope: scope,
          $stateParams,
          LocationsService
        };
        controller = $controller('TenantLocationCtrl', serviceInjection);
        return controller.initialize();
      })
    );
  });

  describe('.onClickSaveButton', function () {
    controller = undefined;
    let progressBarService = {
      start() {
      },
      complete() {
      }
    };
    beforeEach(function () {
      let locationServicePromise = new skykitProvisioning.q.Mock();
      spyOn(LocationsService, 'save').and.returnValue(locationServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      serviceInjection = {
        ProgressBarService: progressBarService,
        LocationsService,
        ToastsService
      };
      controller = $controller('TenantLocationCtrl', serviceInjection);
      controller.location = {};
      return controller.onClickSaveButton();
    });

    it('starts the progress bar animation', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call LocationsService.save, pass the current tenant', () => expect(LocationsService.save).toHaveBeenCalledWith(controller.location));

    describe('.onSuccessSavingLocation', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onSuccessSavingLocation();
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it("displays a success toast", () => expect(ToastsService.showSuccessToast).toHaveBeenCalledWith('We saved your location.'));
    });

    describe('.onSuccessUpdatingLocation', function () {
      let tenant_key = 'some key';
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        controller.editMode = true;
        return controller.onSuccessUpdatingLocation(tenant_key);
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it("displays a success toast", () => expect(ToastsService.showSuccessToast).toHaveBeenCalledWith('We updated your location.'));
    });

    describe('.onFailureSavingLocation 409 conflict', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showErrorToast');
        spyOn(sweet, 'show');
        let errorObject = {status: 409};
        return controller.onFailureSavingLocation(errorObject);
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());

      it('displays an error toast', function () {
        let error = 'Location code conflict. Unable to save your location.';
        return expect(ToastsService.showErrorToast).toHaveBeenCalledWith(error);
      });

      return it("shows an error alert", function () {
        let expectedError =
          'Please change your customer location name. Location name must generate a unique location code.';
        return expect(sweet.show).toHaveBeenCalledWith('Oops...', expectedError, 'error');
      });
    });

    return describe('.onFailureSavingLocation general error', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showErrorToast');
        let errorObject = {status: 400};
        return controller.onFailureSavingLocation(errorObject);
      });

      it('stops the progress bar animation', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it("display error toast", function () {
        let expectedError = 'Unable to save your location.';
        return expect(ToastsService.showErrorToast).toHaveBeenCalledWith(expectedError);
      });
    });
  });

  return describe('.autoGenerateCustomerLocationCode', function () {
    beforeEach(() => controller = $controller('TenantLocationCtrl', serviceInjection));

    it('generates a new customer location code when key is undefined', function () {
      controller.location.key = undefined;
      controller.location.customerLocationName = 'Back of Store';
      controller.autoGenerateCustomerLocationCode();
      return expect(controller.location.customerLocationCode).toBe('back_of_store');
    });

    return it('skips generating a new customer location code when key is defined', function () {
      controller.location.key = 'd8ad97ad87afg897f987g0f8';
      controller.location.customerLocationName = 'Foobar Inc.';
      controller.location.customerLocationCode = 'back_of_store';
      controller.autoGenerateCustomerLocationCode();
      return expect(controller.location.customerLocationCode).toBe('back_of_store');
    });
  });
});

