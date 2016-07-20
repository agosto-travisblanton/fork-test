export default class TimezonesService {
  /*@ngInject*/
  constructor(Restangular) {
    this.Restangular = Restangular
  }

  getUsTimezones() {
    let promise = this.Restangular.oneUrl('timezones', 'api/v1/timezones/us').get();
    return promise;
  }

  getAllTimezones() {
    let promise = this.Restangular.oneUrl('timezones', 'api/v1/timezones/all').get();
    return promise;
  }

  getCustomTimezones() {
    let promise = this.Restangular.oneUrl('timezones', 'api/v1/timezones/custom').get();
    return promise;
  }

  static create(Restangular) {
    return new TimezonesService(Restangular)
  }
}
