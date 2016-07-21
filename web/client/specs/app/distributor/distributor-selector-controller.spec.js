import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject
import angular from 'angular';

import DistributorsServiceClass from './../../../app/services/distributors.service'
import SessionsServiceClass from './../../../app/services/sessions.service'
import ToastsServiceClass from './../../../app/services/toasts.service'
import DevicesServiceClass from './../../../app/services/devices.service'
import ProofPlayServiceClass from './../../../app/services/proofplay.service'
import TenantsServiceClass from './../../../app/services/tenants.service'
import StorageServiceClass from './../../../app/services/storage.service'


describe('DistributorSelectorCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let $state = undefined;
  let promise = undefined;
  let $rootScope = undefined;
  let StorageService = undefined;
  let $scope = undefined;
  let $log = undefined;
  let ToastsService = undefined;
  let SessionsService = undefined;
  let DistributorsService = undefined;
  let DevicesService = undefined;
  let ProofPlayService = undefined;
  let TenantsService = undefined;


  beforeEach(module('skykitProvisioning'));

  beforeEach(module(function ($provide) {
    $provide.service('StorageService', StorageServiceClass); //
    $provide.service('DistributorsService', DistributorsServiceClass); //
    $provide.service('SessionsService', SessionsService); //
    $provide.service('ToastsService', ToastsServiceClass); //
    $provide.service('DevicesService', DevicesServiceClass); //
    $provide.service('ProofPlayService', ProofPlayServiceClass); //
    $provide.service('TenantsService', TenantsServiceClass); //
  }));

  beforeEach(inject(function (_$controller_,
                              _$state_,
                              _$rootScope_,
                              _$log_,
                              _StorageService_,
                              _DistributorsService_,
                              _SessionsService_,
                              _ToastsService_,
                              _DevicesService_,
                              _ProofPlayService_,
                              _TenantsService_) {
    $controller = _$controller_;
    $state = _$state_;
    $rootScope = _$rootScope_;
    $scope = _$rootScope_.$new();
    $log = _$log_;

    ToastsService = _ToastsService_;
    StorageService = _StorageService_;
    DistributorsService = _DistributorsService_;
    SessionsService = _SessionsService_;
    DevicesService = _DevicesService_;
    ProofPlayService = _ProofPlayService_;
    TenantsService = _TenantsService_;

    controller = $controller('DistributorSelectorCtrl', {
      $scope: $scope,
      StorageService: StorageService,
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
  describe('initialization', function () {
    it('distributors should be an empty array', function () {
      console.log(controller)
      return expect(angular.isArray(controller.distributors)).toBeTruthy();
    });
    return it('currentDistributor should be undefined', function () {
      return expect(controller.currentDistributor).toBeUndefined();
    });
  });
  describe('.initialize', function () {
    var expectedCurrentUserKey;
    promise = undefined;
    expectedCurrentUserKey = '32748092734827340';
    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      SessionsService.setUserKey(expectedCurrentUserKey);
      spyOn(DistributorsService, 'fetchAllByUser').and.callFake(function (currentUserKey) {
        return promise;
      });
      spyOn(controller, 'selectDistributor');
      return controller.initialize();
    });
    describe('when distributors array is not a length of 1', function () {
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
      it('invokes DistributorsService.fetchAllByUser', function () {
        return expect(DistributorsService.fetchAllByUser).toHaveBeenCalledWith(expectedCurrentUserKey);
      });
      it('sets distributors on the controller with the result from the promise', function () {
        promise.resolve(distributors);
        return expect(controller.distributors).toEqual(distributors);
      });
      return it('does not call selectDistributor()', function () {
        promise.resolve(distributors);
        return expect(controller.selectDistributor).not.toHaveBeenCalled();
      });
    });
    return describe('when distributors array is a length of 1', function () {
      var distributors;
      distributors = [
        {
          key: 'dsifuyadfya7a8sdf678a6dsf9',
          name: ''
        }
      ];
      it('invokes DistributorsService.fetchAllByUser', function () {
        return expect(DistributorsService.fetchAllByUser).toHaveBeenCalledWith(expectedCurrentUserKey);
      });
      it('sets distributors on the controller with the result from the promise', function () {
        promise.resolve(distributors);
        return expect(controller.distributors).toEqual(distributors);
      });
      return it('calls selectDistributor() to select the only distributor returned from the backend', function () {
        promise.resolve(distributors);
        return expect(controller.selectDistributor).toHaveBeenCalledWith(distributors[0]);
      });
    });
  });
  return describe('.selectDistributor', function () {
    var distributor;
    distributor = {
      key: 'd78f9a0d89f7a0876ga7f6ga786g5a78df57d6f5a6dsf',
      name: 'some_distro'
    };
    beforeEach(function () {

      spyOn($state, 'go');
      spyOn(ToastsService, 'showErrorToast');
      spyOn(DistributorsService, 'switchDistributor');
      spyOn(ToastsService, 'showSuccessToast');
      controller.selectDistributor(distributor);
    });
    return it('sets the currentDistributor property', function () {
      return expect(DistributorsService.switchDistributor).toHaveBeenCalledWith(distributor);
    });
  });
});
