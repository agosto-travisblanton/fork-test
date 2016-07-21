import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

import DistributorsServiceClass from './../../../app/services/distributors.service'
import SessionsServiceClass from './../../../app/services/sessions.service'

describe('DistributorSelectorCtrl', function () {
  let $controller = undefined;
  let $scope = undefined;
  let promise = undefined;
  let controller = undefined;
  let $state = undefined;
  let DistributorsService = undefined;
  let SessionsService = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(function () {
    return inject(function (_$controller_,
                            _$state_,
                            _DistributorsService_,
                            _SessionsService_) {
      $controller = _$controller_;
      $state = _$state_;
      DistributorsService = _DistributorsService_;
      SessionsService = _SessionsService_;

      controller = $controller('DistributorSelectorCtrl', {
        $state,
        DistributorsService,
        SessionsService,
      });

    })
  });

  describe('initialization', function () {
    it('distributors should be an empty array', function () {
      return expect(angular.isArray(controller.distributors)).toBeTruthy();
    });
    return it('currentDistributor should be undefined', function () {
      return expect(controller.currentDistributor).toBeUndefined();
    });
  });
  describe('.initialize', function () {
    let expectedCurrentUserKey = '32748092734827340';
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


      let distributors;
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

      let distributors = [
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
    let distributor = {
      key: 'd78f9a0d89f7a0876ga7f6ga786g5a78df57d6f5a6dsf',
      name: 'some_distro'
    };
    beforeEach(function () {
      controller = $controller('DistributorSelectorCtrl', {
        $state,
        DistributorsService,
        SessionsService,
      });
      spyOn($state, 'go');
      spyOn(DistributorsService, 'switchDistributor').and.callFake(function (distributor) {
        return true;
      });
    });
    it('sets the currentDistributor property', function () {
      controller.selectDistributor(distributor);
      return expect(DistributorsService.switchDistributor).toHaveBeenCalledWith(distributor);
    });
  });
});
