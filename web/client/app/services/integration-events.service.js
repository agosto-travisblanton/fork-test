export default class IntegrationEvents {
/*@ngInject*/
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

  static create(Restangular) {
    return new IntegrationEvents(Restangular)
  }
}



