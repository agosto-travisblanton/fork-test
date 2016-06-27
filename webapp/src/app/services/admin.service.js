angular.module('skykitProvisioning')
.factory('AdminService', Restangular =>
  new class AdminService {

    constructor() {
      this.USER_SERVICE = "users";
      this.DISTRIBUTOR_SERVICE = "distributors";
    }

    makeDistributor(distributor, admin_email) {
      let payload = {
        distributor,
        admin_email
      };

      let promise = Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, '/api/v1/distributors').customPOST(payload);
      return promise;
    }

    addUserToDistributor(userEmail, distributor, distributorAdmin) {
      let payload = {
        user_email: userEmail,
        distributor,
        distributor_admin: distributorAdmin
      };

      let promise = Restangular.oneUrl(this.USER_SERVICE, "/api/v1/users").customPOST(payload);
      return promise;
    }

    getUsersOfDistributor(distributorKey) {
      let promise = Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, `/api/v1/analytics/distributors/${distributorKey}/users`).get();
      return promise;
    }

    getAllDistributors() {
      let promise = Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, "/api/v1/distributors").get();
      return promise;
    }
  }()
);
    
      
      

