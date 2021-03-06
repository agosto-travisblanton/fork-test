import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject


describe('DistributorsCtrl', function () {
  var $controller, $state, DistributorsService, controller, promise;
  $controller = void 0;
  controller = void 0;
  $state = void 0;
  DistributorsService = void 0;
  promise = void 0;
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
  return describe('.initialize', function () {
    var distributors;
    return distributors = [];
  });
});

// ---
// generated by coffee-script 1.9.2
