angular.module('skykitProvisioning').factory('IntegrationEvents', Restangular =>
  new class IntegrationEvents {

    constructor() {
      this.ENROLLMENT_EVENTS = 'integration_events/enrollment';
    }

    getEnrollmentEvents(deviceKey) {
      let query = {
        deviceKey
      };
      return Restangular.all(this.ENROLLMENT_EVENTS).customGET('', query);
    }
  }()
);
