describe('AuthorizationService', function () {
  beforeEach(module('skykitProvisioning'));
  let SessionsService = undefined;
  let AuthorizationService = undefined;
  let $q = undefined;
  let promise = undefined;

  beforeEach(inject(function (_SessionsService_, _$q_, _AuthorizationService_) {
    SessionsService = _SessionsService_;
    $q = _$q_;
    return AuthorizationService = _AuthorizationService_;
  }));

  describe('AuthorizationService as Admin User', function () {
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(SessionsService, 'getUserKey').and.returnValue(true);
      spyOn(SessionsService, 'getDistributorsAsAdmin').and.returnValue(true);
      return spyOn(SessionsService, 'getIsAdmin').and.returnValue(true);
    });

    it('.authenticated resolves', function () {
      let toResolve = AuthorizationService.authenticated();
      return toResolve.then(data => expect(data).toEqual(true));
    });

    it('.notAuthenticated rejects', function () {
      let toResolve = AuthorizationService.notAuthenticated();
      return toResolve.then(data => expect(data).toEqual(["authError", 'home']));
    });

    return it('.notAuthenticated resolves', function () {
      let toResolve = AuthorizationService.isAdminOrDistributorAdmin();
      return toResolve.then(data => expect(data).toEqual(true));
    });
  });

  describe('AuthorizationService as logged out', function () {
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(SessionsService, 'getUserKey').and.returnValue(false);
      spyOn(SessionsService, 'getDistributorsAsAdmin').and.returnValue(false);
      return spyOn(SessionsService, 'getIsAdmin').and.returnValue(false);
    });

    it('.authenticated resolves', function () {
      let toResolve = AuthorizationService.authenticated();
      return toResolve.then(data => expect(data).toEqual(["authError", 'sign_in']));
    });

    it('.notAuthenticated rejects', function () {
      let toResolve = AuthorizationService.notAuthenticated();
      return toResolve.then(data => expect(data).toEqual(true));
    });

    return it('.notAuthenticated resolves', function () {
      let toResolve = AuthorizationService.isAdminOrDistributorAdmin();
      return toResolve.then(data => expect(data).toEqual(["authError", 'sign_in']));
    });
  });

  return describe('AuthorizationService as DistributorAdmin User', function () {
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(SessionsService, 'getUserKey').and.returnValue(true);
      spyOn(SessionsService, 'getDistributorsAsAdmin').and.returnValue(["one"]);
      return spyOn(SessionsService, 'getIsAdmin').and.returnValue(false);
    });

    it('.authenticated resolves', function () {
      let toResolve = AuthorizationService.authenticated();
      return toResolve.then(data => expect(data).toEqual(true));
    });

    it('.notAuthenticated rejects', function () {
      let toResolve = AuthorizationService.notAuthenticated();
      return toResolve.then(data => expect(data).toEqual(["authError", 'home']));
    });

    return it('.notAuthenticated resolves', function () {
      let toResolve = AuthorizationService.isAdminOrDistributorAdmin();
      return toResolve.then(data => expect(data).toEqual(true));
    });
  });
});
