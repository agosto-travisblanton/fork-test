(function () {


    let appModule = angular.module('skykitProvisioning');

    appModule.controller('TenantManagedDevicesCtrl', function ($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) {
        let vm = this;
        vm.currentTenant = {
            key: undefined,
            name: undefined,
            tenant_code: undefined,
            admin_email: undefined,
            content_server_url: undefined,
            content_manager_base_url: undefined,
            domain_key: undefined,
            notification_emails: undefined,
            proof_of_play_logging: false,
            active: true
        };
        vm.tenantDevices = [];
        vm.devicesPrev = null;
        vm.devicesNext = null;
        vm.selectedButton = "Serial Number";
        vm.serialDevices = {};
        vm.disabled = true;
        vm.macDevices = {};
        vm.editMode = !!$stateParams.tenantKey;
        vm.tenantKey = $stateParams.tenantKey;

        vm.getManagedDevices = function (tenantKey, prev_cursor, next_cursor) {
            ProgressBarService.start();
            let devicesPromise = DevicesService.getDevicesByTenant(tenantKey, prev_cursor, next_cursor);
            return devicesPromise.then(function (data) {
                vm.devicesPrev = data["prev_cursor"];
                vm.devicesNext = data["next_cursor"];
                vm.tenantDevices = data["devices"];
                return ProgressBarService.complete();
            });
        };


        vm.refreshDevices = function () {
            vm.devicesPrev = null;
            vm.devicesNext = null;
            vm.tenantDevices = null;
            DevicesService.deviceByTenantCache.removeAll();
            return vm.getManagedDevices(vm.tenantKey, vm.devicesPrev, vm.devicesNext);
        };

        if (vm.editMode) {
            let tenantPromise = TenantsService.getTenantByKey(vm.tenantKey);
            tenantPromise.then(tenant => vm.currentTenant = tenant);

            vm.getManagedDevices(vm.tenantKey, null, null);
        }

        $scope.tabIndex = 1;

        $scope.$watch('tabIndex', function (toTab, fromTab) {
            if (toTab !== undefined) {
                switch (toTab) {
                    case 0:
                        return $state.go('tenantDetails', {tenantKey: vm.tenantKey});
                    case 1:
                        return $state.go('tenantManagedDevices', {tenantKey: vm.tenantKey});
                    case 2:
                        return $state.go('tenantUnmanagedDevices', {tenantKey: vm.tenantKey});
                    case 3:
                        return $state.go('tenantLocations', {tenantKey: vm.tenantKey});
                }
            }
        });

        vm.editItem = item => $state.go('editDevice', {
            deviceKey: item.key,
            tenantKey: vm.tenantKey,
            fromDevices: false
        });


        vm.convertArrayToDictionary = function (theArray, mac) {
            let Devices = {};
            for (let i = 0; i < theArray.length; i++) {
                let item = theArray[i];
                if (mac) {
                    Devices[item.mac] = item;
                } else {
                    Devices[item.serial] = item;
                }
            }
            return Devices;
        };

        vm.changeRadio = function () {
            vm.searchText = '';
            vm.disabled = true;
            vm.serialDevices = {};
            return vm.macDevices = {};
        };


        vm.searchDevices = function (partial_search) {
            if (partial_search) {
                if (partial_search.length > 2) {
                    if (vm.selectedButton === "Serial Number") {
                        return DevicesService.searchDevicesByPartialSerialByTenant(vm.tenantKey, partial_search, false)
                            .then(function (res) {
                                let result = res["serial_number_matches"];
                                vm.serialDevices = vm.convertArrayToDictionary(result, false);
                                let deviceSerials = [];
                                for (let i = 0; i < result.length; i++) {
                                    let each = result[i];
                                    deviceSerials.push(each.serial);
                                }
                                return deviceSerials;
                            });

                    } else {
                        return DevicesService.searchDevicesByPartialMacByTenant(vm.tenantKey, partial_search, false)
                            .then(function (res) {
                                let result = res["mac_matches"];
                                vm.macDevices = vm.convertArrayToDictionary(result, true);
                                let deviceMacs = [];
                                for (let i = 0; i < result.length; i++) {
                                    let each = result[i];
                                    deviceMacs.push(each.mac);
                                }
                                return deviceMacs;
                            });
                    }

                } else {
                    return [];
                }
            } else {
                return [];
            }
        };

        vm.paginateCall = function (forward) {
            if (forward) {
                return vm.getManagedDevices(vm.tenantKey, null, vm.devicesNext);

            } else {
                return vm.getManagedDevices(vm.tenantKey, vm.devicesPrev, null);
            }
        };


        vm.prepareForEditView = function (searchText) {
            let mac = vm.selectedButton === "MAC";
            if (mac) {
                return vm.editItem(vm.macDevices[searchText]);
            } else {
                return vm.editItem(vm.serialDevices[searchText]);
            }
        };


        vm.controlOpenButton = function (isMatch) {
            vm.disabled = !isMatch;
            return vm.loadingDisabled = false;
        };


        vm.isResourceValid = function (resource) {
            if (resource) {
                if (resource.length > 2) {
                    let mac = vm.selectedButton === "MAC";
                    vm.loadingDisabled = true;

                    if (mac) {
                        return DevicesService.matchDevicesByFullMacByTenant(vm.tenantKey, resource, false)
                            .then(res => vm.controlOpenButton(res["is_match"]));

                    } else {
                        return DevicesService.matchDevicesByFullSerialByTenant(vm.tenantKey, resource, false)
                            .then(res => vm.controlOpenButton(res["is_match"]));
                    }

                } else {
                    return vm.controlOpenButton(false);
                }

            } else {
                return vm.controlOpenButton(false);
            }
        };

        return vm;
    });
})
();