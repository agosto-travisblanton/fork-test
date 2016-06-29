(function () {


    let appModule = angular.module('skykitProvisioning');

    appModule.controller("ProofOfPlayCtrl", function (ProofPlayService, $stateParams, $state, ToastsService) {
        let vm = this;
        vm.resource = {title: "Resource Report"};
        vm.location = {title: "Location Report"};
        vm.display = {title: "Display Report"};

        vm.chosen_tenant = null;
        vm.tenants = null;
        vm.disabled = true;


        vm.initialize = () =>
            ProofPlayService.getAllTenants()
                .then(data => vm.tenants = data.data.tenants)
        ;

        vm.querySearch = (resources, searchText) => ProofPlayService.querySearch(resources, searchText);


        vm.isSelectionValid = function (search) {
            if (__in__(search, vm.tenants)) {
                return vm.disabled = false;
            } else {
                return vm.disabled = true;
            }
        };


        vm.submitTenant = function (tenant) {
            if (tenant) {
                vm.chosen_tenant = (tenant);
                return $state.go('proofDetail', {
                    tenant: vm.chosen_tenant
                });
            }
        };

        vm.refreshTenants = function () {
            vm.tenants = null;
            let url = ProofPlayService.makeHTTPURL("/retrieve_my_tenants", '');
            ProofPlayService.proofplayCache.remove(url);
            return vm.initialize();
        };


        return vm;
    });

    function __in__(needle, haystack) {
        return haystack.indexOf(needle) >= 0;
    }
})
();