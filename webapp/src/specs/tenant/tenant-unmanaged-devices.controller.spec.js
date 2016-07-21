import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('TenantUnmanagedDevicesCtrl', function () {
  let scope = undefined;
  let $controller = undefined;
  let $state = undefined;
  let $stateParams = undefined;
  let TenantsService = undefined;
  let DevicesService = undefined;
  let ProgressBarService = undefined;
  let serviceInjection = undefined;
  let tenantsServicePromise = undefined;
  let controller = undefined;
  let partial = undefined;
  let promise = undefined;
  let devicesServicePromise = undefined;
  let serialByTenantPromise = undefined;


  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _TenantsService_, _DevicesService_, _$state_, _ProgressBarService_, _$rootScope_) {
    $controller = _$controller_;
    $state = _$state_;
    $stateParams = {};
    let $rootScope = _$rootScope_;
    TenantsService = _TenantsService_;
    DevicesService = _DevicesService_;
    ProgressBarService = _ProgressBarService_;
    scope = $rootScope.$new();
    return serviceInjection = {
      $scope: scope,
      $stateParams,
      TenantsService,
      DevicesService,
      ProgressBarService
    };
  }));

  return describe('initialization', function () {
    beforeEach(function () {
      tenantsServicePromise = new skykitProvisioning.q.Mock();
      devicesServicePromise = new skykitProvisioning.q.Mock();
      spyOn(ProgressBarService, 'start');
      spyOn(ProgressBarService, 'complete');
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise);
      return spyOn(DevicesService, 'getUnmanagedDevicesByTenant').and.returnValue(devicesServicePromise);
    });

    it('currentTenant should be set', function () {
      controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
      expect(controller.currentTenant).toBeDefined();
      expect(controller.currentTenant.key).toBeUndefined();
      expect(controller.currentTenant.name).toBeUndefined();
      expect(controller.currentTenant.tenant_code).toBeUndefined();
      expect(controller.currentTenant.admin_email).toBeUndefined();
      expect(controller.currentTenant.content_server_url).toBeUndefined();
      expect(controller.currentTenant.domain_key).toBeUndefined();
      expect(controller.currentTenant.notification_emails).toBeUndefined();
      expect(controller.currentTenant.proof_of_play_logging).toBeFalsy();
      return expect(controller.currentTenant.active).toBeTruthy();
    });

    it('tenantDevices property should be defined', function () {
      controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
      return expect(controller.tenantDevices).toBeDefined();
    });

    describe('editing an existing tenant', function () {
      beforeEach(function () {
        let progressBarService = {
          start() {
          },
          complete() {
          }
        };
        $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'};
        serviceInjection = {
          $scope: scope,
          $stateParams,
          ProgressBarService: progressBarService
        };
        promise = new skykitProvisioning.q.Mock();
        return controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
      });


      it('editMode should be set to true', () => expect(controller.editMode).toBeTruthy());

      it('retrieve tenant by key from TenantsService', function () {
        let tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'};
        tenantsServicePromise.resolve(tenant);
        expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey);
        return expect(controller.currentTenant).toBe(tenant);
      });

      return it('retrieve tenant\'s devices by tenant key from DevicesService', function () {
        let data = [1, 2, 3];
        let devices = {"devices": data};
        devicesServicePromise.resolve(devices);
        expect(DevicesService.getUnmanagedDevicesByTenant).toHaveBeenCalledWith($stateParams.tenantKey, null, null);
        return expect(controller.tenantDevices).toBe(data);
      });
    });

    describe('creating a new tenant', function () {
      beforeEach(function () {

      })


      it('editMode should be set to false', function () {
        $stateParams = {};
        controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
        return expect(controller.editMode).toBeFalsy();
      });

      it('do not call TenantsService.getTenantByKey', function () {
        $stateParams = {};
        controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
        return expect(TenantsService.getTenantByKey).not.toHaveBeenCalled();
      });

      return it('do not call Devices.getUnmanagedDevicesByTenant', function () {
        $stateParams = {};
        controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
        return expect(DevicesService.getUnmanagedDevicesByTenant).not.toHaveBeenCalled();
      });
    });

    describe('editItem', function () {
      controller = undefined;
      let tenantKey = 'bhjad897d987fa32fg708fg72';
      let item = {key: 'ahjad897d987fadafg708fg71', tenantKey: tenantKey};

      beforeEach(function () {
        spyOn($state, 'go');
        $stateParams = {tenantKey};
        serviceInjection = {
          $scope: scope,
          $stateParams
        };
        return controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
      });

      return it("route to the 'editDevice' named route, passing the supplied device key", function () {
        controller.editItem(item);
        return expect($state.go).toHaveBeenCalledWith('editDevice', {
          deviceKey: item.key,
          tenantKey: tenantKey,
          fromDevices: false
        });
      });
    });
    
    describe('.prepareForEditItem', function () {
      let resourceSearch = "test";

      beforeEach(function () {
        spyOn($state, 'go');

        controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
        controller.macDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
        controller.tenantKey = controller.macDevices.test.tenantKey
        return controller.serialDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
      });


      it("prepares for editItem as mac", function () {
        controller.selectedButton === "MAC";
        controller.prepareForEditView(resourceSearch);
        return expect($state.go).toHaveBeenCalledWith('editDevice', {
          deviceKey: controller.macDevices[resourceSearch].key,
          tenantKey: controller.tenantKey,
          fromDevices: false
        });
      });

      return it("prepares for editItem as serial", function () {
        controller.selectedButton === "Serial Number";
        controller.prepareForEditView(resourceSearch);
        return expect($state.go).toHaveBeenCalledWith('editDevice', {
          deviceKey: controller.serialDevices[resourceSearch].key,
          tenantKey: controller.tenantKey,
          fromDevices: false
        });
      });
    });

    return describe('.isResourceValid', function () {
      let resource = 'my-resource';

      beforeEach(function () {
        let tenantKey = 'bhjad897d987fa32fg708fg72';
        $stateParams = {tenantKey};
        serviceInjection = {
          $scope: scope,
          $stateParams
        };
        controller = $controller('TenantUnmanagedDevicesCtrl', serviceInjection);
        promise = new skykitProvisioning.q.Mock();
        spyOn(DevicesService, 'matchDevicesByFullMacByTenant').and.returnValue(promise);
        return spyOn(DevicesService, 'matchDevicesByFullSerialByTenant').and.returnValue(promise);
      });

      it("matchDevicesByFullMac called when managed and button is mac", function () {
        controller.selectedButton = "MAC";
        controller.isResourceValid(resource);
        promise.resolve(false);
        return expect(DevicesService.matchDevicesByFullMacByTenant).toHaveBeenCalledWith(controller.tenantKey, resource, true);
      });

      return it("matchDevicesByFullSerial called button is not mac", function () {
        controller.selectedButton = "Serial Number";
        controller.isResourceValid(resource);
        promise.resolve(false);
        return expect(DevicesService.matchDevicesByFullSerialByTenant).toHaveBeenCalledWith(controller.tenantKey, resource, true);
      });
    });
  });

  describe('search and pagination ', function () {
    let genericMatches;
    beforeEach(inject(function ($q) {
      spyOn($state, 'go');
      let tenantKey = 'bhjad897d987fa32fg708fg72';
      $stateParams = {tenantKey};
      serviceInjection = {
        $scope: scope,
        $stateParams,
        DevicesService: DevicesService
      };

      partial = "some text";
      promise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'searchDevices').and.callFake(function (someData) {
        genericMatches = {
          "matches": [
            {"serial": "1234"},
            {"serial": "45566"}
          ]
        };
        let deferred = $q.defer();
        deferred.resolve({
          "success": true,
          "devices": genericMatches
        })
        return deferred.promise
      })
      spyOn(DevicesService, 'executeSearchingPartialSerialByTenant')
      spyOn(DevicesService, 'getUnmanagedDevicesByTenant').and.callThrough();

      spyOn(DevicesService, 'executeSearchingPartialMacByTenant')
      return controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
    }));

    it("returns every serial name when called as a managed serial", function () {
      controller.selectedButton = "Serial Number";
      controller.searchDevices(partial)
        .then(() => expect(controller.serialDevices).toEqual(genericMatches))
    });

    it("returns every serial name when called as a managed mac", function () {
      controller.selectedButton = "MAC";
      controller.searchDevices(partial)
        .then(() => expect(controller.macDevices).toEqual(genericMatches))
    });

    it('resets variables whenever function is called', function () {
      controller.changeRadio();
      expect(controller.searchText).toEqual('');
      expect(controller.disabled).toEqual(true);
      expect(controller.serialDevices).toEqual({});
      return expect(controller.macDevices).toEqual({});
    });

    it('paginates forward', function () {
      controller.paginateCall(true);
      return expect(DevicesService.getUnmanagedDevicesByTenant).toHaveBeenCalledWith(controller.tenantKey, null, controller.devicesNext);
    });

    it('paginates backward', function () {
      controller.paginateCall(false);
      return expect(DevicesService.getUnmanagedDevicesByTenant).toHaveBeenCalledWith(controller.tenantKey, controller.devicesPrev, null);
    });
  })

});


