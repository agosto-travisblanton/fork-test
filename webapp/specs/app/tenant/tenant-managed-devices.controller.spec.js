describe('TenantManagedDevicesCtrl', function () {
  let scope = undefined;
  let $controller = undefined;
  let $state = undefined;
  let $stateParams = undefined;
  let TenantsService = undefined;
  let DevicesService = undefined;
  let serviceInjection = undefined;
  let tenantsServicePromise = undefined;
  let devicesServicePromise = undefined;
  let controller = undefined;
  let promise = undefined;
  let ProgressBarService = undefined;
  let partial = undefined;
  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _TenantsService_, _DevicesService_, _ProgressBarService_, _$state_, _$rootScope_) {
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
      return spyOn(DevicesService, 'getDevicesByTenant').and.returnValue(devicesServicePromise);
    });

    it('currentTenant should be set', function () {
      controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
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
      controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
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
        return serviceInjection = {
          $scope: scope,
          $stateParams,
          ProgressBarService: progressBarService
        };
      });

      it('editMode should be set to true', function () {
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        return expect(controller.editMode).toBeTruthy();
      });

      it('retrieve tenant by key from TenantsService', function () {
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        let tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'};
        tenantsServicePromise.resolve(tenant);
        expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey);
        return expect(controller.currentTenant).toBe(tenant);
      });

      return it('retrieve tenant\'s devices by tenant key from DevicesService', function () {
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        let data = [1, 2, 3];
        let devices = {"devices": data};
        devicesServicePromise.resolve(devices);
        expect(DevicesService.getDevicesByTenant).toHaveBeenCalledWith($stateParams.tenantKey, null, null);
        return expect(controller.tenantDevices).toBe(data);
      });
    });

    describe('creating a new tenant', function () {
      it('editMode should be set to false', function () {
        $stateParams = {};
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        return expect(controller.editMode).toBeFalsy();
      });

      it('do not call TenantsService.getTenantByKey', function () {
        $stateParams = {};
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        return expect(TenantsService.getTenantByKey).not.toHaveBeenCalled();
      });

      return it('do not call Devices.getDevicesByTenant', function () {
        $stateParams = {};
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        return expect(DevicesService.getDevicesByTenant).not.toHaveBeenCalled();
      });
    });

    describe('editItem', function () {
      controller = undefined;
      let tenantKey = 'bhjad897d987fa32fg708fg72';
      let item = {key: 'ahjad897d987fadafg708fg71'};

      beforeEach(function () {
        spyOn($state, 'go');
        $stateParams = {tenantKey};
        serviceInjection = {
          $scope: scope,
          $stateParams
        };
        return controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
      });

      return it("route to the 'editDevice' named route, passing the supplied device key", function () {
        controller.editItem(item);
        return expect($state.go).toHaveBeenCalledWith('editDevice', {
          deviceKey: item.key,
          tenantKey,
          fromDevices: false
        });
      });
    });

    describe('search and pagination ', function () {
      beforeEach(function () {
        spyOn($state, 'go');
        let tenantKey = 'bhjad897d987fa32fg708fg72';
        $stateParams = {tenantKey};
        serviceInjection = {
          $scope: scope,
          $stateParams
        };

        partial = "some text";
        promise = new skykitProvisioning.q.Mock();
        spyOn(DevicesService, 'searchDevicesByPartialMacByTenant').and.returnValue(promise);
        spyOn(DevicesService, 'searchDevicesByPartialSerialByTenant').and.returnValue(promise);
        return controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
      });

      let convertArrayToDictionary = function (theArray, mac) {
        let Devices = {};
        for (let i = 0; i < theArray.length; i++) {
          let item = theArray[i];
          if (mac) {
            Devices[item.mac] = item;
          } else {
            Devices[item.serial] = item;
          }
        }

        return Devices;
      };


      it("returns every serial name when called as an managed serial", function () {
        controller.selectedButton = "Serial Number";
        controller.searchDevices(partial);
        let serial_matches = {
          "matches": [
            {"serial": "1234"},
            {"serial": "45566"}
          ]
        };
        promise.resolve(serial_matches);
        return expect(controller.serialDevices).toEqual(convertArrayToDictionary(serial_matches["matches"], false));
      });

      it("returns every serial name when called as an managed mac", function () {
        controller.selectedButton = "MAC";
        controller.searchDevices(partial);
        let mac_matches = {
          "matches": [
            {"mac": "1234"},
            {"mac": "45566"}
          ]
        };
        promise.resolve(mac_matches);
        return expect(controller.macDevices).toEqual(convertArrayToDictionary(mac_matches["matches"], true));
      });

      it('resets variables whenever function is called', function () {
        controller.changeRadio();
        expect(controller.searchText).toEqual('');
        expect(controller.disabled).toEqual(true);
        expect(controller.serialDevices).toEqual({});
        return expect(controller.macDevices).toEqual({});
      });

      it('paginates forward with managed', function () {
        controller.paginateCall(true);
        return expect(DevicesService.getDevicesByTenant).toHaveBeenCalledWith(controller.tenantKey, null, controller.devicesNext);
      });

      return it('paginates backward with managed', function () {
        controller.paginateCall(false);
        return expect(DevicesService.getDevicesByTenant).toHaveBeenCalledWith(controller.tenantKey, controller.devicesPrev, null);
      });
    });


    describe('.prepareForEditItem', function () {
      let resourceSearch = "test";

      beforeEach(function () {
        spyOn($state, 'go');
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        controller.macDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
        return controller.serialDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
      });


      it("prepares for editItem as managed mac", function () {
        controller.selectedButton === "MAC";
        controller.prepareForEditView(resourceSearch);
        return expect($state.go).toHaveBeenCalledWith('editDevice', {
          deviceKey: controller.macDevices[resourceSearch].key,
          tenantKey: controller.tenantKey,
          fromDevices: false
        });
      });

      return it("prepares for editItem as managed serial", function () {
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
        controller = $controller('TenantManagedDevicesCtrl', serviceInjection);
        promise = new skykitProvisioning.q.Mock();
        spyOn(DevicesService, 'matchDevicesByFullMacByTenant').and.returnValue(promise);
        return spyOn(DevicesService, 'matchDevicesByFullSerialByTenant').and.returnValue(promise);
      });

      it("matchDevicesByFullMac called when managed and button is mac", function () {
        controller.selectedButton = "MAC";
        controller.isResourceValid(resource);
        promise.resolve(false);
        return expect(DevicesService.matchDevicesByFullMacByTenant).toHaveBeenCalledWith(controller.tenantKey, resource, false);
      });

      return it("matchDevicesByFullSerial called when managed and button is not mac", function () {
        controller.selectedButton = "Serial Number";
        controller.isResourceValid(resource);
        promise.resolve(false);
        return expect(DevicesService.matchDevicesByFullSerialByTenant).toHaveBeenCalledWith(controller.tenantKey, resource, false);
      });
    });
  });
});
