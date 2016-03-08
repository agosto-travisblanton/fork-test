'use strict'

app = angular.module 'skykitProvisioning'

app.run ($cookies, Restangular) ->
  Restangular.addRequestInterceptor (elem, operation) ->
    authToken = '6C346588BD4C6D722A1165B43C51C'
    if $location.host().indexOf('-gamestop') > -1
      authToken ='5XZHBF3mOwqJlYAlG1NeeWX0Cb72g'
    Restangular.setDefaultHeaders {
      'Content-Type': 'application/json'
      'Accept': 'application/json'
      'Authorization': authToken
      'X-Provisioning-User': $cookies.get('userKey')
      'X-Provisioning-Distributor': $cookies.get('currentDistributorKey')
    }
    if operation == 'remove'
      return undefined
    elem
