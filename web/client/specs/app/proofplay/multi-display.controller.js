import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject


describe('ProofOfPlayMultiDisplayCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let ProofPlayService = undefined;
  let $stateParams = undefined;
  let $state = undefined;
  let ToastsService = undefined;
  let promise = undefined;
  let selected_tenant = undefined;


  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _ProofPlayService_, _ToastsService_, _$state_) {
    $controller = _$controller_;
    ProofPlayService = _ProofPlayService_;
    ToastsService = _ToastsService_;
    $stateParams = {};
    $state = _$state_;
    return controller = $controller('ProofOfPlayMultiDisplayCtrl', {
      ProofPlayService,
      ToastsService,
      $stateParams,
      $state
    });
  }));

  describe('initialization', function () {
    it('radioButtonChoices should equal', function () {
      let radioButtonChoices = {
        group1: 'By Date',
        group2: 'Summarized',
        selection: null
      };
      return expect(angular.equals(radioButtonChoices, controller.radioButtonChoices)).toBeTruthy();
    });

    it('dateTimeSelection should equal', function () {
      let dateTimeSelection = {
        start: null,
        end: null
      };
      return expect(angular.equals(dateTimeSelection, controller.dateTimeSelection)).toBeTruthy();
    });


    it('dateTimeSelection should equal', function () {
      let formValidity = {
        start_date: false,
        end_date: false,
        displays: false,
      };
      return expect(angular.equals(formValidity, controller.formValidity)).toBeTruthy();
    });

    return it('config objects should equal', function () {
      expect(controller.no_cache).toBeTruthy();
      expect(controller.loading).toBeTruthy();
      expect(controller.disabled).toBeTruthy();
      return expect(angular.isArray(controller.selected_displays)).toBeTruthy();
    });
  });


  describe('.initialize', function () {
    let devicesData = {
      data: {
        devices: ["one resource", "two resource", "three resource", "four"]
      }
    };

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      let querySearch = function () {
      };
      spyOn(ProofPlayService, 'getAllDisplays').and.returnValue(promise);
      spyOn(ProofPlayService, 'querySearch').and.returnValue(querySearch);
      spyOn(ProofPlayService, 'downloadCSVForMultipleDevicesByDate').and.returnValue(true);
      return spyOn(ProofPlayService, 'downloadCSVForMultipleDevicesSummarized').and.returnValue(true);
    });


    it('call getAllDisplays to populate autocomplete with devices', function () {
      controller.initialize();
      promise.resolve(devicesData);
      return expect(ProofPlayService.getAllDisplays).toHaveBeenCalled();
    });


    it('call querySearch accesses service', function () {
      controller.initialize();
      controller.querySearch(devicesData.data.devices, "one");
      return expect(ProofPlayService.querySearch).toHaveBeenCalled();
    });

    it("isRadioValid function sets formValidity type", function () {
      controller.isRadioValid("test");
      return expect(controller.formValidity.type).toBe("test");
    });

    it("the 'then' handler caches the retrieved devices data in the controller and loading to be done", function () {
      controller.initialize();
      promise.resolve(devicesData);
      expect(controller.displays).toBe(devicesData.data.devices);
      return expect(controller.loading).toBeFalsy();
    });


    it('isStartDateValid sets formValidity start_date', function () {
      let someDate = new Date();
      controller.isStartDateValid(someDate);
      return expect(controller.formValidity.start_date).toBe(true);
    });

    it('isEndDateValid sets formValidity end_date', function () {
      let someDate = new Date();
      controller.isEndDateValid(someDate);
      return expect(controller.formValidity.end_date).toBe(true);
    });


    it('isDisplayValid returns validity', function () {
      controller.initialize();
      promise.resolve(devicesData);

      controller.selected_displays = [devicesData.data.devices[0]];
      let resourceValidity = controller.isDisplayValid(devicesData.data.devices[0]);
      expect(resourceValidity).toBeFalsy();
      controller.selected_displays = [];
      let newResourceValidity = controller.isDisplayValid(devicesData.data.devices[0]);
      expect(newResourceValidity).toBeTruthy();
      newResourceValidity = controller.isDisplayValid("something not in devices");
      return expect(newResourceValidity).toBeFalsy();
    });


    it('areDisplaysValid sets formValidity devices value', function () {
      controller.selected_displays = ["at least one value here"];
      controller.areDisplaysValid();
      return expect(controller.formValidity.displays).toBeTruthy();
    });

    it('disabled is false if formValidity keys are true', function () {
      controller.formValidity.start_date = true;
      controller.formValidity.end_date = true;
      controller.formValidity.displays = true;
      controller.formValidity.type = true;
      controller.isDisabled();
      return expect(controller.disabled).toBeFalsy();
    });


    it('adds to selected resource if resource is valid', function () {
      controller.initialize();
      promise.resolve(devicesData);
      controller.addToSelectedDisplays(devicesData.data.devices[0]);
      expect(angular.equals(controller.displays, ["two resource", "three resource", "four"])).toBeTruthy();
      return expect(angular.equals(controller.selected_displays, ['one resource'])).toBeTruthy();
    });


    it('removes from selected resource', function () {
      controller.initialize();
      promise.resolve(devicesData);
      controller.addToSelectedDisplays(devicesData.data.devices[0]);
      controller.removeFromSelectedDisplay(devicesData.data.devices[0]);
      return expect(controller.selected_displays.length).toEqual(0);
    });


    return it('opens window when submit gets called', function () {
      controller.final = {
        start_date_unix: moment(new Date()).unix(),
        end_date_unix: moment(new Date()).unix(),
        displays: ["some", "devices"],
        type: "1"
      };
      controller.submit();
      expect(ProofPlayService.downloadCSVForMultipleDevicesByDate).toHaveBeenCalled();

      controller.final.type = "2";
      controller.submit();
      return expect(ProofPlayService.downloadCSVForMultipleDevicesSummarized).toHaveBeenCalled();
    });
  });

  return describe('.tenant change related functions', function () {
    selected_tenant = "some_tenant";
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn($state, 'go');
      spyOn(ProofPlayService, 'getAllDisplays').and.returnValue(promise);
      return spyOn(ProofPlayService, 'getAllTenants').and.returnValue(promise);
    });


    it('initializeTenantSelection sets tenants', function () {
      controller.initialize_tenant_select();
      let to_resolve = {
        data: {
          tenants: ["one", "two"]
        }
      };
      promise.resolve(to_resolve);
      return expect(controller.tenants).toEqual(["one", "two"]);
    });


    return it('submitTenants sets currentTenant and getsAllDisplays again', function () {
      controller.submitTenant(selected_tenant);
      return expect($state.go).toHaveBeenCalledWith('proofDetail', {tenant: selected_tenant});
    });
  });
});
