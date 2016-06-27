angular.module('skykitProvisioning').factory('TimezonesService', function($http, $log, Restangular) {
  class TimezonesService {
    constructor() {}

    getUsTimezones() {
      let promise = Restangular.oneUrl('timezones', 'api/v1/timezones/us').get();
      return promise;
    }

    getAllTimezones() {
      let promise = Restangular.oneUrl('timezones', 'api/v1/timezones/all').get();
      return promise;
    }

    getCustomTimezones() {
      let promise = Restangular.oneUrl('timezones', 'api/v1/timezones/custom').get();
      return promise;
    }
  }

  return new TimezonesService();
});
