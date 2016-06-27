(function () {


    let appModule = angular.module('skykitProvisioning');
    appModule.controller('DeviceDetailsEnrollmentCtrl', function ($log,
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
                                                                  ToastsService,
                                                                  IntegrationEvents) {
        let vm = this;
        vm.tenantKey = $stateParams.tenantKey;
        vm.deviceKey = $stateParams.deviceKey;
        vm.fromDevices = $stateParams.fromDevices === "true";
        vm.currentDevice = {};
        vm.enrollmentEvents = []

        // enrollment tab
        vm.getEnrollmentEvents = function (deviceKey) {
            ProgressBarService.start();
            let commandEventsPromise = IntegrationEvents.getEnrollmentEvents(deviceKey);
            return commandEventsPromise.then(function (data) {
                vm.enrollmentEvents = data;
                return ProgressBarService.complete();
            });
        };

        vm.initialize = function () {
            vm.panelModels = DevicesService.getPanelModels();
            vm.panelInputs = DevicesService.getPanelInputs();
            let timezonePromise = TimezonesService.getCustomTimezones();
            timezonePromise.then(data => vm.timezones = data);

            let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
            devicePromise.then((response => vm.onGetDeviceSuccess(response)), response => {
                vm.onGetDeviceFailure(response)
            });
            vm.getEnrollmentEvents(vm.deviceKey)

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
                vm.backUrlText = 'Back to devices';
            } else {
                if (vm.currentDevice.isUnmanagedDevice === true) {
                    vm.backUrl = `/#/tenants/${vm.tenantKey}/unmanaged`;
                    vm.backUrlText = 'Back to tenant unmanaged devices';
                } else {
                    vm.backUrl = `/#/tenants/${vm.tenantKey}/managed`;
                    vm.backUrlText = 'Back to tenant managed devices';
                }
            }
            let locationsPromise = LocationsService.getLocationsByTenantKey(vm.tenantKey);
            return locationsPromise.then(function (data) {
                vm.locations = data;
                return vm.setSelectedLocationOptions();
            });
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