import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject
import moment from 'moment'



describe('DeviceDetailsCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let $stateParams = undefined;
  let $state = undefined;
  let $log = undefined;
  let $mdDialog = undefined;
  let DevicesService = undefined;
  let TimezonesService = undefined;
  let getDeviceIssuesPromise = undefined;
  let getPlayerCommandEventsPromise = undefined;
  let LocationsService = undefined;
  let locationsServicePromise = undefined;
  let CommandsService = undefined;
  let ToastsService = undefined;
  let commandsServicePromise = undefined;
  let sweet = undefined;
  let progressBarService = undefined;
  let serviceInjection = undefined;
  let StorageService = undefined;

  let device = {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'};
  let issues = {
    issues: [
      {
        category: "Player down",
        created: "2015-12-15 18:05:52",
        elapsed_time: "37.3 minutes",
        level: 2,
        levelDescriptor: "danger",
        memoryUtilization: 40,
        program: "Test Content",
        playlist: "Playlist 1",
        storageUtilization: 44,
        up: false
      },
      {
        category: "Player up",
        created: "2015-12-15 18:05:52",
        elapsedTime: "37.3 minutes",
        level: 0,
        levelDescriptor: "normal",
        memoryUtilization: 40,
        program: "Test Content",
        playlist: "Playlist 1",
        storageUtilization: 44,
        up: true
      }
    ]
  };
  let commandEvents = {
    events: [
      {
        payload: 'skykit.com/skdchromeapp/reset',
        gcmRegistrationId: 'asdfasdfasdfadfsa1',
        updated: '2016-01-14 18:45:44',
        confirmed: false
      },
      {
        payload: 'skykit.com/skdchromeapp/stop',
        gcmRegistrationId: 'asdfasdfasdfadfsa2',
        updated: '2016-01-14 18:23:30',
        confirmed: false
      }
    ]
  };
  let tenants = [
    {
      key: 'dhjad897d987fadafg708fg7d',
      name: 'Foobar1',
      created: '2015-05-10 22:15:10',
      updated: '2015-05-10 22:15:10'
    },
    {
      key: 'dhjad897d987fadafg708y67d',
      name: 'Foobar2',
      created: '2015-05-10 22:15:10',
      updated: '2015-05-10 22:15:10'
    },
    {
      key: 'dhjad897d987fadafg708hb55',
      name: 'Foobar3',
      created: '2015-05-10 22:15:10',
      updated: '2015-05-10 22:15:10'
    }
  ];

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_, _DevicesService_, _TimezonesService_, _LocationsService_, _CommandsService_,
                              _sweet_, _ToastsService_, _$state_, _$mdDialog_, _$log_, _StorageService_) {
    $controller = _$controller_;
    $stateParams = {};
    $state = _$state_;
    $log = _$log_;
    $mdDialog = _$mdDialog_;
    DevicesService = _DevicesService_;
    TimezonesService = _TimezonesService_;
    LocationsService = _LocationsService_;
    CommandsService = _CommandsService_;
    ToastsService = _ToastsService_;
    StorageService = _StorageService_;
    progressBarService = {
      start() {
      },
      complete() {
      }
    };
    sweet = _sweet_;
    let scope = {};
    return serviceInjection = {
      $scope: scope,
      ToastsService,
      $stateParams,
      ProgressBarService: progressBarService,
      $mdDialog
    };
  }));

  describe('initialize', function () {
    beforeEach(function () {
      let getDevicePromise = new skykitProvisioning.q.Mock();
      let timezonesPromise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'getDeviceByKey').and.returnValue(getDevicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      getPlayerCommandEventsPromise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'getCommandEventsByKey').and.returnValue(getPlayerCommandEventsPromise);
      getDeviceIssuesPromise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'getIssuesByKey').and.returnValue(getDeviceIssuesPromise);
      spyOn(DevicesService, 'getPanelModels').and.returnValue([{'id': 'Sony–FXD40LX2F'}, {'id': 'NEC–LCD4215'}]);

      let inputs = [
        {
          'id': 'HDMI2',
          'parentId': 'Sony–FXD40LX2F'
        },
        {
          'id': 'HDMI1',
          'parentId': 'Sony–FXD40LX2F'
        },
        {
          'id': 'VGA',
          'parentId': 'NEC–LCD4215'
        }
      ];

      spyOn(DevicesService, 'getPanelInputs').and.returnValue(inputs);
      return spyOn(TimezonesService, 'getCustomTimezones').and.returnValue(timezonesPromise);
    });

    describe('new mode', function () {
      beforeEach(function () {
        controller = $controller('DeviceDetailsCtrl', {
          $stateParams,
          $state,
          DevicesService,
          ProgressBarService: progressBarService,
          TimezonesService,
          LocationsService
        });
        return controller.initialize();
      });

      it('should call TimezonesService.getCustomTimezones', () => expect(TimezonesService.getCustomTimezones).toHaveBeenCalled());

      it('currentDevice property should be defined', () => expect(controller.currentDevice).toBeDefined());

      it('commandEvents array should be defined', () => expect(controller.commandEvents).toBeDefined());

      it('issues array should be defined', () => expect(controller.issues).toBeDefined());

      it('declares timezones as an empty array', function () {
        expect(angular.isArray(controller.timezones)).toBeTruthy();
        return expect(controller.timezones.length).toBe(0);
      });

      return it('declares a selectedTimezone', () => expect(controller.selectedTimezone).toBeUndefined());
    });

    return describe('edit mode', function () {
      beforeEach(function () {
        $stateParams = {
          deviceKey: 'fkasdhfjfa9s8udyva7dygoudyg',
          tenantKey: 'tkasdhfjfa9s2udyva5digopdy0'
        };
        controller = $controller('DeviceDetailsCtrl', {
          $stateParams,
          $state,
          ProgressBarService: progressBarService,
          ToastsService,
          DevicesService,
          TimezonesService,
          LocationsService
        });

        let now = new Date();
        let today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        today.setDate(today.getDate() - 30);
        controller.epochEnd = moment(new Date()).unix();
        controller.epochStart = moment(today).unix();
        spyOn(ToastsService, 'showErrorToast');
        spyOn(ToastsService, 'showSuccessToast');
        return controller.initialize();
      });

      it('should call TimezonesService.getCustomTimezones', () => expect(TimezonesService.getCustomTimezones).toHaveBeenCalled());

      it('defines currentDevice property', () => expect(controller.currentDevice).toBeDefined());

      it('calls DevicesService.getPanelModels to retrieve all panel models', () => expect(DevicesService.getPanelModels).toHaveBeenCalled());

      it('calls DevicesService.getPanelInputs to retrieve all panel inputs', () => expect(DevicesService.getPanelInputs).toHaveBeenCalled());

      it('calls DevicesService.getByKey to retrieve the selected device', () => expect(DevicesService.getDeviceByKey).toHaveBeenCalledWith($stateParams.deviceKey));

      it('calls DevicesService.getCommandEventsByKey to retrieve command events for device', () => expect(DevicesService.getCommandEventsByKey).toHaveBeenCalledWith($stateParams.deviceKey, undefined, undefined));

      it('calls DevicesService.getIssuesByKey to retrieve the issues for a given device and datetime range', () => expect(DevicesService.getIssuesByKey).toHaveBeenCalledWith($stateParams.deviceKey, controller.epochStart, controller.epochEnd, undefined, undefined));

      it("the 'then' handler caches the retrieved issues for a given device key in the controller", function () {
        getDeviceIssuesPromise.resolve({issues});
        return expect(controller.issues).toBe(issues);
      });

      return it("the 'then' handler caches the retrieved command events in the controller", function () {
        getPlayerCommandEventsPromise.resolve(commandEvents);
        return expect(controller.commandEvents).toBe(commandEvents.events);
      });
    });
  });

  describe('.onGetDeviceSuccess', function () {
    let tenantKey = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWR3JvdXAiEXRlbmFudlbmFudBiAgICAgIDACAw';
    let timezone = 'America/Denver';
    let response = {
      tenantKey,
      tenantName: 'Acme, Inc.',
      timezone,
      timezoneOffset: -6
    };
    beforeEach(function () {
      $stateParams = {fromDevices: "true"};
      locationsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(LocationsService, 'getLocationsByTenantKey').and.returnValue(locationsServicePromise);
      controller = $controller('DeviceDetailsCtrl', serviceInjection);
      controller.tenantKey = undefined;
      controller.selectedTimezone = "America/Chicago";
      return controller.onGetDeviceSuccess(response);
    });

    it('sets the current device', () => expect(controller.currentDevice).toBe(response));

    it('sets the selected timezone', () => expect(controller.selectedTimezone).toBe(timezone));

    it('sets the tenant key', () => expect(controller.tenantKey).toBe(tenantKey));

    it('calls LocationsService.getLocationsByTenantKey with tenant key to get tenant locations', () => expect(LocationsService.getLocationsByTenantKey).toHaveBeenCalledWith(tenantKey));

    describe('coming from devices', function () {
      beforeEach(function () {
        $stateParams = {fromDevices: "true"};
        controller = $controller('DeviceDetailsCtrl', {
          $stateParams
        });
        return controller.onGetDeviceSuccess(response);
      });

      return it('sets the back button text according to previous context', () => expect(controller.backUrlText).toBe('Back to devices'));
    });

    describe('coming from tenant unmanaged devices', function () {
      beforeEach(function () {
        $stateParams = {fromDevices: "false"};
        controller = $controller('DeviceDetailsCtrl', {
          $stateParams
        });
        response.isUnmanagedDevice = true;
        return controller.onGetDeviceSuccess(response);
      });

      it('sets the back button text according to previous context', () => expect(controller.backUrlText).toBe('Back to tenant unmanaged devices'));

      return it('sets the back url according to previous context', () => expect(controller.backUrl).toBe(`/#/tenants/${tenantKey}/unmanaged`));
    });

    return describe('coming from tenant managed devices', function () {
      beforeEach(function () {
        $stateParams = {fromDevices: "false"};
        controller = $controller('DeviceDetailsCtrl', {
          $stateParams
        });
        response.isUnmanagedDevice = false;
        return controller.onGetDeviceSuccess(response);
      });

      it('sets the back button text according to previous context', () => expect(controller.backUrlText).toBe('Back to tenant managed devices'));

      return it('sets the back url according to previous context', () => expect(controller.backUrl).toBe(`/#/tenants/${tenantKey}/managed`));
    });
  });


  describe('.onGetDeviceFailure', function () {
    beforeEach(function () {
      spyOn($log, 'error');
      spyOn($state, 'go');
      spyOn(ToastsService, 'showErrorToast');
      spyOn(ToastsService, 'showSuccessToast');
      controller = $controller('DeviceDetailsCtrl', serviceInjection);
      controller.deviceKey = 'key';
      let response = {status: 400, statusText: 'Bad Request'};
      return controller.onGetDeviceFailure(response);
    });

    it('displays a toast notifying the user', () =>
      expect(ToastsService.showErrorToast).toHaveBeenCalledWith(
        'Oops. We were unable to fetch the details for this device at this time.')
    );

    it('logs error to the console', function () {
      let errorMessage = `No detail for device_key #${controller.deviceKey = 'key'}. Error: 400 Bad Request`;
      return expect($log.error).toHaveBeenCalledWith(errorMessage);
    });

    return it('navigates back to devices list', () => expect($state.go).toHaveBeenCalledWith('devices'));
  });


  describe('.onSaveDevice', function () {
    beforeEach(function () {
      let devicesServicePromise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'save').and.returnValue(devicesServicePromise);
      spyOn($state, 'go');
      $stateParams = {};
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCtrl', serviceInjection);
      controller.currentDevice.panelModel = {id: 'Sony-112'};
      controller.currentDevice.panelInput = {id: 'HDMI1', parentId: 'Sony-112'};
      controller.onSaveDevice();
      return devicesServicePromise.resolve();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call DevicesService.save with the current device', () => expect(DevicesService.save).toHaveBeenCalledWith(controller.currentDevice));

    describe('.onSuccessDeviceSave', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onSuccessDeviceSave();
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it("displays a success toast", () => expect(ToastsService.showSuccessToast).toHaveBeenCalledWith('We saved your update.'));
    });

    return describe('.onFailureDeviceSave', function () {
      beforeEach(function () {
        spyOn($log, 'info');
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return spyOn(ToastsService, 'showErrorToast');
      });

      it('stops the progress bar', function () {
        controller.onFailureDeviceSave({status: 200});
        return expect(progressBarService.complete).toHaveBeenCalled();
      });

      it('displays a sweet alert when the customer display code has already been used for the tenant', function () {
        controller.onFailureDeviceSave({status: 409, statusText: 'Conflict'});
        return expect(sweet.show).toHaveBeenCalledWith('Oops...',
          'This customer display code already exists for this tenant. Please choose another.', 'error');
      });

      it('logs info to the console when the customer display code has already been used for the tenant', function () {
        controller.onFailureDeviceSave({status: 409, statusText: 'Conflict'});
        let infoMessage = 'Failure saving device. Customer display code already exists for tenant: 409 Conflict';
        return expect($log.info).toHaveBeenCalledWith(infoMessage);
      });

      it('displays a toast for general save failure', function () {
        controller.onFailureDeviceSave({status: 400, statusText: 'Bad Request'});
        return expect(ToastsService.showErrorToast).toHaveBeenCalledWith(
          'Oops. We were unable to save your updates to this device at this time.');
      });

      return it('logs a detailed error to the console for a general save failure', function () {
        controller.onFailureDeviceSave({status: 400, statusText: 'Bad Request'});
        return expect($log.error).toHaveBeenCalledWith('Failure saving device: 400 Bad Request');
      });
    });
  });

  describe('.confirmDeviceDelete', function () {
    let jquery_event = {};
    let device_key = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHIbCxIOQ2hyb21lT3NEZXZpY2UYgICAgICAhggM';
    let confirm = undefined;
    let promise = undefined;

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn($mdDialog, 'confirm').and.callFake(() => 'ok');
      spyOn($mdDialog, 'show').and.returnValue(promise);
      confirm = $mdDialog.confirm(
        {
          title: 'Are you sure to delete this device?',
          textContent: 'Please remember, you MUST remove this device from Content Manager before deleting it from Provisioning.',
          targetEvent: event,
          ok: 'Delete',
          cancel: 'Cancel'
        }
      );
      return controller = $controller('DeviceDetailsCtrl', serviceInjection);
    });

    it('calls $mdDialog.show confirm object', function () {
      controller.confirmDeviceDelete(jquery_event, device_key);
      return expect($mdDialog.show).toHaveBeenCalledWith(confirm);
    });

    it('calls controller.onConfirmDelete when promise resolved', function () {
      spyOn(controller, 'onConfirmDelete');
      controller.confirmDeviceDelete(jquery_event, device_key);
      let confirmResponse = [{result: 'ok'}];
      promise.resolve(confirmResponse);
      return expect(controller.onConfirmDelete).toHaveBeenCalledWith(device_key);
    });

    return it('calls controller.onConfirmCancel when promise rejected', function () {
      spyOn(controller, 'onConfirmCancel');
      controller.confirmDeviceDelete(jquery_event, device_key);
      promise.reject([]);
      return expect(controller.onConfirmCancel).toHaveBeenCalled();
    });
  });

  describe('.onConfirmDelete', function () {
    let device_key = 'ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHIbCxIOQ2hyb21lT3NEZXZpY2UYgICAgICAhggM';
    let promise = undefined;

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'delete').and.returnValue(promise);
      spyOn(sweet, 'show');
      spyOn(ToastsService, 'showSuccessToast');
      spyOn(ToastsService, 'showErrorToast');
      spyOn($state, 'go');
      spyOn($log, 'error');
      return controller = $controller('DeviceDetailsCtrl', serviceInjection);
    });

    describe('when promise is resolved', function () {
      it('calls DevicesService.delete with device key', function () {
        controller.onConfirmDelete(device_key);
        return expect(DevicesService.delete).toHaveBeenCalledWith(device_key);
      });

      it('displays a toast confirming that the delete request was processed', function () {
        controller.onConfirmDelete(device_key);
        promise.resolve();
        return expect(ToastsService.showSuccessToast).toHaveBeenCalledWith('We processed your delete request.');
      });

      return it('calls $state router', function () {
        controller.onConfirmDelete(device_key);
        promise.resolve();
        return expect($state.go).toHaveBeenCalledWith('devices');
      });
    });

    return describe('when promise is rejected', function () {
      it('display an error toast with a friendly message about delete failure', function () {
        controller.onConfirmDelete(device_key);
        promise.reject([]);
        return expect(ToastsService.showErrorToast).toHaveBeenCalledWith(
          'We were unable to complete your delete request at this time.');
      });

      return it('logs a detailed error to the console', function () {
        let response = {status: 400, statusText: 'Bad request'};
        controller.onConfirmDelete(device_key);
        promise.reject(response);
        return expect($log.error).toHaveBeenCalledWith(`Delete device failure for device_key ${device_key}: 400 Bad request`);
      });
    });
  });

  describe('.onConfirmCancel', function () {
    beforeEach(function () {
      spyOn(ToastsService, 'showInfoToast');
      controller = $controller('DeviceDetailsCtrl', serviceInjection);
      return controller.onConfirmCancel();
    });

    return it('displays a toast indicating delete request was canceled', () => expect(ToastsService.showInfoToast).toHaveBeenCalledWith('We canceled your delete request.'));
  });

  describe('.onProofOfPlayLoggingCheck', function () {
    beforeEach(() => controller = $controller('DeviceDetailsCtrl', serviceInjection));

    describe('proof of play logging is true with a location specified', function () {
      beforeEach(function () {
        spyOn(controller, 'onSaveDevice');
        controller.currentDevice.proofOfPlayLogging = true;
        controller.currentDevice.locationKey = 'ah1kZXZ-c2t5a2l0LW';
        return controller.onProofOfPlayLoggingCheck();
      });

      return it('saves proof of play is true on the device entity', () => expect(controller.onSaveDevice).toHaveBeenCalled());
    });

    describe('proof of play logging is true with no Location specified', function () {
      beforeEach(function () {
        spyOn(sweet, 'show');
        controller.currentDevice.proofOfPlayLogging = true;
        controller.currentDevice.locationKey = null;
        return controller.onProofOfPlayLoggingCheck();
      });

      it('displays a sweet alert indicating a location is needed to enable Proof of Play', () =>
        expect(sweet.show).toHaveBeenCalledWith('Oops...',
          "You must have a Location to enable Proof of play.", 'error')
      );

      return it('set proofOfPlayLogging to false since the location pre-condition is not met', () => expect(controller.currentDevice.proofOfPlayLogging).toBe(false));
    });

    describe('proof of play logging is true with no Display code specified', function () {
      beforeEach(function () {
        spyOn(sweet, 'show');
        controller.currentDevice.proofOfPlayLogging = true;
        controller.currentDevice.locationKey = 'ah1kZXZ-c2t5a2l0LW';
        controller.currentDevice.customerDisplayCode = null;
        return controller.onProofOfPlayLoggingCheck();
      });

      it('displays a sweet alert indicating a Display code is needed to enable Proof of Play', () =>
        expect(sweet.show).toHaveBeenCalledWith('Oops...',
          "You must have a Display code to enable Proof of play.", 'error')
      );

      return it('set proofOfPlayLogging to false since the location pre-condition is not met', () => expect(controller.currentDevice.proofOfPlayLogging).toBe(false));
    });

    return describe('proof of play logging is false', function () {
      beforeEach(function () {
        spyOn(controller, 'onSaveDevice');
        controller.currentDevice.proofOfPlayLogging = false;
        return controller.onProofOfPlayLoggingCheck();
      });

      return it('saves proof of play is false on the device entity', () => expect(controller.onSaveDevice).toHaveBeenCalled());
    });
  });

  describe('.onUpdateLocation', function () {
    beforeEach(function () {
      controller = $controller('DeviceDetailsCtrl', serviceInjection);
      spyOn(controller, 'onSaveDevice');
      return controller.onUpdateLocation();
    });

    return it('saves proof of play on the device entity', () => expect(controller.onSaveDevice).toHaveBeenCalled());
  });


  describe('.onClickRefreshButton', function () {
    beforeEach(function () {
      let devicesServicePromise = new skykitProvisioning.q.Mock();
      spyOn(DevicesService, 'getIssuesByKey').and.returnValue(getDeviceIssuesPromise);
      spyOn(progressBarService, 'start');
      $stateParams.deviceKey = 'fkasdhfjfa9s8udyva7dygoudyg';
      controller = $controller('DeviceDetailsCtrl', {
        $stateParams,
        $state,
        DevicesService,
        ProgressBarService: progressBarService
      });
      controller.prev_cursor = null;
      controller.next_cursor = null;
      return controller.onClickRefreshButton();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    it('defines epochStart', () => expect(controller.epochStart).toBeDefined());

    it('defines epochEnd', () => expect(controller.epochEnd).toBeDefined());


    it('calls service to refresh issues for a given device within a specified datetime range', () =>
      expect(DevicesService.getIssuesByKey).toHaveBeenCalledWith(
        $stateParams.deviceKey, controller.epochStart, controller.epochEnd, controller.prev_cursor, controller.next_cursor)
    );

    describe('.onRefreshIssuesSuccess', function () {
      beforeEach(function () {
        spyOn(progressBarService, 'complete');
        return controller.onRefreshIssuesSuccess(issues);
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it('populates the issues array with two records', () => expect(controller.issues.length).toBe(2));
    });

    return describe('.onRefreshIssuesFailure', function () {
      let error = {status: 403, statusText: 'Forbidden'};

      beforeEach(function () {
        spyOn(progressBarService, 'complete');
        spyOn(ToastsService, 'showInfoToast');
        spyOn($log, 'error');
        return controller.onRefreshIssuesFailure(error);
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a toast with error information', () =>
        expect(ToastsService.showInfoToast).toHaveBeenCalledWith(
          'We were unable to refresh the device issues list at this time.')
      );

      return it('logs a detailed error to the console for failure to refresh issues', () =>
        expect($log.error).toHaveBeenCalledWith(
          `Failure to refresh device issues: ${error.status } ${error.statusText}`)
      );
    });
  });

  describe('.autoGenerateCustomerDisplayCode', function () {
    beforeEach(() => controller = $controller('DeviceDetailsCtrl', {}));

    return it('generates a new customer display code', function () {
      controller.currentDevice.customerDisplayName = 'Panel in Reception';
      controller.autoGenerateCustomerDisplayCode();
      return expect(controller.currentDevice.customerDisplayCode).toBe('panel_in_reception');
    });
  });

  describe('isAgostoDomain', function () {
    beforeEach(() => controller = $controller('DeviceDetailsCtrl', {StorageService}));

    it('is a valid domain if @demo.agosto.com', function () {
      StorageService.set("userEmail", "some.user@demo.agosto.com");
      return expect(controller.logglyForUser()).toBeTruthy();
    });


    return it('is not if anything else', function () {
      StorageService.set("userEmail", "some.user@123.com");
      return expect(controller.logglyForUser()).toBeFalsy();
    });
  });

  describe('.copyDeviceKey', function () {
    beforeEach(function () {
      controller = $controller('DeviceDetailsCtrl', {ToastsService});
      spyOn(ToastsService, 'showSuccessToast');
      return controller.copyDeviceKey();
    });

    return it('is shows a success toast', () => expect(ToastsService.showSuccessToast).toHaveBeenCalledWith('Device key copied to your clipboard'));
  });

  return describe('.copyCorrelationIdentifier', function () {
    beforeEach(function () {
      controller = $controller('DeviceDetailsCtrl', {ToastsService});
      spyOn(ToastsService, 'showSuccessToast');
      return controller.copyCorrelationIdentifier();
    });

    return it('is shows a success toast', () =>
      expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
        'Correlation ID copied to your clipboard')
    );
  });
});
