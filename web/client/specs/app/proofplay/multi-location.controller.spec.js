import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject


describe('ProofOfPlayMultiLocationCtrl', function () {
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
    return controller = $controller('ProofOfPlayMultiLocationCtrl', {
      ProofPlayService,
      ToastsService,
      $stateParams,
      $state
    });
  }));

  describe('initialization', function () {
    it('radioButtonChoices should equal', function () {
      let radioButtonChoices = {
        group1: 'By Device',
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
        locations: false,
      };
      return expect(angular.equals(formValidity, controller.formValidity)).toBeTruthy();
    });

    return it('config objects should equal', function () {
      expect(controller.no_cache).toBeTruthy();
      expect(controller.loading).toBeTruthy();
      expect(controller.disabled).toBeTruthy();
      return expect(angular.isArray(controller.selected_locations)).toBeTruthy();
    });
  });


  describe('.initialize', function () {
    let locationsData = {
      data: {
        locations: ["one resource", "two resource", "three resource", "four"]
      }
    };

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      let querySearch = function () {
      };
      spyOn($state, 'go');
      spyOn(ProofPlayService, 'getAllLocations').and.returnValue(promise);
      spyOn(ProofPlayService, 'querySearch').and.returnValue(querySearch);
      spyOn(ProofPlayService, 'downloadCSVForMultipleLocationsByDevice').and.returnValue(true);
      return spyOn(ProofPlayService, 'downloadCSVForMultipleLocationsSummarized').and.returnValue(true);
    });


    it('call getAllLocations to populate autocomplete with locations', function () {
      controller.initialize();
      promise.resolve(locationsData);
      return expect(ProofPlayService.getAllLocations).toHaveBeenCalled();
    });


    it('call querySearch accesses service', function () {
      controller.initialize();
      controller.querySearch(locationsData.data.locations, "one");
      return expect(ProofPlayService.querySearch).toHaveBeenCalled();
    });

    it("isRadioValid function sets formValidity type", function () {
      controller.isRadioValid("test");
      return expect(controller.formValidity.type).toBe("test");
    });

    it("the 'then' handler caches the retrieved locations data in the controller and loading to be done", function () {
      controller.initialize();
      promise.resolve(locationsData);
      expect(controller.locations).toBe(locationsData.data.locations);
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


    it('isLocationValid returns validity', function () {
      controller.initialize();
      promise.resolve(locationsData);

      controller.selected_locations = [locationsData.data.locations[0]];
      let resourceValidity = controller.isLocationValid(locationsData.data.locations[0]);
      expect(resourceValidity).toBeFalsy();
      controller.selected_locations = [];
      let newResourceValidity = controller.isLocationValid(locationsData.data.locations[0]);
      expect(newResourceValidity).toBeTruthy();
      newResourceValidity = controller.isLocationValid("something not in locations");
      return expect(newResourceValidity).toBeFalsy();
    });


    it('areLocationsValid sets formValidity locations value', function () {
      controller.selected_locations = ["at least one value here"];
      controller.areLocationsValid();
      return expect(controller.formValidity.locations).toBeTruthy();
    });

    it('disabled is false if formValidity keys are true', function () {
      controller.formValidity.start_date = true;
      controller.formValidity.end_date = true;
      controller.formValidity.locations = true;
      controller.formValidity.type = true;
      controller.isDisabled();
      return expect(controller.disabled).toBeFalsy();
    });


    it('adds to selected resource if resource is valid', function () {
      controller.initialize();
      promise.resolve(locationsData);
      controller.addToSelectedLocations(locationsData.data.locations[0]);
      expect(angular.equals(controller.locations, ["two resource", "three resource", "four"])).toBeTruthy();
      return expect(angular.equals(controller.selected_locations, ['one resource'])).toBeTruthy();
    });


    it('removes from selected resource', function () {
      controller.initialize();
      promise.resolve(locationsData);
      controller.addToSelectedLocations(locationsData.data.locations[0]);
      controller.removeFromSelectedLocation(locationsData.data.locations[0]);
      return expect(controller.selected_locations.length).toEqual(0);
    });


    return it('opens window when submit gets called', function () {
      controller.final = {
        start_date_unix: moment(new Date()).unix(),
        end_date_unix: moment(new Date()).unix(),
        locations: ["some", "locations"],
        type: "1"
      };
      controller.submit();
      expect(ProofPlayService.downloadCSVForMultipleLocationsByDevice).toHaveBeenCalled();

      controller.final.type = "2";
      controller.submit();
      return expect(ProofPlayService.downloadCSVForMultipleLocationsSummarized).toHaveBeenCalled();
    });
  });

  return describe('.tenant change related functions', function () {

    selected_tenant = "some_tenant";

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn($state, 'go');
      spyOn(ProofPlayService, 'getAllLocations').and.returnValue(promise);
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
