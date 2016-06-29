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
                                                        IntegrationEvents,
                                                        sweet,
                                                        ProgressBarService,
                                                        $mdDialog,
                                                        ToastsService) {
        let vm = this;
        vm.tenantKey = $stateParams.tenantKey;
        vm.deviceKey = $stateParams.deviceKey;
        vm.fromDevices = $stateParams.fromDevices === "true";
        vm.currentDevice = {};
        vm.locations = [];
        vm.commandEvents = [];
        vm.dayRange = 30;
        vm.issues = [];
        vm.pickerOptions = "{widgetPositioning: {vertical:'bottom'}, showTodayButton: true, sideBySide: true, icons:{ next:'glyphicon glyphicon-arrow-right', previous:'glyphicon glyphicon-arrow-left', up:'glyphicon glyphicon-arrow-up', down:'glyphicon glyphicon-arrow-down'}}";
        vm.timezones = [];
        vm.selectedTimezone = undefined;
        let now = new Date();
        let today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        vm.endTime = now.toLocaleString().replace(/,/g, "");
        today.setDate(now.getDate() - vm.dayRange);
        vm.startTime = today.toLocaleString().replace(/,/g, "");
        vm.enrollmentEvents = [];

        vm.generateLocalFromUTC = function (UTCTime) {
            let localTime = moment.utc(UTCTime).toDate();
            return localTime = moment(localTime).format('YYYY-MM-DD hh:mm:ss A');
        };

        vm.replaceIssueTime = function (issues) {
            for (let i = 0; i < issues.length; i++) {
                let each = issues[i];
                if (each.created) {
                    each.created = vm.generateLocalFromUTC(each.created);
                }
                if (each.updated) {
                    each.updated = vm.generateLocalFromUTC(each.updated);
                }
            }
            return;
        };

        vm.replaceCommandTime = function (issues) {
            for (let i = 0; i < issues.length; i++) {
                let each = issues[i];
                if (each.postedTime) {
                    each.postedTime = vm.generateLocalFromUTC(each.postedTime);
                }
                if (each.confirmedTime) {
                    each.confirmedTime = vm.generateLocalFromUTC(each.confirmedTime);
                }
            }
            return;
        };

        vm.copyDeviceKey = () => ToastsService.showSuccessToast('Device key copied to your clipboard');

        vm.copyCorrelationIdentifier = () => ToastsService.showSuccessToast('Correlation ID copied to your clipboard');

        // event tab
        vm.getIssues = function (device, epochStart, epochEnd, prev, next) {
            ProgressBarService.start();
            let issuesPromise = DevicesService.getIssuesByKey(device, epochStart, epochEnd, prev, next);
            return issuesPromise.then(function (data) {
                vm.replaceIssueTime(data.issues);
                vm.issues = data.issues;
                vm.prev_cursor = data.prev;
                vm.next_cursor = data.next;
                return ProgressBarService.complete();
            });
        };

        // command history tab
        vm.getEvents = function (deviceKey, prev, next) {
            ProgressBarService.start();
            let commandEventsPromise = DevicesService.getCommandEventsByKey(deviceKey, prev, next);
            return commandEventsPromise.then(function (data) {
                vm.replaceCommandTime(data.events);
                vm.event_next_cursor = data.next_cursor;
                vm.event_prev_cursor = data.prev_cursor;
                vm.commandEvents = data.events;
                return ProgressBarService.complete();
            });
        };

        // enrollment tab
        vm.getEnrollmentEvents = function (deviceKey) {
            ProgressBarService.start();
            let commandEventsPromise = IntegrationEvents.getEnrollmentEvents(deviceKey);
            return commandEventsPromise.then(function (data) {
                vm.enrollmentEvents = data;
                return ProgressBarService.complete();
            });
        };

        vm.paginateCall = function (forward) {
            if (forward) {
                return vm.getIssues(vm.deviceKey, vm.epochStart, vm.epochEnd, null, vm.next_cursor);

            } else {
                return vm.getIssues(vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, null);
            }
        };

        vm.paginateEventCall = function (forward) {
            if (forward) {
                return vm.getEvents(vm.deviceKey, null, vm.event_next_cursor);

            } else {
                return vm.getEvents(vm.deviceKey, vm.event_prev_cursor, null);
            }
        };

        vm.initialize = function () {
            vm.epochStart = moment(new Date(vm.startTime)).unix();
            vm.epochEnd = moment(new Date(vm.endTime)).unix();
            let timezonePromise = TimezonesService.getCustomTimezones();
            timezonePromise.then(data => vm.timezones = data);

            vm.panelModels = DevicesService.getPanelModels();
            vm.panelInputs = DevicesService.getPanelInputs();

            let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
            devicePromise.then((response => vm.onGetDeviceSuccess(response)), response => vm.onGetDeviceFailure(response));

            vm.getEvents(vm.deviceKey);
            vm.getIssues(vm.deviceKey, vm.epochStart, vm.epochEnd);
            return vm.getEnrollmentEvents(vm.deviceKey);
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
                return vm.setSelectedOptions();
            });
        };

        vm.onGetDeviceFailure = function (response) {
            ToastsService.showErrorToast('Oops. We were unable to fetch the details for this device at this time.');
            let errorMessage = `No detail for device_key #${vm.deviceKey}. Error: ${response.status} ${response.statusText}`;
            $log.error(errorMessage);
            return $state.go('devices');
        };

        vm.setSelectedOptions = function () {
            if (vm.currentDevice.panelModel === null) {
                vm.currentDevice.panelModel = vm.panelModels[0];
                vm.currentDevice.panelInput = vm.panelInputs[0];
            } else {
                for (let i = 0; i < vm.panelModels.length; i++) {
                    let panelModel = vm.panelModels[i];
                    if (panelModel.id === vm.currentDevice.panelModel) {
                        vm.currentDevice.panelModel = panelModel;
                    }
                }
                for (let j = 0; j < vm.panelInputs.length; j++) {
                    let panelInput = vm.panelInputs[j];
                    let isParent = panelInput.parentId === vm.currentDevice.panelModel.id;
                    if (isParent && panelInput.id.toLowerCase() === vm.currentDevice.panelInput) {
                        vm.currentDevice.panelInput = panelInput;
                    }
                }
            }
            if (vm.currentDevice.locationKey !== null) {
                for (let k = 0; k < vm.locations.length; k++) {
                    let location = vm.locations[k];
                    if (location.key === vm.currentDevice.locationKey) {
                        vm.currentDevice.location = location;
                    }
                }
                return;
            }
        };

        //####################
        // Properties Tab
        //####################

        vm.onSaveDevice = function () {
            ProgressBarService.start();
            if (vm.currentDevice.location !== undefined && vm.currentDevice.location.key !== undefined) {
                vm.currentDevice.locationKey = vm.currentDevice.location.key;
            }
            if (vm.currentDevice.panelModel.id !== undefined && vm.currentDevice.panelModel.id !== 'None') {
                vm.currentDevice.panelModelNumber = vm.currentDevice.panelModel.id;
            }
            if (vm.currentDevice.panelInput.id !== undefined && vm.currentDevice.panelInput.id !== 'None') {
                vm.currentDevice.panelSerialInput = vm.currentDevice.panelInput.id.toLowerCase();
            }
            vm.currentDevice.timezone = vm.selectedTimezone;
            let promise = DevicesService.save(vm.currentDevice);
            return promise.then(vm.onSuccessDeviceSave, vm.onFailureDeviceSave);
        };

        vm.onSuccessDeviceSave = function () {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast('We saved your update.');
        };

        vm.onFailureDeviceSave = function (error) {
            ProgressBarService.complete();
            if (error.status === 409) {
                $log.info(
                    `Failure saving device. Customer display code already exists for tenant: ${error.status } ${error.statusText}`);
                return sweet.show('Oops...', 'This customer display code already exists for this tenant. Please choose another.', 'error');
            } else {
                $log.error(`Failure saving device: ${error.status } ${error.statusText}`);
                return ToastsService.showErrorToast('Oops. We were unable to save your updates to this device at this time.');
            }
        };

        vm.confirmDeviceDelete = function (event, key) {
            let confirm = $mdDialog.confirm(
                {
                    title: 'Are you sure to delete this device?',
                    textContent: 'Please remember, you MUST remove this device from Content Manager before deleting it from Provisioning.',
                    targetEvent: event,
                    ok: 'Delete',
                    cancel: 'Cancel'
                }
            );
            let showPromise = $mdDialog.show(confirm);
            let success = () => vm.onConfirmDelete(key);
            let failure = () => vm.onConfirmCancel();
            return showPromise.then(success, failure);
        };

        vm.onConfirmDelete = function (key) {
            let success = function () {
                ToastsService.showSuccessToast('We processed your delete request.');
                return $state.go('devices');
            };
            let failure = function (error) {
                let friendlyMessage = 'We were unable to complete your delete request at this time.';
                ToastsService.showErrorToast(friendlyMessage);
                return $log.error(`Delete device failure for device_key ${key}: ${error.status } ${error.statusText}`);
            };
            let deletePromise = DevicesService.delete(key);
            return deletePromise.then(success, failure);
        };

        vm.onConfirmCancel = () => ToastsService.showInfoToast('We canceled your delete request.');

        vm.onProofOfPlayLoggingCheck = function () {
            if (vm.currentDevice.proofOfPlayLogging) {
                let noLocation = vm.currentDevice.locationKey === null;
                let noDisplayCode = vm.currentDevice.customerDisplayCode === null;
                if (noLocation) {
                    sweet.show('Oops...', "You must have a Location to enable Proof of play.", 'error');
                    return vm.currentDevice.proofOfPlayLogging = false;
                } else if (noDisplayCode) {
                    sweet.show('Oops...', "You must have a Display code to enable Proof of play.", 'error');
                    return vm.currentDevice.proofOfPlayLogging = false;
                } else {
                    return vm.onSaveDevice();
                }
            } else {
                return vm.onSaveDevice();
            }
        };

        vm.onUpdateLocation = () => vm.onSaveDevice();

        vm.autoGenerateCustomerDisplayCode = function () {
            let newDisplayCode = '';
            if (vm.currentDevice.customerDisplayName) {
                newDisplayCode = vm.currentDevice.customerDisplayName.toLowerCase();
                newDisplayCode = newDisplayCode.replace(/\s+/g, '_');
                newDisplayCode = newDisplayCode.replace(/\W+/g, '');
            }
            return vm.currentDevice.customerDisplayCode = newDisplayCode;
        };

        vm.logglyForUser = function () {
            let userDomain = SessionsService.getUserEmail().split("@")[1];
            return userDomain === "demo.agosto.com" || userDomain === "agosto.com";
        };

        //####################
        // Commands Tab
        //####################

        vm.onResetContent = function () {
            ProgressBarService.start();
            let promise = CommandsService.contentDelete(vm.deviceKey);
            return promise.then(vm.onResetContentSuccess, vm.onResetContentFailure);
        };

        vm.onResetContentSuccess = function () {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast("We posted your reset content command into the player's queue.");
        };

        vm.onResetContentFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Reset content command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your reset content command into the player's queue.", 'error');
        };

        vm.onUpdateContent = function () {
            ProgressBarService.start();
            let promise = CommandsService.contentUpdate(vm.deviceKey);
            return promise.then(vm.onUpdateContentSuccess, vm.onUpdateContentFailure);
        };

        vm.onUpdateContentSuccess = function () {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast("We posted your update content command into the player's queue.");
        };

        vm.onUpdateContentFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Content update command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your update content command into the player's queue.", 'error');
        };

        vm.onResetPlayer = function () {
            ProgressBarService.start();
            let promise = CommandsService.reset(vm.deviceKey);
            return promise.then(vm.onResetPlayerSuccess, vm.onResetPlayerFailure);
        };

        vm.onResetPlayerSuccess = function () {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast("We posted your reset player command into the player's queue.");
        };

        vm.onResetPlayerFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Reset player command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your reset player command into the player's queue.", 'error');
        };

        vm.onPanelOn = function () {
            ProgressBarService.start();
            let promise = CommandsService.powerOn(vm.deviceKey);
            return promise.then(vm.onPanelOnSuccess, vm.onPanelOnFailure);
        };

        vm.onPanelOnSuccess = function () {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast("We posted your panel on command into the player's queue.");
        };

        vm.onPanelOnFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Panel on command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your panel on command into the player's queue.", 'error');
        };

        vm.onPanelOff = function () {
            ProgressBarService.start();
            let promise = CommandsService.powerOff(vm.deviceKey);
            return promise.then(vm.onPanelOffSuccess, vm.onPanelOffFailure);
        };

        vm.onPanelOffSuccess = function () {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast("We posted your panel off command into the player's queue.");
        };

        vm.onPanelOffFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Panel off command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your panel off command into the player's queue.", 'error');
        };

        vm.onUpdateDevice = function () {
            ProgressBarService.start();
            let promise = CommandsService.updateDevice(vm.deviceKey);
            return promise.then(vm.onUpdateDeviceSuccess, vm.onUpdateDeviceFailure);
        };

        vm.onUpdateDeviceSuccess = function () {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast("We posted your update device command into the player's queue.");
        };

        vm.onUpdateDeviceFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Update device command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your update device command into the player's queue.", 'error');
        };

        vm.onVolumeChange = function () {
            ProgressBarService.start();
            let promise = CommandsService.volume(vm.deviceKey, vm.currentDevice.volume);
            return promise.then(vm.onVolumeChangeSuccess(vm.currentDevice.volume), vm.onVolumeChangeFailure);
        };

        vm.onVolumeChangeSuccess = function (level) {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast(`We posted your volume change command of ${level} into the player's queue.`);
        };

        vm.onVolumeChangeFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Volume change command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your volume change command into the player's queue.", 'error');
        };

        vm.onCustomCommand = function () {
            ProgressBarService.start();
            let promise = CommandsService.custom(vm.deviceKey, vm.currentDevice.custom);
            return promise.then(vm.onCustomCommandSuccess(vm.currentDevice.custom), vm.onCustomCommandFailure);
        };

        vm.onCustomCommandSuccess = function (command) {
            ProgressBarService.complete();
            return ToastsService.showSuccessToast(`We posted your custom command '${command}' into the player's queue.`);
        };

        vm.onCustomCommandFailure = function (error) {
            ProgressBarService.complete();
            $log.error(`Custom command error: ${error.status } ${error.statusText}`);
            return sweet.show('Oops...', "We were unable to post your custom command into the player's queue.", 'error');
        };

        vm.onClickRefreshButton = function () {
            ProgressBarService.start();
            vm.epochStart = moment(new Date(vm.startTime)).unix();
            vm.epochEnd = moment(new Date(vm.endTime)).unix();
            vm.prev_cursor = null;
            vm.next_cursor = null;
            let issuesPromise = DevicesService.getIssuesByKey(vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, vm.next_cursor);
            return issuesPromise.then((data => vm.onRefreshIssuesSuccess(data)), error => vm.onRefreshIssuesFailure(error));
        };

        vm.onRefreshIssuesSuccess = function (data) {
            vm.replaceIssueTime(data.issues);
            vm.issues = data.issues;
            vm.prev_cursor = data.prev;
            vm.next_cursor = data.next;
            return ProgressBarService.complete();
        };

        vm.onRefreshIssuesFailure = function (error) {
            ProgressBarService.complete();
            ToastsService.showInfoToast('We were unable to refresh the device issues list at this time.');
            return $log.error(`Failure to refresh device issues: ${error.status } ${error.statusText}`);
        };

        return vm;
    });
})
();