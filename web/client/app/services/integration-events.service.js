export default class IntegrationEvents {

  constructor(Restangular) {
    this.Restangular = Restangular
    this.ENROLLMENT_EVENTS = 'integration_events/enrollment';
  }

  getEnrollmentEvents(deviceKey) {
    let query = {
      deviceKey
    };
    return this.Restangular.all(this.ENROLLMENT_EVENTS).customGET('', query);
  }

  static integrationEventsServiceFactory(Restangular) {
    return new IntegrationEvents(Restangular)
  }
}

IntegrationEvents.integrationEventsServiceFactory.$inject = [
  "Restangular",
]


