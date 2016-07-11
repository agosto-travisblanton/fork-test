angular.module('skykitProvisioning').factory('DistributorsService', (Restangular,
                                                                     $state,
                                                                     SessionsService,
                                                                     ProofPlayService,
                                                                     TenantsService,
                                                                     DevicesService) =>
    new class DistributorsService {
        constructor() {
            this.DISTRIBUTOR_SERVICE = 'distributors';
        }

        save(tenant) {
            if (tenant.key !== undefined) {
                var promise = tenant.put();
            } else {
                var promise = Restangular.service(this.DISTRIBUTOR_SERVICE).post(tenant);
            }
            return promise;
        }

        fetchAll() {
            let promise = Restangular.all(this.DISTRIBUTOR_SERVICE).getList();
            return promise;
        }

        fetchAllByUser(userKey) {
            if (userKey) {
                let promise = Restangular.one('users', userKey).doGET(this.DISTRIBUTOR_SERVICE);
                return promise;
            }
        }

        getByKey(key) {
            let promise = Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, `api/v1/distributors/${key}`).get();
            return promise;
        }

        delete(entity) {
            if (entity.key) {
                let promise = Restangular.one(this.DISTRIBUTOR_SERVICE, entity.key).remove();
                return promise;
            }
        }

        getByName(name) {
            let promise = Restangular.all(this.DISTRIBUTOR_SERVICE).getList({distributorName: name});
            return promise;
        }

        getDomainsByKey(key) {
            let promise = Restangular.oneUrl(this.DISTRIBUTOR_SERVICE, `api/v1/distributors/${key}/domains`).get();
            return promise;
        }

        switchDistributor(distributor) {
            ProofPlayService.proofplayCache.removeAll();
            TenantsService.tenantCache.removeAll();
            DevicesService.deviceCache.removeAll();
            DevicesService.deviceByTenantCache.removeAll();

            SessionsService.setCurrentDistributorName(distributor.name);
            SessionsService.setCurrentDistributorKey(distributor.key);

            return $state.go('welcome');
        }
    }()
);
