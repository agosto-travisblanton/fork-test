export default class IntegrationEvents {

  constructor(Restangular) {
    'ngInject';
    this.Restangular = Restangular
    this.CREATE_TENANT_EVENTS = 'integration_events/tenant_create';
    this.ENROLLMENT_EVENTS = 'integration_events/enrollment';
  }

   getTenantCreateEvents(tenantKey) {
    let query = {
      tenantKey
    };
    return this.Restangular.all(this.CREATE_TENANT_EVENTS).customGET('', query);
  }

  getEnrollmentEvents(deviceKey) {
    let query = {
      deviceKey
    };
    return this.Restangular.all(this.ENROLLMENT_EVENTS).customGET('', query);
  }
}
