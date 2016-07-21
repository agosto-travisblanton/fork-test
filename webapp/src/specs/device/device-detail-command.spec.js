import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject
import moment from 'moment'



describe('DeviceDetailsCommandsCtrl', function () {
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
        elapsedTime: "37.3 minutes",
        level: 2,
        levelDescriptor: "danger",
        memoryUtilization: 40,
        program: "Test Content",
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
        controller = $controller('DeviceDetailsCommandsCtrl', {
          $stateParams,
          $state,
          DevicesService,
          ProgressBarService: progressBarService,
          TimezonesService,
          LocationsService
        });
        return controller.initialize();
      });


      it('currentDevice property should be defined', () => expect(controller.currentDevice).toBeDefined());

      it('commandEvents array should be defined', () => expect(controller.commandEvents).toBeDefined());


    });

    return describe('edit mode', function () {
      beforeEach(function () {
        $stateParams = {
          deviceKey: 'fkasdhfjfa9s8udyva7dygoudyg',
          tenantKey: 'tkasdhfjfa9s2udyva5digopdy0'
        };
        controller = $controller('DeviceDetailsCommandsCtrl', {
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


      it('defines currentDevice property', () => expect(controller.currentDevice).toBeDefined());

      it('calls DevicesService.getByKey to retrieve the selected device', () => expect(DevicesService.getDeviceByKey).toHaveBeenCalledWith($stateParams.deviceKey));

      it('calls DevicesService.getCommandEventsByKey to retrieve command events for device', () => expect(DevicesService.getCommandEventsByKey).toHaveBeenCalledWith($stateParams.deviceKey, undefined, undefined));


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
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.tenantKey = undefined;
      controller.selectedTimezone = "America/Chicago";
      return controller.onGetDeviceSuccess(response);
    });

    it('sets the current device', () => expect(controller.currentDevice).toBe(response));

    it('sets the selected timezone', () => expect(controller.selectedTimezone).toBe(timezone));

    it('sets the tenant key', () => expect(controller.tenantKey).toBe(tenantKey));

    describe('coming from devices', function () {
      beforeEach(function () {
        $stateParams = {fromDevices: "true"};
        controller = $controller('DeviceDetailsCommandsCtrl', {
          $stateParams
        });
        return controller.onGetDeviceSuccess(response);
      });

      return it('sets the back button text according to previous context', () => expect(controller.backUrlText).toBe('Back to devices'));
    });

    describe('coming from tenant unmanaged devices', function () {
      beforeEach(function () {
        $stateParams = {fromDevices: "false"};
        controller = $controller('DeviceDetailsCommandsCtrl', {
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
        controller = $controller('DeviceDetailsCommandsCtrl', {
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
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
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

  describe('.onResetPlayer', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'reset').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onResetPlayer();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call CommandsService.reset with the current device', () => expect(CommandsService.reset).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onResetPlayerSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onResetPlayerSuccess();
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating reset player command was sent to the player queue', function () {
        let message = "We posted your reset player command into the player's queue.";
        return expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(message);
      });
    });

    return describe('.onResetPlayerFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn($log, 'error');
        spyOn(sweet, 'show');
        return controller.onResetPlayerFailure(error);
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert indicating unable to send reset player command to the player queue', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your reset player command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () => expect($log.error).toHaveBeenCalledWith(`Reset player command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onPanelOn', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'powerOn').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onPanelOn();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call CommandsService.powerOn with the current device', () => expect(CommandsService.powerOn).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onPanelOnSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onPanelOnSuccess();
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your panel on command into the player's queue.")
      );
    });

    return describe('.onPanelOnFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onPanelOnFailure(error);
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your panel on command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () => expect($log.error).toHaveBeenCalledWith(`Panel on command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onPanelOff', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'powerOff').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onPanelOff();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call CommandsService.powerOff with the current device', () => expect(CommandsService.powerOff).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onPanelOffSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onPanelOffSuccess();
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your panel off command into the player's queue.")
      );
    });

    return describe('.onPanelOffFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onPanelOffFailure(error);
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your panel off command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () => expect($log.error).toHaveBeenCalledWith(`Panel off command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onUpdateDevice', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'updateDevice').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onUpdateDevice();
    });

    it('starts the progress bar', () => expect(progressBarService.start).toHaveBeenCalled());

    it('call CommandsService.updateDevice with the current device', () => expect(CommandsService.updateDevice).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onUpdateDeviceSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onUpdateDeviceSuccess();
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your update device command into the player's queue.")
      );
    });

    return describe('.onUpdateDeviceFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onUpdateDeviceFailure(error);
      });

      it('stops the progress bar', () => expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your update device command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () => expect($log.error).toHaveBeenCalledWith(`Update device command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onDiagnosticsToggle', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'toggleDiagnostics').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onDiagnosticsToggle();
    });

    it('starts the progress bar', () =>
      expect(progressBarService.start).toHaveBeenCalled());

    it('call CommandsService.toggleDiagnostics with the current device', () =>
      expect(CommandsService.toggleDiagnostics).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onToggleDiagnosticsSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onToggleDiagnosticsSuccess();
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your diagnostics command into the player's queue.")
      );
    });

    return describe('.onToggleDiagnosticsFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onToggleDiagnosticsFailure(error);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your diagnostics command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () =>
        expect($log.error).toHaveBeenCalledWith(
          `Diagnostics command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onRestart', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'restart').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onRestart();
    });

    it('starts the progress bar', () =>
      expect(progressBarService.start).toHaveBeenCalled());

    it('call CommandsService.restart with the current device', () =>
      expect(CommandsService.restart).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onRestartSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onRestartSuccess();
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your restart command into the player's queue.")
      );
    });

    return describe('.onRestartFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onRestartFailure(error);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your restart command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () =>
        expect($log.error).toHaveBeenCalledWith(
          `Restart command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onPostLog', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'postLog').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onPostLog();
    });

    it('starts the progress bar', () =>
      expect(progressBarService.start).toHaveBeenCalled());

    it('call CommandsService.postLog with the current device', () =>
      expect(CommandsService.postLog).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onPostLogSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onPostLogSuccess();
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your post log command into the player's queue.")
      );
    });

    return describe('.onPostLogFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onPostLogFailure(error);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your post log command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () =>
        expect($log.error).toHaveBeenCalledWith(
          `Post log command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onVolumeChange', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'volume').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      controller.currentDevice.volume = 5;
      return controller.onVolumeChange();
    });

    it('starts the progress bar', () =>
      expect(progressBarService.start).toHaveBeenCalled());

    it('calls CommandsService.volume with the current device', () =>
      expect(CommandsService.volume).toHaveBeenCalledWith(controller.currentDevice.key,
        controller.currentDevice.volume));

    describe('.onVolumeChangeSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onVolumeChangeSuccess(controller.currentDevice.volume);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating volume command was sent to the player queue', function () {
        let message = `We posted your volume change command of ${controller.currentDevice.volume} into the player's queue.`;
        return expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(message);
      });
    });

    return describe('.onVolumeChangeFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn($log, 'error');
        spyOn(sweet, 'show');
        return controller.onVolumeChangeFailure(error);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert indicating unable to send volume change command to the player queue', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your volume change command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () =>
        expect($log.error).toHaveBeenCalledWith(`Volume change command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onCustomCommand', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'custom').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      controller.currentDevice.custom = 'skykit.com/skdchromeapp/channel/2';
      return controller.onCustomCommand();
    });

    it('starts the progress bar', () =>
      expect(progressBarService.start).toHaveBeenCalled());

    it('calls CommandsService.custom with the current device', () =>
      expect(CommandsService.custom).toHaveBeenCalledWith(controller.currentDevice.key, controller.currentDevice.custom));

    describe('.onCustomCommandSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onCustomCommandSuccess(controller.currentDevice.custom);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating custom command was sent to the player queue', function () {
        let message = `We posted your custom command '${controller.currentDevice.custom}' into the player's queue.`;
        return expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(message);
      });
    });

    return describe('.onCustomCommandFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onCustomCommandFailure(error);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert indicating unable to custom command to the player queue', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your custom command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () =>
        expect($log.error).toHaveBeenCalledWith(`Custom command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onResetContent', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'contentDelete').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onResetContent();
    });

    it('starts the progress bar', () =>
      expect(progressBarService.start).toHaveBeenCalled());

    it('calls CommandsService.contentDelete with the current device', () =>
      expect(CommandsService.contentDelete).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onResetContentSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onResetContentSuccess();
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your reset content command into the player's queue.")
      );
    });

    return describe('.onResetContentFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onResetContentFailure(error);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your reset content command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () =>
        expect($log.error).toHaveBeenCalledWith(`Reset content command error: ${error.status} ${error.statusText}`));
    });
  });

  describe('.onUpdateContent', function () {
    beforeEach(function () {
      commandsServicePromise = new skykitProvisioning.q.Mock();
      spyOn(CommandsService, 'contentUpdate').and.returnValue(commandsServicePromise);
      spyOn(progressBarService, 'start');
      spyOn(progressBarService, 'complete');
      controller = $controller('DeviceDetailsCommandsCtrl', serviceInjection);
      controller.editMode = true;
      return controller.onUpdateContent();
    });

    it('starts the progress bar', () =>
      expect(progressBarService.start).toHaveBeenCalled());

    it('calls CommandsService.contentUpdate with the current device', () =>
      expect(CommandsService.contentUpdate).toHaveBeenCalledWith(controller.currentDevice.key));

    describe('.onUpdateContentSuccess', function () {
      beforeEach(function () {
        spyOn(ToastsService, 'showSuccessToast');
        return controller.onUpdateContentSuccess();
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      return it('displays a toast indicating command was sent to player', () =>
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
          "We posted your update content command into the player's queue.")
      );
    });

    return describe('.onUpdateContentFailure', function () {
      let error = {status: 404, statusText: 'Not Found'};

      beforeEach(function () {
        spyOn(sweet, 'show');
        spyOn($log, 'error');
        return controller.onUpdateContentFailure(error);
      });

      it('stops the progress bar', () =>
        expect(progressBarService.complete).toHaveBeenCalled());

      it('displays a sweet alert', () =>
        expect(sweet.show).toHaveBeenCalledWith(
          'Oops...', "We were unable to post your update content command into the player's queue.", 'error')
      );

      return it('logs a detailed error to the console', () =>
        expect($log.error).toHaveBeenCalledWith(`Content update command error: ${error.status} ${error.statusText}`));
    });
  });


});
