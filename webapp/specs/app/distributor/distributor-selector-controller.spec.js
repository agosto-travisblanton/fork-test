'use strict';
describe('DistributorSelectorCtrl', function() {
  var $controller, $log, $rootScope, $scope, $state, DevicesService, DistributorsService, ProofPlayService, SessionsService, StorageService, TenantsService, ToastsService, controller, promise;
  $controller = void 0;
  controller = void 0;
  $state = void 0;
  promise = void 0;
  $rootScope = void 0;
  StorageService = void 0;
  $scope = void 0;
  $log = void 0;
  ToastsService = void 0;
  SessionsService = void 0;
  DistributorsService = void 0;
  DevicesService = void 0;
  ProofPlayService = void 0;
  TenantsService = void 0;
  beforeEach(module('skykitProvisioning'));
  beforeEach(inject(function(_$controller_, _$state_, _StorageService_, _$rootScope_, _$log_, _DistributorsService_, _SessionsService_, _ToastsService_, _DevicesService_, _ProofPlayService_, _TenantsService_) {
    $controller = _$controller_;
    $state = _$state_;
    StorageService = _StorageService_;
    $rootScope = _$rootScope_;
    $scope = _$rootScope_.$new();
    ToastsService = _ToastsService_;
    $log = _$log_;
    DistributorsService = _DistributorsService_;
    SessionsService = _SessionsService_;
    DevicesService = _DevicesService_;
    ProofPlayService = _ProofPlayService_;
    TenantsService = _TenantsService_;
    return controller = $controller('DistributorSelectorCtrl', {
      $scope: $scope,
      StorageService: _StorageService_,
      $log: $log,
      $state: $state,
      ToastsService: ToastsService,
      DistributorsService: DistributorsService,
      SessionsService: SessionsService,
      DevicesService: DevicesService,
      ProofPlayService: ProofPlayService,
      TenantsService: TenantsService
    });
  }));
  describe('initialization', function() {
    it('distributors should be an empty array', function() {
      return expect(angular.isArray(controller.distributors)).toBeTruthy();
    });
    return it('currentDistributor should be undefined', function() {
      return expect(controller.currentDistributor).toBeUndefined();
    });
  });
  describe('.initialize', function() {
    var expectedCurrentUserKey;
    promise = void 0;
    expectedCurrentUserKey = '32748092734827340';
    beforeEach(function() {
      promise = new skykitProvisioning.q.Mock();
      SessionsService.setUserKey(expectedCurrentUserKey);
      spyOn(DistributorsService, 'fetchAllByUser').and.callFake(function(currentUserKey) {
        return promise;
      });
      spyOn(controller, 'selectDistributor');
      DevicesService.deviceCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      DevicesService.deviceByTenantCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      ProofPlayService.proofplayCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      TenantsService.tenantCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      return controller.initialize();
    });
    describe('when distributors array is not a length of 1', function() {
      var distributors;
      distributors = [
        {
          key: 'dsifuyadfya7a8sdf678a6dsf9',
          name: ''
        }, {
          key: 'dsifuyadfya7a8sdf678a6dff7',
          name: ''
        }
      ];
      it('invokes DistributorsService.fetchAllByUser', function() {
        return expect(DistributorsService.fetchAllByUser).toHaveBeenCalledWith(expectedCurrentUserKey);
      });
      it('sets distributors on the controller with the result from the promise', function() {
        promise.resolve(distributors);
        return expect(controller.distributors).toEqual(distributors);
      });
      return it('does not call selectDistributor()', function() {
        promise.resolve(distributors);
        return expect(controller.selectDistributor).not.toHaveBeenCalled();
      });
    });
    return describe('when distributors array is a length of 1', function() {
      var distributors;
      distributors = [
        {
          key: 'dsifuyadfya7a8sdf678a6dsf9',
          name: ''
        }
      ];
      it('invokes DistributorsService.fetchAllByUser', function() {
        return expect(DistributorsService.fetchAllByUser).toHaveBeenCalledWith(expectedCurrentUserKey);
      });
      it('sets distributors on the controller with the result from the promise', function() {
        promise.resolve(distributors);
        return expect(controller.distributors).toEqual(distributors);
      });
      return it('calls selectDistributor() to select the only distributor returned from the backend', function() {
        promise.resolve(distributors);
        return expect(controller.selectDistributor).toHaveBeenCalledWith(distributors[0]);
      });
    });
  });
  return describe('.selectDistributor', function() {
    var distributor;
    distributor = {
      key: 'd78f9a0d89f7a0876ga7f6ga786g5a78df57d6f5a6dsf',
      name: 'some_distro'
    };
    beforeEach(function() {
      DevicesService.deviceCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      DevicesService.deviceByTenantCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      ProofPlayService.proofplayCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      TenantsService.tenantCache = {
        get: function() {},
        put: function() {},
        removeAll: function() {}
      };
      spyOn($state, 'go');
      spyOn(ToastsService, 'showErrorToast');
      spyOn(DistributorsService, 'switchDistributor');
      spyOn(ToastsService, 'showSuccessToast');
      return controller.selectDistributor(distributor);
    });
    return it('sets the currentDistributor property', function() {
      return expect(DistributorsService.switchDistributor).toHaveBeenCalledWith(distributor);
    });
  });
});

// ---
// generated by coffee-script 1.9.2