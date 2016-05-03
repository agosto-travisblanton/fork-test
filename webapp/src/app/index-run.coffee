'use strict'

app = angular.module 'skykitProvisioning'


app.config ($cookies, Restangular, $location) ->
  app.constant("moment", moment)

  Restangular.addRequestInterceptor (elem, operation, what, url) ->
    authToken = '6C346588BD4C6D722A1165B43C51C'
    if $location.host().indexOf('provisioning-gamestop') > -1
      authToken = '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g'
    Restangular.setDefaultHeaders {
      'Content-Type': 'application/json'
      'Accept': 'application/json'
      'Authorization': authToken
      'X-Provisioning-User': $cookies.get('userKey')
      'X-Provisioning-Distributor': $cookies.get('currentDistributorKey')
    }
    distributorKey = $cookies.get('currentDistributorKey')
    console.log(distributorKey)
    console.log elem
    console.log operation
    console.log what
    console.log url
    if operation == 'remove'
      return undefined

    elem

