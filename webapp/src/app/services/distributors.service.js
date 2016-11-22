export default class DistributorsService {

  constructor(Restangular, $state, SessionsService) {
    'ngInject';
    this.Restangular = Restangular;
    this.$state = $state;
    this.SessionsService = SessionsService;
    this.DISTRIBUTOR_SERVICE = 'distributors';
  }

  save(tenant) {
    if (tenant.key !== undefined) {
      var promise = tenant.put();
    } else {
      var promise = this.Restangular.service(this.DISTRIBUTOR_SERVICE).post(tenant);
    }
    return promise;
  }

  fetchAll() {
    let promise = this.Restangular.all(this.DISTRIBUTOR_SERVICE).getList();
    return promise;
  }

  fetchAllByUser(userKey) {
    if (userKey) {
      let promise = this.Restangular.one('users', userKey).doGET(this.DISTRIBUTOR_SERVICE);
      return promise;
    }
  }

  getByKey(key) {
    let promise = this.Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, `internal/v1/distributors/${key}`).get();
    return promise;
  }

  delete(entity) {
    if (entity.key) {
      let promise = this.Restangular.one(this.DISTRIBUTOR_SERVICE, entity.key).remove();
      return promise;
    }
  }

  getByName(name) {
    let promise = this.Restangular.all(this.DISTRIBUTOR_SERVICE).getList({distributorName: name});
    return promise;
  }

  getDomainsByKey(key) {
    let promise = this.Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, `internal/v1/distributors/${key}/domains`).get();
    return promise;
  }

  switchDistributor(distributor) {
    this.SessionsService.setCurrentDistributorName(distributor.name);
    this.SessionsService.setCurrentDistributorKey(distributor.key);
    return this.$state.go('welcome');
  }
}
