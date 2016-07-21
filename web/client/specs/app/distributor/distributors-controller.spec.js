import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('DistributorsCtrl', function () {
  var $controller, $state, DistributorsService, controller, promise;
  $controller = undefined;
  controller = undefined;
  $state = undefined;
  DistributorsService = undefined;
  promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _$state_) {
    $controller = _$controller_;
    $state = _$state_;
    return controller = $controller('DistributorsCtrl', {
      $state: $state
    });
  }));
  describe('initialization', function () {
    return it('distributors should be an empty array', function () {
      return expect(angular.isArray(controller.distributors)).toBeTruthy();
    });
  });
});
