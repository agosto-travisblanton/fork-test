import moment from 'moment';

function DeviceDetailsCtrl($log,
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
                           ToastsService,
                           DateManipulationService,
                           $sce) {
  "ngInject";

  const vm = this;
  vm.tenantKey = $stateParams.tenantKey;
  vm.deviceKey = $stateParams.deviceKey;
  vm.fromDevices = $stateParams.fromDevices === "true";
  vm.currentDevice = {};
  vm.locations = [];
  vm.commandEvents = [];
  vm.dayRange = 30;
  vm.issues = [];
  vm.timezones = [];
  vm.selectedTimezone = undefined;
  [vm.startTime, vm.endTime] = DateManipulationService.createFormattedStartAndEndDateFromToday(30);
  vm.enrollmentEvents = [];
  vm.logoChange = false;

  vm.getTenantImages = () => {
    vm.OVERLAY_TYPES = [
      {type: "TIME", name: "TIME", new: true, image_urlsafe_key: null},
      {type: "DATE", name: "DATE", new: true, image_urlsafe_key: null},
      {type: "DATETIME", name: "DATETIME", new: true, image_urlsafe_key: null},
    ]

    DevicesService.getImages(vm.tenantKey)
      .then((res) => {
        res.forEach((value) => {
          value.svg_rep = $sce.trustAsHtml(JSON.parse(value.svg_rep))
          value.type = "LOGO"
          value.realName = angular.copy(value.name)
          console.log(value.realName)
          value.name = "LOGO: " + value.name
          value.image_urlsafe_key = value.key
          vm.OVERLAY_TYPES.push(value)
        })
        console.log(vm.OVERLAY_TYPES)
      })
  }


  vm.replaceIssueTime = function (issues) {
    for (let i = 0; i < issues.length; i++) {
      let each = issues[i];
      if (each.created) {
        each.created = DateManipulationService.generateLocalFromUTC(each.created);
      }
      if (each.updated) {
        each.updated = DateManipulationService.generateLocalFromUTC(each.updated);
      }
    }
    return;
  };

  vm.replaceCommandTime = function (issues) {
    for (let i = 0; i < issues.length; i++) {
      let each = issues[i];
      if (each.postedTime) {
        each.postedTime = DateManipulationService.generateLocalFromUTC(each.postedTime);
      }
      if (each.confirmedTime) {
        each.confirmedTime = DateManipulationService.generateLocalFromUTC(each.confirmedTime);
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
    vm.epochStart = moment(vm.startTime, 'YYYY-MM-DD hh:mm A').unix();
    vm.epochEnd = moment(vm.endTime, 'YYYY-MM-DD hh:mm A').unix();

    let timezonePromise = TimezonesService.getCustomTimezones();
    timezonePromise.then(data => vm.timezones = data);

    vm.panelModels = DevicesService.getPanelModels();
    vm.panelInputs = DevicesService.getPanelInputs();

    let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
    devicePromise.then((response => vm.onGetDeviceSuccess(response)), response => vm.onGetDeviceFailure(response));

    vm.getTenantImages();
    vm.getEvents(vm.deviceKey);
    vm.getIssues(vm.deviceKey, vm.epochStart, vm.epochEnd);
    return vm.getEnrollmentEvents(vm.deviceKey);
  };

  vm.onGetDeviceSuccess = function (response) {
    vm.currentDevice = response;
    console.log(vm.currentDevice.overlays)
    console.log(vm.currentDevice.overlay)

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
  vm.adjustOverlayStatus = (status) => {
    vm.currentDevice.overlay_status = status
    ProgressBarService.start();
    let promise = DevicesService.save(vm.currentDevice);
    return promise.then(() => {
      let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
      devicePromise.then((response => {
        vm.onGetDeviceSuccess(response)
        ProgressBarService.complete();
      }), response => vm.onGetDeviceFailure(response));
    })
  }

  vm.submitOverlaySettings = (overlayForm) => {
    let overlaySettings = vm.currentDevice.overlay;
    delete overlaySettings.key;
    delete overlaySettings.device_key;


    ProgressBarService.start();
    DevicesService.saveOverlaySettings(vm.deviceKey, overlaySettings)
      .then((res) => {
        console.log(res)
        ProgressBarService.complete();
      })
  }


  vm.submitImage = () => {

    if (vm.selectedLogo && vm.selectedLogo[0]) {
      ProgressBarService.start();

      var r = new FileReader();
      r.onload = function () {

        vm.selectedLogoFinal = {}
        vm.selectedLogoFinal.asString = JSON.stringify(r.result)
        vm.selectedLogoFinal.name = vm.selectedLogo[0].lfFileName
        vm.selectedLogoChange = true;

        DevicesService.saveImage(vm.tenantKey, vm.selectedLogoFinal.asString, vm.selectedLogoFinal.name)
          .then((res) => {
            console.log(res)
            ProgressBarService.complete();
            vm.getTenantImages();

          })
      }
      r.readAsText(vm.selectedLogo[0].lfFile);
    }
  }


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

  vm.onPanelSleep = function (command) {
    ProgressBarService.start();
    let promise = CommandsService.panelSleep(vm.deviceKey, command);
    return promise.then(vm.onPanelSleepSuccess, vm.onPanelSleepFailure);
  };

  vm.onPanelSleepSuccess = function () {
    ProgressBarService.complete();
    return ToastsService.showSuccessToast("We toggled the panel sleep attribute. The player should adjust to these changes within 15 minutes.");
  };

  vm.onPanelSleepFailure = function (error) {
    ProgressBarService.complete();
    return sweet.show('Oops...', "We were unable to toggle the panel sleep attribute.", 'error');
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

  vm.onClickRefreshButton = function () {
    ProgressBarService.start();
    vm.startTime = DateManipulationService.convertToMomentIfNotAlready(vm.startTime);
    vm.endTime = DateManipulationService.convertToMomentIfNotAlready(vm.endTime);
    vm.epochStart = moment(vm.startTime, 'YYYY-MM-DD hh:mm A').unix();
    vm.epochEnd = moment(vm.endTime, 'YYYY-MM-DD hh:mm A').unix();
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
}

export {DeviceDetailsCtrl}

