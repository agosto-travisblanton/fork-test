describe('DevicesService', function () {
  let DevicesService = undefined;
  let Restangular = undefined;
  let $http = undefined;
  let promise = undefined;
  let CacheFactory = undefined;
  let $q = undefined;
  let deferred = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_DevicesService_, _Restangular_, _CacheFactory_, _$http_, _$q_) {
    DevicesService = _DevicesService_;
    Restangular = _Restangular_;
    CacheFactory = _CacheFactory_;
    $http = _$http_;
    $q = _$q_;
    return promise = new skykitProvisioning.q.Mock();
  }));

  beforeEach(function () {
    DevicesService.deviceCache = {
      get() {
      },

      put() {
      }

    };
    DevicesService.deviceByTenantCache = {
      get() {
      },

      put() {
      }

    };
    return deferred = $q.defer();
  });

  describe('.getDevicesByTenant', () =>
    it('retrieve all devices associated to a tenant, returning a promise', function () {
      deferred.resolve(promise);
      let restangularServiceStub = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(restangularServiceStub);
      spyOn(restangularServiceStub, 'get').and.returnValue(promise);
      let tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud';
      let actual = DevicesService.getDevicesByTenant(tenantKey, null, null);
      return actual.then(() => {
        expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `/api/v1/tenants/null/null/${tenantKey}/devices?unmanaged=false`);
        return expect(actual).toBe(promise);
      });
    })
  );

  describe('.getUnmanagedDevicesByTenant', () =>
    it('retrieve all unmanaged devices associated to a tenant, returning a promise', function () {
      deferred.resolve(promise);
      let restangularServiceStub = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(restangularServiceStub);
      spyOn(restangularServiceStub, 'get').and.returnValue(promise);
      let tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud';
      let actual = DevicesService.getUnmanagedDevicesByTenant(tenantKey, null, null);
      return actual.then(() => {
        expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `/api/v1/tenants/null/null/${tenantKey}/devices?unmanaged=true`);
        return expect(actual).toBe(promise);
      });
    })
  );

  describe('.getDevicesByDistributor', () =>
    it('retrieve all devices associated with a distributor, returning a promise', function () {
      deferred.resolve(promise);
      let restangularServiceStub = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(restangularServiceStub);
      spyOn(restangularServiceStub, 'get').and.returnValue(promise);
      let distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud';
      let actual = DevicesService.getDevicesByDistributor(distributorKey, null, null);
      return actual.then(() => {
        expect(Restangular.oneUrl).toHaveBeenCalledWith('devices',
          `/api/v1/distributors/null/null/${distributorKey}/devices?unmanaged=false`);
        return expect(actual).toBe(promise);
      });
    })
  );

  describe('.getUnmanagedDevicesByDistributor', () =>
    it('retrieve all unmanaged devices associated with a distributor, returning a promise', function () {
      deferred.resolve(promise);
      let restangularServiceStub = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(restangularServiceStub);
      spyOn(restangularServiceStub, 'get').and.returnValue(promise);
      let distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFud';
      let actual = DevicesService.getUnmanagedDevicesByDistributor(distributorKey, null, null);
      return actual.then(() => {
        expect(Restangular.oneUrl).toHaveBeenCalledWith('devices',
          `/api/v1/distributors/null/null/${distributorKey}/devices?unmanaged=true`);
        return expect(actual).toBe(promise);
      });
    })
  );

  describe('.getDeviceByKey', () =>
    it('retrieve device associated with supplied key, returning a promise', function () {
      let deviceKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIRVGVuYW50RW50aXR5R3JvdXAiEXRlbmFudEVudGl0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw';
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.getDeviceByKey(deviceKey);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${deviceKey}`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.getDevices', () =>
    it('retrieve all devices, returning a promise', function () {
      let deviceRestangularService = {
        getList() {
        }
      };
      spyOn(Restangular, 'all').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'getList').and.returnValue(promise);
      let actual = DevicesService.getDevices();
      expect(Restangular.all).toHaveBeenCalledWith('devices');
      let parameters = {};
      expect(deviceRestangularService.getList).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.getIssuesByKey', () =>
    it('retrieve issues associated with supplied key, returning a promise', function () {
      let now = new Date();
      let epochEnd = moment(now).unix();
      now.setDate(now.getDate() - 1);
      let epochStart = moment(now).unix();
      expect(epochEnd).toBeGreaterThan(epochStart);
      let deviceKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.getIssuesByKey(deviceKey, epochStart, epochEnd);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices',
        `/api/v1/devices/null/null/${deviceKey}/issues?start=${epochStart}&end=${epochEnd}`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.getCommandEventsByKey', () =>
    it('retrieve command events associated with supplied key, returning a promise', function () {
      let deviceKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.getCommandEventsByKey(deviceKey);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `/api/v1/player-command-events/null/null/${deviceKey}`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );


  describe('.searchDevicesByPartialMac', () =>
    it('search devices with a partial mac address returns an http promise', function () {
      let distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.searchDevicesByPartialMac(distributorKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/distributors/search/mac/${distributorKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.searchDevicesByPartialSerial', () =>
    it('search devices with a partial mac address returns an http promise', function () {
      let distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.searchDevicesByPartialSerial(distributorKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/distributors/search/serial/${distributorKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.matchDevicesByFullMac', () =>
    it('match devices with a full mac address returns an http promise', function () {
      let distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.matchDevicesByFullMac(distributorKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/distributors/match/mac/${distributorKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.matchDevicesByFullSerial', () =>
    it('match devices with a full mac address returns an http promise', function () {
      let distributorKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.matchDevicesByFullSerial(distributorKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/distributors/match/serial/${distributorKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );


  describe('.searchDevicesByPartialMacByTenant', () =>
    it('search devices with a partial mac address returns an http promise', function () {
      let tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.searchDevicesByPartialMacByTenant(tenantKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/tenants/search/mac/${tenantKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.searchDevicesByPartialSerialByTenant', () =>
    it('search devices with a partial mac address returns an http promise', function () {
      let tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.searchDevicesByPartialSerialByTenant(tenantKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/tenants/search/serial/${tenantKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.matchDevicesByFullMacByTenant', () =>
    it('match devices with a full mac address returns an http promise', function () {
      let tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.matchDevicesByFullMacByTenant(tenantKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/tenants/match/mac/${tenantKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  return describe('.matchDevicesByFullSerialByTenant', () =>
    it('match devices with a full mac address returns an http promise', function () {
      let tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHI7CxIsSBlRlbmFudBiAgICAgMCvCgw';
      let partialMac = "1234";
      let unmanaged = false;
      let deviceRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(deviceRestangularService);
      spyOn(deviceRestangularService, 'get').and.returnValue(promise);
      let actual = DevicesService.matchDevicesByFullSerialByTenant(tenantKey, partialMac, unmanaged);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/tenants/match/serial/${tenantKey}/${partialMac}/${unmanaged}/devices`);
      expect(deviceRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );
});
