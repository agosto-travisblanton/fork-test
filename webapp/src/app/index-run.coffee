'use strict'

app = angular.module 'skykitProvisioning'

app.run ($cookies, Restangular) ->
  Restangular.addRequestInterceptor (elem, operation) ->
    Restangular.setDefaultHeaders {
      'Content-Type': 'application/json'
      'Accept': 'application/json'
      'Authorization': '6C346588BD4C6D722A1165B43C51C'
      'X-Provisioning-User': $cookies.get('userKey')
      'X-Provisioning-Distributor': $cookies.get('currentDistributorKey')
    }
    if operation == 'remove'
      return undefined
    elem
