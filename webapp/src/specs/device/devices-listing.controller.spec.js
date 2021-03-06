import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('DevicesListingCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let $stateParams = undefined;
  let $state = undefined;
  let DevicesService = undefined;
  let promise = undefined;
  let unmanagedPromise = undefined;
  let ProgressBarService = undefined;
  let serialPromise = undefined;
  let sweet = undefined;
  let gcmidPromise = undefined;

  let to_respond_with_devices = {
    devices: [
      {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'},
      {key: 'dhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'},
      {key: 'dhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]
  };
  let to_respond_with_unmanagedDevices = {
    unmanagedDevices: [
      {key: 'uhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'},
      {key: 'uhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'},
      {key: 'uhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]
  };

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _DevicesService_, _$stateParams_, _$state_, _ProgressBarService_, _sweet_) {
    $controller = _$controller_;
    $stateParams = _$stateParams_;
    DevicesService = _DevicesService_;
    $state = _$state_;
    ProgressBarService = _ProgressBarService_;
    return sweet = _sweet_;
  }));

  describe('initialization', function () {
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      unmanagedPromise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'getDevicesByDistributor').and.returnValue(promise);
      spyOn(DevicesService, 'getUnmanagedDevicesByDistributor').and.returnValue(unmanagedPromise);
      spyOn(ProgressBarService, 'start');
      spyOn(ProgressBarService, 'complete');
      controller = $controller('DevicesListingCtrl', {});
      return controller.distributorKey = 'some-key';
    });

    it('devices should be an array', () => expect(angular.isArray(controller.devices)).toBeTruthy());

    it('unmanagedDevices should be an array', () => expect(angular.isArray(controller.unmanagedDevices)).toBeTruthy());

    it('calls DevicesService.getDevicesByDistributor to retrieve all distributor devices', function () {
      controller.initialize();
      return expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith(controller.distributorKey, controller.devicesPrev, controller.devicesNext);
    });

    it('starts the progress bar', function () {
      controller.initialize();
      promise.resolve(to_respond_with_devices);
      unmanagedPromise.resolve(to_respond_with_unmanagedDevices);
      expect(controller.devices).toBe(to_respond_with_devices.devices);
      expect(controller.unmanagedDevices).toBe(to_respond_with_unmanagedDevices.devices);
      return expect(ProgressBarService.start).toHaveBeenCalled();
    });

    return it('calls DevicesService.getUnmanagedDevicesByDistributor to retrieve all distributor unmanaged devices', function () {
      controller.initialize();
      return expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith(controller.distributorKey, controller.unmanagedDevicesPrev, controller.unmanagedDevicesNext);
    });
  });

  describe('.getFetchSuccess', function () {
    beforeEach(function () {
      spyOn(ProgressBarService, 'complete');
      return controller = $controller('DevicesListingCtrl', {});
    });

    return it('stops the progress bar', function () {
      controller.getFetchSuccess();
      return expect(ProgressBarService.complete).toHaveBeenCalled();
    });
  });

  describe('.getFetchFailure', function () {
    let response = {status: 400, statusText: 'Bad request'};
    beforeEach(function () {
      spyOn(ProgressBarService, 'complete');
      spyOn(sweet, 'show');
      return controller = $controller('DevicesListingCtrl', {});
    });

    it('stops the progress bar', function () {
      controller.getFetchFailure(response);
      return expect(ProgressBarService.complete).toHaveBeenCalled();
    });

    return it('calls seet alert with error', function () {
      controller.getFetchFailure(response);
      return expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to fetch devices. Error: 400 Bad request.', 'error');
    });
  });

  describe('.editItem', function () {
    let item = {key: 'ahjad897d987fadafg708fg71', tenantKey: 'ahjad897d987fadafg708fg71', fromDevices: true};

    beforeEach(function () {
      spyOn($state, 'go');
      return controller = $controller('DevicesListingCtrl', {});
    });

    return it("route to the 'editDevice' named route, passing the supplied device key", function () {
      controller.editItem(item);
      return expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: item.key,
        tenantKey: item.tenantKey,
        fromDevices: true
      });
    });
  });

  describe('.paginateCall', function () {
    beforeEach(function () {
      spyOn($state, 'go');
      promise = new skykitProvisioning.q.Mock();
      unmanagedPromise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'getDevicesByDistributor').and.returnValue(promise);
      spyOn(DevicesService, 'getUnmanagedDevicesByDistributor').and.returnValue(unmanagedPromise);
      spyOn(ProgressBarService, 'start');
      spyOn(ProgressBarService, 'complete');
      controller = $controller('DevicesListingCtrl', {});
      controller.devicesPrev = '1';
      controller.devicesNext = '2';
      controller.unmanagedDevicesPrev = '3';
      controller.unmanagedDevicesNext = '4';
      return controller.distributorKey = 'some-key';
    });

    it("paginated forward with unmanaged", function () {
      controller.paginateCall(true, false);
      return expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith(controller.distributorKey, null, controller.unmanagedDevicesNext);
    });

    it('paginates forward with managed', function () {
      controller.paginateCall(true, true);
      return expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith(controller.distributorKey, null, controller.devicesNext);
    });


    it("paginated backward with unmanaged", function () {
      controller.paginateCall(false, false);
      return expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith(controller.distributorKey, controller.unmanagedDevicesPrev, null);
    });

    return it('paginates backward with managed', function () {
      controller.paginateCall(false, true);
      return expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith(controller.distributorKey, controller.devicesPrev, null);
    });
  });

  describe('.search bar related functions', function () {
    beforeEach(() => controller = $controller('DevicesListingCtrl', {}));

    it('resets variables whenever function is called with unmanaged', function () {
      let unmanaged = true;
      controller.changeRadio(unmanaged);

      expect(controller.unmanagedSearchText).toEqual('');
      expect(controller.unmanagedDisabled).toEqual(true);
      expect(controller.unmanagedSerialDevices).toEqual({});
      return expect(controller.unmanagedMacDevices).toEqual({});
    });

    it('resets variables whenever function is called with managed', function () {
      let unmanaged = false;
      controller.changeRadio(unmanaged);

      expect(controller.searchText).toEqual('');
      expect(controller.disabled).toEqual(true);
      expect(controller.serialDevices).toEqual({});
      return expect(controller.macDevices).toEqual({});
    });


    it('converts array to dictionary with serial as key', function () {
      let theArray = [{"serial": "test", "a": "b"}];
      let isMac = false;
      let result = DevicesService.convertDevicesArrayToDictionaryObj(theArray, isMac);
      return expect(result).toEqual({"test": {"a": "b", "serial": "test"}});
    });


    it('converts array to dictionary with mac key', function () {
      let theArray = [{"mac": "test", "a": "b"}];
      let isMac = true;
      let result = DevicesService.convertDevicesArrayToDictionaryObj(theArray, isMac);
      return expect(result).toEqual({"test": {"a": "b", "mac": "test"}});
    });

    return it('converts array to dictionary with gcmid key', function () {
      let theArray = [{"gcmid": "test", "a": "b"}];
      let isMac = false;
      let isGCMid = true
      let result = DevicesService.convertDevicesArrayToDictionaryObj(theArray, isMac, isGCMid);
      return expect(result).toEqual({"test": {"a": "b", "gcmid": "test"}});
    });
  });


  describe('.prepareForEditItem', function () {
    let resourceSearch = "test";

    beforeEach(function () {
      spyOn($state, 'go');
      controller = $controller('DevicesListingCtrl', {});
      controller.unmanagedMacDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
      controller.unmanagedSerialDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
      controller.macDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
      return controller.serialDevices = {"test": {"key": "1234", "tenantKey": "5678"}};
    });

    it("prepares for editItem as unmanaged mac", function () {
      controller.unmanagedSelectedButton === "MAC";
      let unmanaged = true;
      controller.prepareForEditView(unmanaged, resourceSearch);
      return expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.unmanagedMacDevices[resourceSearch].key,
        tenantKey: controller.unmanagedMacDevices[resourceSearch].tenantKey,
        fromDevices: true
      });
    });

    it("prepares for editItem as unmanaged serial;", function () {
      controller.unmanagedSelectedButton === "Serial Number";
      let unmanaged = true;
      controller.prepareForEditView(unmanaged, resourceSearch);
      return expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.unmanagedMacDevices[resourceSearch].key,
        tenantKey: controller.unmanagedMacDevices[resourceSearch].tenantKey,
        fromDevices: true
      });
    });


    it("prepares for editItem as unmanaged gcmid", function () {
      controller.unmanagedSelectedButton === "GCM ID";
      let unmanaged = true;
      controller.prepareForEditView(unmanaged, resourceSearch);
      return expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.unmanagedMacDevices[resourceSearch].key,
        tenantKey: controller.unmanagedMacDevices[resourceSearch].tenantKey,
        fromDevices: true
      });
    });


    it("prepares for editItem as managed gcmid", function () {
      controller.selectedButton === "GCM ID";
      let unmanaged = false;
      controller.prepareForEditView(unmanaged, resourceSearch);
      return expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.macDevices[resourceSearch].key,
        tenantKey: controller.macDevices[resourceSearch].tenantKey,
        fromDevices: true
      });
    });


    it("prepares for editItem as managed mac", function () {
      controller.selectedButton === "MAC";
      let unmanaged = false;
      controller.prepareForEditView(unmanaged, resourceSearch);
      return expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.macDevices[resourceSearch].key,
        tenantKey: controller.macDevices[resourceSearch].tenantKey,
        fromDevices: true
      });
    });

    return it("prepares for editItem as managed serial", function () {
      controller.selectedButton === "Serial Number";
      let unmanaged = false;
      controller.prepareForEditView(unmanaged, resourceSearch);
      return expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.serialDevices[resourceSearch].key,
        tenantKey: controller.serialDevices[resourceSearch].tenantKey,
        fromDevices: true
      });
    });
  });

  describe('.controlOpenButton', function () {
    beforeEach(() => controller = $controller('DevicesListingCtrl', {}));

    it("unmanagedDisabled is false if unmanaged and a match", function () {
      let isMatch = true;
      let unmanaged = true;
      controller.controlOpenButton(unmanaged, isMatch);
      return expect(controller.unmanagedDisabled).toBeFalsy();
    });

    it("unmanagedDisabled is true if unmanaged and a not match", function () {
      let isMatch = false;
      let unmanaged = true;
      controller.controlOpenButton(unmanaged, isMatch);
      return expect(controller.unmanagedDisabled).toBeTruthy();
    });


    it("disabled is false if managed and a match", function () {
      let isMatch = true;
      let unmanaged = false;
      controller.controlOpenButton(unmanaged, isMatch);
      return expect(controller.disabled).toBeFalsy();
    });

    return it("disabled is true if managed and a match", function () {
      let isMatch = false;
      let unmanaged = false;
      controller.controlOpenButton(unmanaged, isMatch);
      return expect(controller.disabled).toBeTruthy();
    });
  });


  describe('.isResourceValid', function () {

    beforeEach(function () {
      controller = $controller('DevicesListingCtrl', {});
    });

    it('returns true when called resource is in vm.devicesToMatchOnManaged and managed', function () {
      controller.devicesToMatchOnManaged = ["one", "two"]
      expect(controller.isResourceValid(false, "one")).toBeTruthy()
    })

    it('returns false when called resource is not in vm.devicesToMatchOnManaged and managed', function () {
      controller.devicesToMatchOnManaged = ["one", "two"]
      expect(controller.isResourceValid(false, "blah")).toBeFalsy();
    })


    it('returns true when called resource is in vm.devicesToMatchOnUnmanaged and unmanaged', function () {
      controller.devicesToMatchOnUnmanaged = ["one", "two"]
      expect(controller.isResourceValid(true, "one")).toBeTruthy()
    })

    it('returns false when called resource is not in vm.devicesToMatchOnUnmanaged and unmanaged', function () {
      controller.devicesToMatchOnUnmanaged = ["one", "two"]
      expect(controller.isResourceValid(true, "blah")).toBeFalsy();
    })
  });

  return describe('.searchDevices', function () {
    let partial = "it doesn't matter dwight!";
    let genericMatches;


    beforeEach(inject(function ($q) {
      controller = $controller('DevicesListingCtrl', {});
      promise = new skykitProvisioning.q.Mock();
      serialPromise = new skykitProvisioning.q.Mock();
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
      return spyOn(DevicesService, 'searchDevicesByPartialSerial').and.returnValue(serialPromise);

    }));

    it("returns every serial name when called as an unmanaged serial", function () {
      let unmanaged = true;
      controller.unmanagedSelectedButton = "Serial Number";
      controller.searchDevices(unmanaged, partial)
        .then(function () {
          return expect(controller.unmanagedSerialDevices).toEqual(genericMatches);
        })
    });


    it("returns every serial name when called as an unmanaged mac", function () {
      let unmanaged = true;
      controller.unmanagedSelectedButton = "MAC";
      controller.searchDevices(unmanaged, partial)
        .then(function () {
          return expect(controller.unmanagedMacDevices).toEqual(genericMatches);
        })
    });


    it("returns every gcmid name when called as an unmanaged gcmid", function () {
      let unmanaged = true;
      controller.unmanagedSelectedButton = "GCM ID";
      controller.searchDevices(unmanaged, partial)
        .then(function () {
          return expect(controller.unmanagedSerialDevices).toEqual(genericMatches);
        })
    });

    it("returns every serial name when called as an managed serial", function () {
      let unmanaged = false;
      controller.selectedButton = "Serial Number";
      controller.searchDevices(unmanaged, partial)
        .then(function () {
          return expect(controller.serialDevices).toEqual(genericMatches);
        })
    });

    it("returns every mac name when called as an managed mac", function () {
      let unmanaged = false;
      controller.selectedButton = "MAC";

      controller.searchDevices(unmanaged, partial)
        .then(function () {
          return expect(controller.macDevices).toEqual(genericMatches);
        })
    });

    it("returns every gcmid name when called as an managed gcmid", function () {
      let unmanaged = false;
      controller.selectedButton = "GCM ID";

      controller.searchDevices(unmanaged, partial)
        .then(function () {
          return expect(controller.gcmidDevices).toEqual(genericMatches);
        })
    });
  });
});
