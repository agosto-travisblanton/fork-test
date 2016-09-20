import moment from 'moment';

function DeviceDetailsCommandsCtrl($log,
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
                                   $timeout) {
  "ngInject";

  let vm = this;
  vm.tenantKey = $stateParams.tenantKey;
  vm.deviceKey = $stateParams.deviceKey;
  vm.fromDevices = $stateParams.fromDevices === "true";
  vm.currentDevice = {};
  vm.commandEvents = [];

  vm.generateLocalFromUTC = function (UTCTime) {
    let localTime = moment.utc(UTCTime).toDate();
    return localTime = moment(localTime).format('YYYY-MM-DD hh:mm:ss A');
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

  vm.getEventsTimeOut = (deviceKey, prev, next) =>
    $timeout(( () => vm.getEvents(deviceKey, prev, next)), 1000)
  ;

  vm.commandHistorySelected = () => vm.getEvents(vm.deviceKey);

  vm.paginateEventCall = function (forward) {
    if (forward) {
      return vm.getEvents(vm.deviceKey, null, vm.event_next_cursor);

    } else {
      return vm.getEvents(vm.deviceKey, vm.event_prev_cursor, null);
    }
  };

  vm.initialize = function () {
    let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
    devicePromise.then((response => vm.onGetDeviceSuccess(response)), response => vm.onGetDeviceFailure(response));

    return vm.getEvents(vm.deviceKey);
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

  vm.onResetContent = function () {
    ProgressBarService.start();
    let promise = CommandsService.contentDelete(vm.deviceKey);
    return promise.then(vm.onResetContentSuccess, vm.onResetContentFailure);
  };

  vm.onResetContentSuccess = function () {
    ProgressBarService.complete();
    vm.getEventsTimeOut(vm.deviceKey);
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
    vm.getEventsTimeOut(vm.deviceKey);
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
    vm.getEventsTimeOut(vm.deviceKey);
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
    vm.getEventsTimeOut(vm.deviceKey);
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
    vm.getEventsTimeOut(vm.deviceKey);
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
    vm.getEventsTimeOut(vm.deviceKey);
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
    vm.getEventsTimeOut(vm.deviceKey);
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
    vm.getEventsTimeOut(vm.deviceKey);
    return ToastsService.showSuccessToast(`We posted your custom command '${command}' into the player's queue.`);
  };

  vm.onCustomCommandFailure = function (error) {
    ProgressBarService.complete();
    $log.error(`Custom command error: ${error.status } ${error.statusText}`);
    return sweet.show('Oops...', "We were unable to post your custom command into the player's queue.", 'error');
  };

  vm.onDiagnosticsToggle = function () {
    ProgressBarService.start();
    let promise = CommandsService.toggleDiagnostics(vm.deviceKey);
    return promise.then(vm.onToggleDiagnosticsSuccess, vm.onToggleDiagnosticsFailure);
  };

  vm.onToggleDiagnosticsSuccess = function () {
    ProgressBarService.complete();
    return ToastsService.showSuccessToast("We posted your diagnostics command into the player's queue.");
  };

  vm.onToggleDiagnosticsFailure = function (error) {
    ProgressBarService.complete();
    $log.error(`Diagnostics command error: ${error.status } ${error.statusText}`);
    return sweet.show('Oops...', "We were unable to post your diagnostics command into the player's queue.",
      'error');
  };

  vm.onRestart = function () {
    ProgressBarService.start();
    let promise = CommandsService.restart(vm.deviceKey);
    return promise.then(vm.onRestartSuccess, vm.onRestartFailure);
  };

  vm.onRestartSuccess = function () {
    ProgressBarService.complete();
    return ToastsService.showSuccessToast("We posted your restart command into the player's queue.");
  };

  vm.onRestartFailure = function (error) {
    ProgressBarService.complete();
    $log.error(`Restart command error: ${error.status } ${error.statusText}`);
    return sweet.show('Oops...', "We were unable to post your restart command into the player's queue.",
      'error');
  };

  vm.onPostLog = function () {
    ProgressBarService.start();
    let promise = CommandsService.postLog(vm.deviceKey);
    return promise.then(vm.onPostLogSuccess, vm.onPostLogFailure);
  };

  vm.onPostLogSuccess = function () {
    ProgressBarService.complete();
    return ToastsService.showSuccessToast("We posted your post log command into the player's queue.");
  };

  vm.onPostLogFailure = function (error) {
    ProgressBarService.complete();
    $log.error(`Post log command error: ${error.status } ${error.statusText}`);
    return sweet.show('Oops...', "We were unable to post your post log command into the player's queue.",
      'error');
  };

  return vm;
}

export {DeviceDetailsCommandsCtrl}
