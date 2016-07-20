describe('DomainsCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let $state = undefined;
  let DomainsService = undefined;
  let sweet = undefined;
  let promise = undefined;


  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _DomainsService_, _$state_, _sweet_) {
    $controller = _$controller_;
    $state = _$state_;
    DomainsService = _DomainsService_;
    sweet = _sweet_;
    return controller = $controller('DomainsCtrl', {$state, DomainsService, sweet});
  }));

  describe('initialization', () =>
    it('domains should be an empty array', () => expect(angular.isArray(controller.domains)).toBeTruthy())
  );

  describe('.initialize', function () {
    let domains = [
      {
        key: 'ahjad897d987fadafg708fg71',
        name: 'bob.agosto.com',
        impersonation_admin_email_address: 'bob.macneal@skykit.com',
        created: '2015-09-08 12:15:08',
        updated: '2015-09-08 12:15:08'
      },
      {
        key: 'bhjad897d987fadafg708y672',
        name: 'chris.agosto.com',
        impersonation_admin_email_address: 'chris.bartling@skykit.com',
        created: '2015-09-08 12:15:09',
        updated: '2015-09-08 12:15:09'
      },
      {
        key: 'chjad897d987fadafg708hb53',
        name: 'paul.agosto.com',
        impersonation_admin_email_address: 'paul.lundberg@skykit.com',
        created: '2015-09-08 12:15:10',
        updated: '2015-09-08 12:15:10'
      }
    ];

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      return spyOn(DomainsService, 'fetchAllDomains').and.returnValue(promise);
    });

    it('call DomainsService.fetchAllDomains to retrieve all domains', function () {
      controller.initialize();
      promise.resolve(domains);
      return expect(DomainsService.fetchAllDomains).toHaveBeenCalled();
    });

    return it("the 'then' handler caches the retrieved domains in the controller", function () {
      controller.initialize();
      promise.resolve(domains);
      return expect(controller.domains).toBe(domains);
    });
  });

  describe('.editItem', function () {
    let domain = {key: 'ahjad897d987fadafg708fg71'};

    beforeEach(() => spyOn($state, 'go'));

    return it("route to the 'editDomain' named route, passing the supplied domain key", function () {
      controller.editItem(domain);
      return expect($state.go).toHaveBeenCalledWith('editDomain', {domainKey: domain.key});
    });
  });

  return describe('.deleteItem', function () {
    let domain = {
      key: 'ahjad897d987fadafg708fg71',
      name: 'bob.agosto.com',
      created: '2015-05-10 22:15:10',
      updated: '2015-05-10 22:15:10'
    };

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(DomainsService, 'delete').and.returnValue(promise);
      spyOn(controller, 'initialize');
      return spyOn(sweet, 'show').and.callFake((options, callback) => callback());
    });

    it('call DomainsService.delete domain', function () {
      controller.deleteItem(domain);
      promise.resolve();
      return expect(DomainsService.delete).toHaveBeenCalledWith(domain);
    });

    it("the 'then' handler calls initialize to re-fetch all domains", function () {
      controller.deleteItem(domain);
      promise.resolve();
      return expect(controller.initialize).toHaveBeenCalled;
    });

    return it("the SweetAlert confirmation should be shown", function () {
      controller.deleteItem(domain);
      promise.resolve();
      return expect(sweet.show).toHaveBeenCalled;
    });
  });
});

