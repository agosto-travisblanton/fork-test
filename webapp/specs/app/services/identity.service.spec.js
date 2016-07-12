describe('IdentityService', function () {
  let IdentityService = undefined;
  let Restangular = undefined;
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_IdentityService_, _Restangular_) {
    IdentityService = _IdentityService_;
    Restangular = _Restangular_;
    return promise = new skykitProvisioning.q.Mock();
  }));

  return describe('.getIdentity', function () {
    let identityRestangularService = undefined;
    let result = undefined;

    beforeEach(function () {
      identityRestangularService = {
        get() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(identityRestangularService);
      spyOn(identityRestangularService, 'get').and.returnValue(promise);
      return result = IdentityService.getIdentity();
    });

    it('obtains Restangular service for identity', () => expect(Restangular.oneUrl).toHaveBeenCalledWith('identity'));

    it('obtains the identity from the Restangular service', () => expect(identityRestangularService.get).toHaveBeenCalled());

    return it('returns a promise', () => expect(result).toBe(promise));
  });
});

