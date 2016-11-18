export default class AdminService {
  constructor(Restangular) {
    'ngInject';
    this.Restangular = Restangular
    this.USER_SERVICE = "users";
    this.DISTRIBUTOR_SERVICE = "distributors";
  }

  makeDistributor(distributor, admin_email) {
    let payload = {
      distributor,
      admin_email
    };

    let promise = this.Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, '/internal/v1/distributors').customPOST(payload);
    return promise;
  }

  addUserToDistributor(userEmail, distributor, distributorAdmin) {
    let payload = {
      user_email: userEmail,
      distributor,
      distributor_admin: distributorAdmin
    };

    let promise = this.Restangular.oneUrl(this.USER_SERVICE, "/internal/v1/users").customPOST(payload);
    return promise;
  }

  getUsersOfDistributor(distributorKey) {
    let promise = this.Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, `/internal/v1/analytics/distributors/${distributorKey}/users`).get();
    return promise;
  }

  getAllDistributors() {
    let promise = this.Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, "/internal/v1/distributors").get();
    return promise;
  }
}


