
import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('AdminService', function () {
  beforeEach(module('skykitProvisioning'));
  let Restangular = undefined;
  let AdminService = undefined;
  let restangularService = undefined;

  beforeEach(inject(function (_AdminService_, _Restangular_) {
    Restangular = _Restangular_;
    return AdminService = _AdminService_;
  }));

  return describe('Restangular API', function () {
    beforeEach(function () {
      restangularService = {
        customPOST() {
        },

        get() {
        }
      };

      return spyOn(Restangular, 'oneUrl').and.returnValue(restangularService);
    });

    it('.makeDistributor', function () {
      AdminService.makeDistributor('distributor', 'admin@gmail.com');
      return expect(Restangular.oneUrl).toHaveBeenCalledWith(AdminService.DISTRIBUTOR_SERVICE, "/api/v1/distributors");
    });


    it('.addUserToDistributor', function () {
      AdminService.addUserToDistributor('admin@gmail.com', 'distributor', true);
      return expect(Restangular.oneUrl).toHaveBeenCalledWith(AdminService.USER_SERVICE, '/api/v1/users');
    });


    it('.getUsersOfDistributor', function () {
      let distributorKey = 'distributorKey';
      AdminService.getUsersOfDistributor(distributorKey);
      return expect(Restangular.oneUrl).toHaveBeenCalledWith(AdminService.DISTRIBUTOR_SERVICE, `/api/v1/analytics/distributors/${distributorKey}/users`);
    });

    return it('.getUsersOfDistributor', function () {
      AdminService.getAllDistributors();
      return expect(Restangular.oneUrl).toHaveBeenCalledWith(AdminService.DISTRIBUTOR_SERVICE, "/api/v1/distributors");
    });
  });
});
