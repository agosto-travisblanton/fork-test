let appModule = angular.module('skykitProvisioning');
appModule.controller('DeviceDetailsPropertiesCtrl', function(
  $log,
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

    vm.initialize = function() {
      vm.panelModels = DevicesService.getPanelModels();
      vm.panelInputs = DevicesService.getPanelInputs();
      let timezonePromise = TimezonesService.getCustomTimezones();
      timezonePromise.then(data => vm.timezones = data);

      let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
      return devicePromise.then((response => vm.onGetDeviceSuccess(response)), response => vm.onGetDeviceFailure(response));
    };

    vm.onGetDeviceSuccess = function(response) {
      vm.currentDevice = response;
      if (response.timezone !== vm.selectedTimezone) { vm.selectedTimezone = response.timezone; }
      if (vm.tenantKey === undefined) { vm.tenantKey = vm.currentDevice.tenantKey; }
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
      return locationsPromise.then(function(data) {
        vm.locations = data;
        return vm.setSelectedLocationOptions();
      });
    };

    vm.onGetDeviceFailure = function(response) {
      ToastsService.showErrorToast('Oops. We were unable to fetch the details for this device at this time.');
      let errorMessage = `No detail for device_key #${vm.deviceKey}. Error: ${response.status} ${response.statusText}`;
      $log.error(errorMessage);
      return $state.go('devices');
    };

    vm.setSelectedLocationOptions = function() {
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

    vm.onSaveDevice = function() {
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

    vm.onSuccessDeviceSave = function() {
      ProgressBarService.complete();
      return ToastsService.showSuccessToast('We saved your update.');
    };

    vm.onFailureDeviceSave = function(error) {
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

    vm.confirmDeviceDelete = function(event, key) {
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

    vm.onConfirmDelete = function(key) {
      let success = function() {
        ToastsService.showSuccessToast('We processed your delete request.');
        return $state.go('devices');
      };
      let failure = function(error) {
        let friendlyMessage = 'We were unable to complete your delete request at this time.';
        ToastsService.showErrorToast(friendlyMessage);
        return $log.error(`Delete device failure for device_key ${key}: ${error.status } ${error.statusText}`);
      };
      let deletePromise = DevicesService.delete(key);
      return deletePromise.then(success, failure);
    };

    vm.onConfirmCancel = () => ToastsService.showInfoToast('We canceled your delete request.');

    vm.onProofOfPlayLoggingCheck = function() {
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

    vm.autoGenerateCustomerDisplayCode = function() {
      let newDisplayCode = '';
      if (vm.currentDevice.customerDisplayName) {
        newDisplayCode = vm.currentDevice.customerDisplayName.toLowerCase();
        newDisplayCode = newDisplayCode.replace(/\s+/g, '_');
        newDisplayCode = newDisplayCode.replace(/\W+/g, '');
      }
      return vm.currentDevice.customerDisplayCode = newDisplayCode;
    };

    vm.logglyForUser = function() {
      let userDomain = SessionsService.getUserEmail().split("@")[1];
      return userDomain === "demo.agosto.com" || userDomain === "agosto.com";
    };

    return vm;
  });
