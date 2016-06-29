(function () {


    let appModule = angular.module('skykitProvisioning');
    appModule.controller("ProofOfPlayMultiResourceCtrl", function (ProofPlayService, $stateParams, $state, ToastsService) {
        let vm = this;
        vm.radioButtonChoices = {
            group1: 'By Device',
            group2: 'By Date',
            selection: null
        };


        vm.dateTimeSelection = {
            start: null,
            end: null
        };

        vm.formValidity = {
            start_date: false,
            end_date: false,
            resources: false,
        };

        vm.tenant = $stateParams.tenant;
        vm.no_cache = true;
        vm.loading = true;
        vm.disabled = true;
        vm.disabledTenant = true;
        vm.selected_resources = [];

        vm.initialize = () =>
            ProofPlayService.getAllResources(vm.tenant)
                .then(function (data) {
                    vm.loading = false;
                    vm.full_resource_map = data.data.resources;
                    vm.resources = [];
                    for (let i = 0; i < data.data.resources.length; i++) {
                        let resource = data.data.resources[i];
                        vm.resources.push(resource.resource_name);
                    }

                    if (vm.resources.length > 0) {
                        return vm.had_some_items = true;
                    } else {
                        return vm.had_some_items = false;
                    }
                })
        ;

        vm.refreshResources = function () {
            vm.searchText = '';
            vm.selectedItem = '';
            vm.loading = true;
            vm.disabled = true;
            vm.selected_resources = [];
            ProofPlayService.proofplayCache.removeAll();
            return vm.initialize();
        };

        vm.addToSelectedResources = function (searchText) {
            if (vm.isResourceValid(searchText)) {
                vm.selected_resources.push(searchText);
                let index = vm.resources.indexOf(searchText);
                vm.resources.splice(index, 1);
                vm.searchText = '';
            }
            vm.areResourcesValid();
            return vm.isDisabled();
        };

        vm.querySearch = (resources, searchText) => ProofPlayService.querySearch(resources, searchText);


        vm.isRadioValid = function (selection) {
            vm.formValidity.type = selection;
            return vm.isDisabled();
        };


        vm.isResourceValid = function (searchText) {
            if (__in__(searchText, vm.resources)) {
                if (!__in__(searchText, vm.selected_resources)) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        };


        vm.areResourcesValid = function () {
            vm.formValidity.resources = (vm.selected_resources.length > 0);
            return vm.isDisabled();
        };

        vm.isStartDateValid = function (start_date) {
            vm.formValidity.start_date = (start_date instanceof Date);
            return vm.isDisabled();
        };


        vm.isEndDateValid = function (end_date) {
            vm.formValidity.end_date = (end_date instanceof Date);
            return vm.isDisabled();
        };

        vm.removeFromSelectedResource = function (item) {
            let index = vm.selected_resources.indexOf(item);
            vm.selected_resources.splice(index, 1);
            vm.resources.push(item);
            vm.areResourcesValid();
            return vm.isDisabled();
        };


        vm.isDisabled = function () {
            if (vm.formValidity.start_date && vm.formValidity.end_date && vm.formValidity.resources && vm.formValidity.type) {
                vm.disabled = false;
                return vm.final = {
                    start_date_unix: moment(vm.dateTimeSelection.start).unix(),
                    end_date_unix: moment(vm.dateTimeSelection.end).unix(),
                    resources: vm.selected_resources,
                    type: vm.radioButtonChoices.selection
                };

            } else {
                return vm.disabled = true;
            }
        };

        vm.submit = function () {
            let resources_as_ids = [];
            for (let i = 0; i < vm.final.resources.length; i++) {
                let item = vm.final.resources[i];
                for (let j = 0; j < vm.full_resource_map.length; j++) {
                    let each = vm.full_resource_map[j];
                    if (each["resource_name"] === item) {
                        resources_as_ids.push(each["resource_identifier"]);
                    }
                }
            }

            if (vm.final.type === "1") {
                return ProofPlayService.downloadCSVForMultipleResourcesByDevice(vm.final.start_date_unix, vm.final.end_date_unix, resources_as_ids, vm.tenant);

            } else {
                return ProofPlayService.downloadCSVForMultipleResourcesByDate(vm.final.start_date_unix, vm.final.end_date_unix, resources_as_ids, vm.tenant);
            }
        };

        vm.tenants = null;
        vm.currentTenant = vm.tenant;

        vm.initialize_tenant_select = () =>
            ProofPlayService.getAllTenants()
                .then(data => vm.tenants = data.data.tenants)
        ;

        vm.querySearch = (resources, searchText) => ProofPlayService.querySearch(resources, searchText);

        vm.isSelectionValid = function (search) {
            if (__in__(search, vm.tenants)) {
                return vm.disabledTenant = false;
            } else {
                return vm.disabledTenant = true;
            }
        };


        vm.submitTenant = function (tenant) {
            if (tenant !== vm.currentTenant) {
                $state.go('proofDetail', {
                    tenant
                });
                return ToastsService.showSuccessToast(`Proof of Play reporting set to ${tenant}`);
            } else {
                return ToastsService.showErrorToast(`Proof of Play reporting is already set to ${tenant}`);
            }
        };


        return vm;
    });

    function __in__(needle, haystack) {
        return haystack.indexOf(needle) >= 0;
    }
})
();