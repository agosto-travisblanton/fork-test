'use strict'

angular.module('skykitProvisioning').factory 'IntegrationEvents', (Restangular) ->
  new class IntegrationEvents

    constructor: () ->
      @ENROLLMENT_EVENTS = 'integration_events/enrollment'

    getEnrollmentEvents: (deviceKey) ->
      query = {
        deviceKey: deviceKey
      }
      Restangular.all(@ENROLLMENT_EVENTS).customGET('', query)
