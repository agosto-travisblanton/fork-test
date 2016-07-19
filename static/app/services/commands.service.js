angular.module('skykitProvisioning').factory('CommandsService', Restangular =>
  new class CommandsService {

    constructor() {
      this.SERVICE_NAME = 'devices';
    }

    reset(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/reset`).post();
      return promise;
    }

    contentDelete(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/content-delete`).post();
      return promise;
    }

    contentUpdate(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/content-update`).post();
      return promise;
    }

    updateDevice(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/refresh-device-representation`).post();
      return promise;
    }

    toggleDiagnostics(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/diagnostics`).post();
      return promise;
    }

    restart(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/restart`).post();
      return promise;
    }

    postLog(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/post-log`).post();
      return promise;
    }

    powerOn(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/power-on`).post();
      return promise;
    }

    powerOff(key) {
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/power-off`).post();
      return promise;
    }

    volume(key, volume) {
      let payload = {
        volume
      };
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}`).customPOST(payload, 'commands/volume');
      return promise;
    }

    custom(key, command) {
      let payload = {
        command
      };
      let promise = Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}`).customPOST(payload, 'commands/custom');
      return promise;
    }
  }()
);
