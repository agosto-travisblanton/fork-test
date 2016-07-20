import 'restangular';

export default class CommandsService {
/*@ngInject*/
  constructor(Restangular) {
    this.Restangular = Restangular
    this.SERVICE_NAME = 'devices';
  }

  reset(key) {
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/reset`).post();
    return promise;
  }

  contentDelete(key) {
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/content-delete`).post();
    return promise;
  }

  contentUpdate(key) {
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/content-update`).post();
    return promise;
  }

  updateDevice(key) {
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/refresh-device-representation`).post();
    return promise;
  }

  toggleDiagnostics(key) {
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/diagnostics`).post();
    return promise;
  }

  powerOn(key) {
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/power-on`).post();
    return promise;
  }

  powerOff(key) {
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}/commands/power-off`).post();
    return promise;
  }

  volume(key, volume) {
    let payload = {
      volume
    };
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}`).customPOST(payload, 'commands/volume');
    return promise;
  }

  custom(key, command) {
    let payload = {
      command
    };
    let promise = this.Restangular.oneUrl(this.SERVICE_NAME, `api/v1/devices/${key}`).customPOST(payload, 'commands/custom');
    return promise;
  }

  static create(Restangular) {
    return new CommandsService(Restangular)
  }
}



