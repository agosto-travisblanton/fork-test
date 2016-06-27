describe('ProofOfPlayCtrl', function() {
  let $controller = undefined;
  let controller = undefined;
  let ProofPlayService = undefined;
  let promise = undefined;
  let $stateParams = undefined;
  let $state = undefined;
  let ToastsService = undefined;


  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function(_$controller_, _ProofPlayService_, _$state_, _ToastsService_) {
    $controller = _$controller_;
    ProofPlayService = _ProofPlayService_;
    $state = _$state_;
    ToastsService = _ToastsService_;

    return controller = $controller('ProofOfPlayCtrl', {
      ProofPlayService,
      $stateParams,
      $state,
      ToastsService
    });
  }));

  describe('at the start', () =>
    it('tab dict values should equal', function() {
      let resource = {
        title: 'Resource Report',

      };
      return expect(angular.equals(resource, controller.resource)).toBeTruthy();
    })
  );

  return describe('Service functionality', function() {
    beforeEach(function() {
      promise = new skykitProvisioning.q.Mock();
      return spyOn(ProofPlayService, 'getAllTenants').and.returnValue(promise);
    });

    it('sets inner tenants from Proofplay Service', function() {
      controller.initialize();
      let output = {
        data: {
          tenants: ["one_tenant"]
        }
      };
      promise.resolve(output);
      return expect(controller.tenants).toEqual(output.data.tenants);
    });


    return it('sets tenant', function() {
      controller.submitTenant('some_tenant');
      return expect(angular.equals(controller.chosen_tenant, 'some_tenant')).toBeTruthy();
    });
  });
});
