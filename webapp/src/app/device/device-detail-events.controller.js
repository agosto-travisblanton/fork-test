(function () {

let appModule = angular.module('skykitProvisioning');
appModule.controller('DeviceDetailsEventsCtrl', function(
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
    vm.dayRange = 30;
    vm.issues = [];
    vm.pickerOptions = "{widgetPositioning: {vertical:'bottom'}, showTodayButton: true, sideBySide: true, icons:{ next:'glyphicon glyphicon-arrow-right', previous:'glyphicon glyphicon-arrow-left',  up:'glyphicon glyphicon-arrow-up', down:'glyphicon glyphicon-arrow-down'}}";

    let now = new Date();
    let today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    vm.endTime = now.toLocaleString().replace(/,/g, "");
    today.setDate(now.getDate() - vm.dayRange);
    vm.startTime = today.toLocaleString().replace(/,/g, "");
    
    vm.generateLocalFromUTC = function(UTCTime) {
      let localTime = moment.utc(UTCTime).toDate();
      return localTime = moment(localTime).format('YYYY-MM-DD hh:mm:ss A');
    };

    vm.replaceIssueTime = function(issues) {
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

    vm.getIssues = function(device, epochStart, epochEnd, prev, next) {
      ProgressBarService.start();
      let issuesPromise = DevicesService.getIssuesByKey(device, epochStart, epochEnd, prev, next);
      return issuesPromise.then(function(data) {
        vm.replaceIssueTime(data.issues);
        vm.issues = data.issues;
        vm.prev_cursor = data.prev;
        vm.next_cursor = data.next;
        return ProgressBarService.complete();
      });
    };

    vm.paginateCall = function(forward) {
      if (forward) {
        return vm.getIssues(vm.deviceKey, vm.epochStart, vm.epochEnd, null, vm.next_cursor);

      } else {
        return vm.getIssues(vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, null);
      }
    };

    vm.initialize = function() {
      vm.epochStart = moment(new Date(vm.startTime)).unix();
      vm.epochEnd = moment(new Date(vm.endTime)).unix();

      let devicePromise = DevicesService.getDeviceByKey(vm.deviceKey);
      devicePromise.then((response => vm.onGetDeviceSuccess(response)), response => vm.onGetDeviceFailure(response));

      return vm.getIssues(vm.deviceKey, vm.epochStart, vm.epochEnd);
    };

    vm.onGetDeviceSuccess = function(response) {
      vm.currentDevice = response;
      if (response.timezone !== vm.selectedTimezone) { vm.selectedTimezone = response.timezone; }
      if (vm.tenantKey === undefined) { vm.tenantKey = vm.currentDevice.tenantKey; }
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

    vm.onGetDeviceFailure = function(response) {
      ToastsService.showErrorToast('Oops. We were unable to fetch the details for this device at this time.');
      let errorMessage = `No detail for device_key #${vm.deviceKey}. Error: ${response.status} ${response.statusText}`;
      $log.error(errorMessage);
      return $state.go('devices');
    };
      
      
    vm.onClickRefreshButton = function() {
      ProgressBarService.start();
      vm.epochStart = moment(new Date(vm.startTime)).unix();
      vm.epochEnd = moment(new Date(vm.endTime)).unix();
      vm.prev_cursor = null;
      vm.next_cursor = null;
      let issuesPromise = DevicesService.getIssuesByKey(vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, vm.next_cursor);
      return issuesPromise.then((data => vm.onRefreshIssuesSuccess(data)), error => vm.onRefreshIssuesFailure(error));
    };

    vm.onRefreshIssuesSuccess = function(data) {
      vm.replaceIssueTime(data.issues);
      vm.issues = data.issues;
      vm.prev_cursor = data.prev;
      vm.next_cursor = data.next;
      return ProgressBarService.complete();
    };

    vm.onRefreshIssuesFailure = function(error) {
      ProgressBarService.complete();
      ToastsService.showInfoToast('We were unable to refresh the device issues list at this time.');
      return $log.error(`Failure to refresh device issues: ${error.status } ${error.statusText}`);
    };


    return vm;
  });

})
();