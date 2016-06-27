describe('ProofPlayService', function() {
  let ProofPlayService = undefined;
  let $http = undefined;
  let $stateParams = undefined;
  let $state = undefined;
  let ToastsService = undefined;
  let Lockr = undefined;
  let deferred = undefined;
  let $q = undefined;
  let promise = undefined;
  let $rootScope = undefined;
  let window = undefined;
  let StorageService = undefined;
  let cookie_token = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function(_$httpBackend_, _$q_, _ProofPlayService_, _$http_, _$window_, _StorageService_, _ToastsService_, _$state_) {
    ProofPlayService = _ProofPlayService_;
    $http = _$http_;
    ToastsService = _ToastsService_;
    let $httpBackend = _$httpBackend_;
    $q = _$q_;
    $stateParams = {};
    $state = _$state_;
    StorageService = _StorageService_;
    return window = _$window_;
  }));


  describe('querying for csvs', function() {
    beforeEach(function() {
      spyOn(window, 'open').and.callFake(() => true
      );
      promise = new skykitProvisioning.q.Mock();
      spyOn($state, 'go');
      spyOn($q, 'defer');
      deferred = $q.defer();
      spyOn(ToastsService, 'showErrorToast');
      spyOn(ToastsService, 'showSuccessToast');
      cookie_token = 'test';
      return StorageService.set('currentDistributorKey', cookie_token);
    });


    it('sets @uriBase variable', () => expect(ProofPlayService.uriBase).toEqual('proofplay/api/v1'));

    it('sets @cachedResources variable to null', () => expect(ProofPlayService.cachedResources).toBeFalsy());

    it('sets tenant and downloads multi-resource csv across date range', function() {
      let start_date = 12312;
      let end_date = 234234;
      let resources = ["some_resource", "another"];
      let tenants = ["one_tenant", "two_tenant"];
      ProofPlayService.downloadCSVForMultipleResourcesByDate(start_date, end_date, resources, tenants[0]);
      expect(window.open).toHaveBeenCalled();

      let allResources = [];

      for (let i = 0; i < resources.length; i++) {
        let each = resources[i];
        allResources = allResources + "|" + each;
      }

      return expect(window.open).toHaveBeenCalledWith(`proofplay/api/v1/multi_resource_by_date/${start_date}/${end_date}/${allResources}/${tenants[0]}/${cookie_token}`, '_blank');
    });


    it('sets tenant and downloadCSVForMultipleResourcesByDevice', function() {
      let start_date = 12312;
      let end_date = 234234;
      let resources = ["some_resource", "another"];
      let tenants = ["one_tenant", "two_tenant"];
      ProofPlayService.downloadCSVForMultipleResourcesByDevice(start_date, end_date, resources, tenants[0]);
      expect(window.open).toHaveBeenCalled();

      let allResources = '';

      for (let i = 0; i < resources.length; i++) {
        let each = resources[i];
        allResources = allResources + "|" + each;
      }


      return expect(window.open).toHaveBeenCalledWith(`proofplay/api/v1/multi_resource_by_device/${start_date}/${end_date}/${allResources}/${tenants[0]}/${cookie_token}`, '_blank');
    });


    it('sets tenant and downloads multi-devices summarized csv', function() {
      let start_date = 12312;
      let end_date = 234234;
      let devices = ["some_devices", "another_device"];
      let tenants = ["one_tenant", "two_tenant"];
      ProofPlayService.downloadCSVForMultipleDevicesSummarized(start_date, end_date, devices, tenants[0]);
      expect(window.open).toHaveBeenCalled();

      let allDevices = '';

      for (let i = 0; i < devices.length; i++) {
        let each = devices[i];
        allDevices = allDevices + "|" + each;
      }


      return expect(window.open).toHaveBeenCalledWith(`proofplay/api/v1/multi_device_summarized/${start_date}/${end_date}/${allDevices}/${tenants[0]}/${cookie_token}`, '_blank');
    });

    it('sets tenant and downloadCSVForMultipleDevicesByDate', function() {
      let start_date = 12312;
      let end_date = 234234;
      let devices = ["some_devices", "another_device"];
      let tenants = ["one_tenant", "two_tenant"];
      ProofPlayService.downloadCSVForMultipleDevicesByDate(start_date, end_date, devices, tenants[0]);
      expect(window.open).toHaveBeenCalled();

      let allDevices = '';

      for (let i = 0; i < devices.length; i++) {
        let each = devices[i];
        allDevices = allDevices + "|" + each;
      }


      return expect(window.open).toHaveBeenCalledWith(`proofplay/api/v1/multi_device_by_date/${start_date}/${end_date}/${allDevices}/${tenants[0]}/${cookie_token}`, '_blank');
    });

    it('sets tenant and downloadCSVForMultipleLocationsByDevice', function() {
      let start_date = 12312;
      let end_date = 234234;
      let locations = ["some_location", "another_location"];
      let tenants = ["one_tenant", "two_tenant"];
      ProofPlayService.downloadCSVForMultipleLocationsByDevice(start_date, end_date, locations, tenants[0]);
      expect(window.open).toHaveBeenCalled();

      let allLocations = '';

      for (let i = 0; i < locations.length; i++) {
        let each = locations[i];
        allLocations = allLocations + "|" + each;
      }


      return expect(window.open).toHaveBeenCalledWith(`proofplay/api/v1/multi_location_by_device/${start_date}/${end_date}/${allLocations}/${tenants[0]}/${cookie_token}`, '_blank');
    });


    return it('sets tenant and downloadCSVForMultipleLocationsSummarized', function() {
      let start_date = 12312;
      let end_date = 234234;
      let locations = ["some_location", "another_location"];
      let tenants = ["one_tenant", "two_tenant"];
      ProofPlayService.downloadCSVForMultipleLocationsSummarized(start_date, end_date, locations, tenants[0]);
      expect(window.open).toHaveBeenCalled();

      let allLocations = '';

      for (let i = 0; i < locations.length; i++) {
        let each = locations[i];
        allLocations = allLocations + "|" + each;
      }

      expect(window.open).toHaveBeenCalledWith(`proofplay/api/v1/multi_location_summarized/${start_date}/${end_date}/${allLocations}/${tenants[0]}/${cookie_token}`, '_blank');

      it('gets all tenants', function() {
        let to_respond = {
          data: {
            tenants: ["one", "two"]
          }
        };
        $httpBackend.expectGET("proofplay/api/v1/retrieve_my_tenants").respond(to_respond);
        ProofPlayService.getAllTenants()
        .then(data => expect(angular.equals(data.data.tenants, to_respond.data.tenants)));
  
        return $httpBackend.flush();
      });


      it('gets all displays of a tenant', function() {
        let to_respond = {
          data: {
            displays: ["one", "two"]
          }
        };
  
        let chosen_tenant = "some-tenant";
        $httpBackend.expectGET(`proofplay/api/v1/retrieve_all_displays/${chosen_tenant}`).respond(to_respond);
  
        ProofPlayService.getAllDisplays(chosen_tenant)
        .then(data => expect(angular.equals(data.data.displays, to_respond.data.displays)));
  
        return $httpBackend.flush();
      });

      return it('gets all locations of a tenant', function() {
        let to_respond = {
          data: {
            locations: ["one", "two"]
          }
        };
  
        let chosen_tenant = "some-tenant";
  
        $httpBackend.expectGET(`proofplay/api/v1/retrieve_all_locations/${chosen_tenant}`).respond(to_respond);
  
        ProofPlayService.getAllLocations(chosen_tenant)
        .then(data => expect(angular.equals(data.data.locations, to_respond.data.locations)));
  
        return $httpBackend.flush();
      });
    });
  });


  return describe('querySearch filters array by text', () =>
    it('filters properly', function() {
      let resources = ["some_resource", "other", "again", "otherwise"];
      let new_resources = ProofPlayService.querySearch(resources, 'oth');
      expect(angular.equals(["other", "otherwise"], new_resources)).toBeTruthy();
      let other_new_resources = ProofPlayService.querySearch(resources);
      return expect(angular.equals(other_new_resources, resources)).toBeTruthy();
    })
  );
});

