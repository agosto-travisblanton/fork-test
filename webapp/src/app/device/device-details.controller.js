(function () {

    let appModule = angular.module('skykitProvisioning');
    appModule.controller('DeviceDetailsCtrl', function ($log,
                                                        $stateParams,
                                                        $state,
                                                        SessionsService,
                                                        DevicesService,
                                                        LocationsService,
                                                        CommandsService,
                                                        TimezonesService,
                                                        sweet,
                                                        ProgressBarService,
                                                        $mdDialog,
                                                        ToastsService) {
        let vm = this;
        vm.tenantKey = $stateParams.tenantKey;
        vm.deviceKey = $stateParams.deviceKey;
        vm.fromDevices = $stateParams.fromDevices === "true";
        vm.currentDevice = {};

        vm.copyDeviceKey = () => ToastsService.showSuccessToast('Device key has been copied to your clipboard');

        vm.initialize = function () {
            let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
            return devicePromise.then((response => vm.onGetDeviceSuccess(response)), response => vm.onGetDeviceFailure(response));
        };


        vm.onGetDeviceSuccess = function (response) {
            vm.currentDevice = response;
            if (response.timezone !== vm.selectedTimezone) {
                vm.selectedTimezone = response.timezone;
            }
            if (vm.tenantKey === undefined) {
                vm.tenantKey = vm.currentDevice.tenantKey;
            }
            if ($stateParams.fromDevices === "true") {
                vm.backUrl = '/#/devices';
                return vm.backUrlText = 'Back to devices';
            } else {
                if (vm.currentDevice.isUnmanagedDevice === true) {
                    vm.backUrl = `/#/tenants/${vm.tenantKey}/unmanaged`;
                    return vm.backUrlText = 'Back to tenant unmanaged devices';
                } else {
                    vm.backUrl = `/#/tenants/${vm.tenantKey}/managed`;
                    return vm.backUrlText = 'Back to tenant managed devices';
                }
            }
        };

        vm.onGetDeviceFailure = function (response) {
            ToastsService.showErrorToast('Oops. We were unable to fetch the details for this device at this time.');
            let errorMessage = `No detail for device_key #${vm.deviceKey}. Error: ${response.status} ${response.statusText}`;
            $log.error(errorMessage);
            return $state.go('devices');
        };

        return vm;
    });
})
();