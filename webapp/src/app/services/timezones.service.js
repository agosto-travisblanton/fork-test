export default class TimezonesService {
  constructor(Restangular) {
    'ngInject';
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
}


