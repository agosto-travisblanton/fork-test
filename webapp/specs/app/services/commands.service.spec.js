describe('CommandsService', function () {
  let CommandsService = undefined;
  let Restangular = undefined;
  let promise = undefined;
  let $cookies = undefined;
  let userEmail = 'bob.macneal@agosto.com';
  let key = 'l0eUdyb3VwDAsSBlRlbmFudBiAgICAgMCvCgw';
  let payload = {
    userIdentifier: userEmail
  };

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_CommandsService_, _Restangular_, _$cookies_) {
    CommandsService = _CommandsService_;
    Restangular = _Restangular_;
    $cookies = _$cookies_;
    promise = new skykitProvisioning.q.Mock();
    return spyOn($cookies, 'get').and.returnValue(userEmail);
  }));

  describe('.reset', () =>
    it('prepares a device reset command, returning a promise', function () {
      let commandsRestangularService = {
        post() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'post').and.returnValue(promise);
      let actual = CommandsService.reset(key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}/commands/reset`);
      expect(commandsRestangularService.post).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.powerOn', () =>
    it('prepares a power on command, returning a promise', function () {
      let commandsRestangularService = {
        post() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'post').and.returnValue(promise);
      let actual = CommandsService.powerOn(key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}/commands/power-on`);
      expect(commandsRestangularService.post).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.powerOff', () =>
    it('prepares a power on command, returning a promise', function () {
      let commandsRestangularService = {
        post() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'post').and.returnValue(promise);
      let actual = CommandsService.powerOff(key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}/commands/power-off`);
      expect(commandsRestangularService.post).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.toggleDiagnostics', () =>
    it('prepares a toggle diagnostics command, returning a promise', function () {
      let commandsRestangularService = {
        post() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'post').and.returnValue(promise);
      let actual = CommandsService.toggleDiagnostics(key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}/commands/diagnostics`);
      expect(commandsRestangularService.post).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.restart', () =>
    it('prepares a restart command, returning a promise', function () {
      let commandsRestangularService = {
        post() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'post').and.returnValue(promise);
      let actual = CommandsService.restart(key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}/commands/restart`);
      expect(commandsRestangularService.post).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.postLog', () =>
    it('prepares a post log command, returning a promise', function () {
      let commandsRestangularService = {
        post() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'post').and.returnValue(promise);
      let actual = CommandsService.postLog(key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}/commands/post-log`);
      expect(commandsRestangularService.post).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.contentDelete', () =>
    it('prepares a content delete command, returning a promise', function () {
      let commandsRestangularService = {
        post() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'post').and.returnValue(promise);
      let actual = CommandsService.contentDelete(key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}/commands/content-delete`);
      expect(commandsRestangularService.post).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  describe('.volume', () =>
    it('prepares a device volume command, returning a promise', function () {
      let commandsRestangularService = {
        customPOST() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'customPOST').and.returnValue(promise);
      let volume = 6;
      payload = {
        volume
      };
      let actual = CommandsService.volume(key, volume);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}`);
      expect(commandsRestangularService.customPOST).toHaveBeenCalledWith(payload, 'commands/volume');
      return expect(actual).toBe(promise);
    })
  );

  return describe('.custom', () =>
    it('prepares a device custom command, returning a promise', function () {
      let commandsRestangularService = {
        customPOST() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(commandsRestangularService);
      spyOn(commandsRestangularService, 'customPOST').and.returnValue(promise);
      let update_something = 'skykit.com/skdchromeapp/update/something';
      payload = {
        command: update_something
      };
      let actual = CommandsService.custom(key, update_something);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('devices', `api/v1/devices/${key}`);
      expect(commandsRestangularService.customPOST).toHaveBeenCalledWith(payload, 'commands/custom');
      return expect(actual).toBe(promise);
    })
  );
});

