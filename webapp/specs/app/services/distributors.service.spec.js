describe('DistributorsService', function() {
  let DistributorsService = undefined;
  let Restangular = undefined;
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function(_DistributorsService_, _Restangular_) {
    DistributorsService = _DistributorsService_;
    Restangular = _Restangular_;
    return promise = new skykitProvisioning.q.Mock();
  }));

  describe('service initialization', () =>
    it('the current distributor is undefined', () => expect(DistributorsService.currentDistributor).toBeUndefined())
  );

  describe('.save', function() {
    describe('existing distributor', function() {
      let distributor = undefined;
      let result = undefined;

      beforeEach(function() {
        distributor = {
          key: 'kdfalkdsjfakjdf98ad87fa87df0',
          put() {}
        };
        spyOn(distributor, 'put').and.returnValue(promise);
        return result = DistributorsService.save(distributor);
      });

      it('calls put() on existing distributor', () => expect(distributor.put).toHaveBeenCalled());

      return it('returns a promise', () => expect(result).toBe(promise));
    });

    return describe('new distributor', function() {
      let distributor = undefined;
      let result = undefined;
      let distributorRestangularService = undefined;

      beforeEach(function() {
        distributor = {
          key: undefined
        };
        distributorRestangularService = {post(distributor) {}};
        spyOn(Restangular, 'service').and.returnValue(distributorRestangularService);
        spyOn(distributorRestangularService, 'post').and.returnValue(promise);
        return result = DistributorsService.save(distributor);
      });

      it('obtains Restangular service for distributors', () => expect(Restangular.service).toHaveBeenCalledWith(DistributorsService.DISTRIBUTOR_SERVICE));

      it('calls post(distributor) on Restangular service for distributors', () => expect(distributorRestangularService.post).toHaveBeenCalledWith(distributor));

      return it('returns a promise', () => expect(result).toBe(promise));
    });
  });

  describe('.fetchAll', function() {
    let distributorRestangularService = undefined;
    let result = undefined;

    beforeEach(function() {
      distributorRestangularService = {getList() {}};
      spyOn(Restangular, 'all').and.returnValue(distributorRestangularService);
      spyOn(distributorRestangularService, 'getList').and.returnValue(promise);
      return result = DistributorsService.fetchAll();
    });

    it('obtains Restangular service for distributors', () => expect(Restangular.all).toHaveBeenCalledWith(DistributorsService.DISTRIBUTOR_SERVICE));

    it('obtains a list of distributors from the Restangular service', () => expect(distributorRestangularService.getList).toHaveBeenCalled());

    return it('returns a promise', () => expect(result).toBe(promise));
  });

  describe('.getByKey', function() {
    let distributorRestangularService = undefined;
    let result = undefined;
    let distributorKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';

    beforeEach(function() {
      distributorRestangularService = {get() {}};
      spyOn(Restangular, 'oneUrl').and.returnValue(distributorRestangularService);
      spyOn(distributorRestangularService, 'get').and.returnValue(promise);
      return result = DistributorsService.getByKey(distributorKey);
    });

    it('obtains Restangular service for distributors', () => expect(Restangular.oneUrl).toHaveBeenCalledWith(DistributorsService.DISTRIBUTOR_SERVICE, `api/v1/distributors/${distributorKey}`));

    it('obtains the distributor from the Restangular service', () => expect(distributorRestangularService.get).toHaveBeenCalled());

    return it('returns a promise', () => expect(result).toBe(promise));
  });

  describe('.delete', function() {
    let distributorRestangularService = undefined;
    let result = undefined;
    let distributor = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'Foobar'};

    beforeEach(function() {
      distributorRestangularService = {remove() {}};
      spyOn(Restangular, 'one').and.returnValue(distributorRestangularService);
      spyOn(distributorRestangularService, 'remove').and.returnValue(promise);
      return result = DistributorsService.delete(distributor);
    });

    it('obtains Restangular service for the particular distributor', () => expect(Restangular.one).toHaveBeenCalledWith(DistributorsService.DISTRIBUTOR_SERVICE, distributor.key));

    it('removes the distributor via the Restangular service', () => expect(distributorRestangularService.remove).toHaveBeenCalled());

    return it('returns a promise', () => expect(result).toBe(promise));
  });

  describe('.getByName', function() {
    let distributorRestangularService = undefined;
    let result = undefined;

    beforeEach(function() {
      distributorRestangularService = {getList() {}};
      spyOn(Restangular, 'all').and.returnValue(distributorRestangularService);
      spyOn(distributorRestangularService, 'getList').and.returnValue(promise);
      return result = DistributorsService.getByName('Tierney Brothers');
    });

    it('obtains Restangular service for distributors', () => expect(Restangular.all).toHaveBeenCalledWith(DistributorsService.DISTRIBUTOR_SERVICE));

    it('calls getList with name as query parameter', () => expect(distributorRestangularService.getList).toHaveBeenCalledWith({distributorName: 'Tierney Brothers'}));

    return it('returns a promise', () => expect(result).toBe(promise));
  });

  return describe('.getDomainsByKey', function() {
    let distributorRestangularService = undefined;
    let result = undefined;
    let distributorKey = 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67';

    beforeEach(function() {
      distributorRestangularService = {get() {}};
      spyOn(Restangular, 'oneUrl').and.returnValue(distributorRestangularService);
      spyOn(distributorRestangularService, 'get').and.returnValue(promise);
      return result = DistributorsService.getDomainsByKey(distributorKey);
    });

    it('obtains Restangular service for distributor domains', () => expect(Restangular.oneUrl).toHaveBeenCalledWith(DistributorsService.DISTRIBUTOR_SERVICE, `api/v1/distributors/${distributorKey}/domains`));

    it('obtains the distributor domains from the Restangular service', () => expect(distributorRestangularService.get).toHaveBeenCalled());

    return it('returns a promise', () => expect(result).toBe(promise));
  });
});
