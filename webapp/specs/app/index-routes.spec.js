describe('skykitProvisioning module and configuration', function () {
    let $rootScope = undefined;
    let $state = undefined;
    let $injector = undefined;
    let RestangularProvider = undefined;

    beforeEach(function () {
        module("restangular", function (_RestangularProvider_) {
            RestangularProvider = _RestangularProvider_;
            spyOn(RestangularProvider, 'setBaseUrl').and.callThrough();
            spyOn(RestangularProvider, 'addRequestInterceptor').and.callThrough();
            spyOn(RestangularProvider, 'addResponseInterceptor').and.callThrough();
            return spyOn(RestangularProvider, 'setRestangularFields').and.callThrough();
        });

        module('skykitProvisioning');

        return inject(function (_$rootScope_, _$state_, _$injector_, $templateCache) {
            $rootScope = _$rootScope_;
            $state = _$state_;
            $injector = _$injector_;
            // We need add the template entry into the templateCache if we ever specify a templateUrl
            return $templateCache.put('template.html', '');
        });
    });


    describe('URL resolution', function () {
        it('should resolve \'home\' state', () => expect($state.href('home', {})).toEqual('#/'));

        it('should resolve \'proof\' state', () => expect($state.href('proof', {})).toEqual('#/proof'));

        it('should resolve \'domains\' state', () => expect($state.href('domains', {})).toEqual('#/domains'));

        it('should resolve \'addDomain\' state', () => expect($state.href('addDomain', {})).toEqual('#/domains/add'));

        it('should resolve \'editDomain\' state', function () {
            let domainKey = 'deree0re9reuewqerer';
            return expect($state.href('editDomain', {domainKey})).toEqual(`#/domains/${domainKey}`);
        });

        it('should resolve \'devices\' state', () => expect($state.href('devices', {})).toEqual('#/devices'));

        it('should resolve \'tenants\' state', () => expect($state.href('tenants', {})).toEqual('#/tenants'));

        it('should resolve \'addTenant\' state', () => expect($state.href('addTenant', {})).toEqual('#/tenants/add'));

        it('should resolve \'tenantDetails\' state', function () {
            let tenantKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6';
            return expect($state.href('tenantDetails', {tenantKey})).toEqual(`#/tenants/${tenantKey}/details`);
        });

        return it('should resolve \'editDevice\' state', function () {
            let deviceKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6';
            return expect($state.href('editDevice', {deviceKey})).toEqual(`#/devices/${deviceKey}`);
        });
    });

    describe('breadcrumbs', function () {
        describe('labels', function () {
            it('should resolve \'home\' state', () => expect($state.get('home').ncyBreadcrumb.label).toBe('Skykit Provisioning'));

            it('should resolve \'welcome\' state', () => expect($state.get('welcome').ncyBreadcrumb.label).toBe('Skykit Provisioning'));

            it('should resolve \'domains\' state', () => expect($state.get('domains').ncyBreadcrumb.label).toBe('Domains'));

            it('should resolve \'addDomain\' state', () => expect($state.get('addDomain').ncyBreadcrumb.label).toBe('Add domain'));

            it('should resolve \'editDomain\' state', () => expect($state.get('editDomain').ncyBreadcrumb.label).toBe('{{ domainDetailsCtrl.currentDomain.name }}'));

            it('should resolve \'tenants\' state', () => expect($state.get('tenants').ncyBreadcrumb.label).toBe('Tenants'));

            it('should resolve \'addTenant\' state', () => expect($state.get('addTenant').ncyBreadcrumb.label).toBe('Add tenant'));

            it('should resolve \'tenantDetails\' state', () => expect($state.get('tenantDetails').ncyBreadcrumb.label).toBe('{{ tenantDetailsCtrl.currentTenant.name }}'));

            it('should resolve \'tenantManagedDevices\' state', function () {
                expect($state.get('tenantManagedDevices').ncyBreadcrumb.label).toBe;
                return '{{ tenantManagedDevicesCtrl.currentTenant.name }}';
            });

            it('should resolve \'tenantUnmanagedDevices\' state', function () {
                expect($state.get('tenantUnmanagedDevices').ncyBreadcrumb.label).toBe;
                return '{{ tenantUnmanagedDevicesCtrl.currentTenant.name }}';
            });

            it('should resolve \'tenantLocations\' state', () => expect($state.get('tenantLocations').ncyBreadcrumb.label).toBe('{{ tenantLocationsCtrl.currentTenant.name }}'));

            it('should resolve \'addLocation\' state', () => expect($state.get('addLocation').ncyBreadcrumb.label).toBe('{{ tenantLocationCtrl.tenantName }}  / Location'));

            it('should resolve \'editLocation\' state', function () {
                expect($state.get('editLocation').ncyBreadcrumb.label).toBe;
                return '{{ tenantLocationCtrl.tenantName }}  / {{ tenantLocationCtrl.locationName }}';
            });

            it('should resolve \'devices\' state', () => expect($state.get('devices').ncyBreadcrumb.label).toBe('Devices'));

            it('should resolve \'editDevice\' state', () => expect($state.get('editDevice').ncyBreadcrumb.label).toBe('{{ deviceDetailsCtrl.currentDevice.key }}'));

            return it('should resolve \'proof\' state', () => expect($state.get('proof').ncyBreadcrumb.label).toBe('Proof of Play'));
        });

        return describe('parents', function () {
            it('should resolve \'addTenant\' state', () => expect($state.get('addTenant').ncyBreadcrumb.parent).toBe('tenants'));

            it('should resolve \'tenantDetails\' state', () => expect($state.get('tenantDetails').ncyBreadcrumb.parent).toBe('tenants'));

            it('should resolve \'tenantManagedDevices\' state', () => expect($state.get('tenantManagedDevices').ncyBreadcrumb.parent).toBe('tenants'));

            it('should resolve \'tenantUnmanagedDevices\' state', () => expect($state.get('tenantUnmanagedDevices').ncyBreadcrumb.parent).toBe('tenants'));

            it('should resolve \'tenantLocations\' state', () => expect($state.get('tenantLocations').ncyBreadcrumb.parent).toBe('tenants'));

            it('should resolve \'editLocation\' state', () => expect($state.get('editLocation').ncyBreadcrumb.parent).toBe('tenants'));

            it('should resolve \'editDevice\' state', () => expect($state.get('editDevice').ncyBreadcrumb.parent).toBe('devices'));


            it('should resolve \'addLocation\' state', () => expect($state.get('addLocation').ncyBreadcrumb.parent).toBe('tenants'));

            it('should resolve \'addDomain\' state', () => expect($state.get('addDomain').ncyBreadcrumb.parent).toBe('domains'));

            return it('should resolve \'editDomain\' state', () => expect($state.get('editDomain').ncyBreadcrumb.parent).toBe('domains'));
        });
    });


    return describe('Restangular configuration', function () {
        it('sets the base URL', () => expect(RestangularProvider.setBaseUrl).toHaveBeenCalledWith('/api/v1'));

        it('adds a response interceptor', function () {
            expect(RestangularProvider.addResponseInterceptor).toHaveBeenCalled();
            let args = RestangularProvider.addResponseInterceptor.calls.argsFor(0);
            return expect(args[0] instanceof Function).toBeTruthy();
        });

        return it('sets the Restangular fields mapping', function () {
            let restangularFieldsMapping = {id: 'key'};
            return expect(RestangularProvider.setRestangularFields).toHaveBeenCalledWith(restangularFieldsMapping);
        });
    });
});
