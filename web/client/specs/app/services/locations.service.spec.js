describe('LocationsService', function () {
  let LocationsService = undefined;
  let Restangular = undefined;
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_LocationsService_, _Restangular_) {
    LocationsService = _LocationsService_;
    Restangular = _Restangular_;
    return promise = new skykitProvisioning.q.Mock();
  }));

  describe('.save', function () {
    it('updates an existing location, returning a promise', function () {
      let location = {
        key: 'kdfalkdsjfakjdf98ad87fa87df0',
        put() {
        }
      };
      spyOn(location, 'put').and.returnValue(promise);
      let actual = LocationsService.save(location);
      expect(location.put).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    });

    return it('inserts a new location, returning a promise', function () {
      let location = {customerLocationName: 'Back of the store'};
      let locationRestangularService = {
        post(location) {
        }
      };
      spyOn(Restangular, 'service').and.returnValue(locationRestangularService);
      spyOn(locationRestangularService, 'post').and.returnValue(promise);
      let actual = LocationsService.save(location);
      expect(Restangular.service).toHaveBeenCalledWith('locations');
      expect(locationRestangularService.post).toHaveBeenCalledWith(location);
      return expect(actual).toBe(promise);
    });
  });

  describe('.getLocationsByTenantKey', function () {
    it('retrieve locations by tenant key, returning a promise', function () {
      let tenantKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';
      let locationRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(locationRestangularService);
      spyOn(locationRestangularService, 'get').and.returnValue(promise);
      let actual = LocationsService.getLocationsByTenantKey(tenantKey);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('tenants', `api/v1/tenants/${tenantKey}/locations`);
      expect(locationRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    });


    describe('.getLocationsByTenantKeyPaginated', function () {
    });
    return it('retrieve locations by tenant key, returning a promise', function () {
      let tenantKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';
      let locationRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(locationRestangularService);
      spyOn(locationRestangularService, 'get').and.returnValue(promise);
      let actual = LocationsService.getLocationsByTenantKeyPaginated(tenantKey);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('tenants', `api/v1/tenants/${tenantKey}/null/null/locations`);
      expect(locationRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    });
  });

  return describe('.getLocationByKey', () =>
    it('retrieve location by location key, returning a promise', function () {
      let locationKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';
      let locationRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(locationRestangularService);
      spyOn(locationRestangularService, 'get').and.returnValue(promise);
      let actual = LocationsService.getLocationByKey(locationKey);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('locations', `api/v1/locations/${locationKey}`);
      expect(locationRestangularService.get).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );
});
