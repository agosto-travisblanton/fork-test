angular.module('skykitProvisioning').factory('TenantsService', (Restangular, CacheFactory, SessionsService) =>
    new class TenantsService {

        constructor() {
            if (!CacheFactory.get('tenantCache')) {
                this.tenantCache = CacheFactory('tenantCache', {
                        maxAge: 60 * 60 * 1000,
                        deleteOnExpire: 'aggressive',
                        storageMode: 'localStorage',
                        onExpire: (key, value) => {
                            $http.get(key).success(data => {
                                this.tenantCache.put(key, data);
                                return;
                            });
                            return;
                        }
                    }
                );
            }
        }


        save(tenant) {
            if (tenant.key !== undefined) {
                var promise = tenant.put();
            } else {
                var promise = Restangular.service('tenants').post(tenant);
            }
            return promise;
        }

        fetchAllTenants() {
            let promise = Restangular.all('tenants').getList();
            return promise;
        }

        fetchAllTenantsPaginated(page_size, offset) {
            let url = `api/v1/tenants/paginated/${page_size}/${offset}`;
            let promise = Restangular.oneUrl('tenants', url).get();
            return promise;
        }

        getTenantByKey(tenantKey) {
            let url = `api/v1/tenants/${tenantKey}`;
            let promise = Restangular.oneUrl('tenants', url).get();
            return promise;
        }

        delete(tenant) {
            if (tenant.key !== undefined) {
                let promise = Restangular.one("tenants", tenant.key).remove();
                return promise;
            }
        }
    }()
);


