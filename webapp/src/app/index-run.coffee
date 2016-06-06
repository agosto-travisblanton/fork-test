'use strict'

app = angular.module 'skykitProvisioning'

app.run (StorageService, Restangular, $location, $rootScope, $state) ->
  app.constant("moment", moment)

  Restangular.addRequestInterceptor (elem, operation, what, url) ->
    authToken = '6C346588BD4C6D722A1165B43C51C'
    if $location.host().indexOf('provisioning-gamestop') > -1
      authToken = '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g'
    Restangular.setDefaultHeaders {
      'Content-Type': 'application/json'
      'Accept': 'application/json'
      'Authorization': authToken
      'X-Provisioning-User': StorageService.get('userKey')
      'X-Provisioning-Distributor': StorageService.get('currentDistributorKey')
    }
    distributorKey = StorageService.get('currentDistributorKey')
    if operation == 'remove'
      return undefined

    elem


app.factory 'RequestInterceptor', (StorageService, $location) ->
  interceptor = {
    request: (config) ->
      gs = '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g'
      prod = '6C346588BD4C6D722A1165B43C51C'
      config.headers = {
        'Content-Type': 'application/json'
        'Accept': 'application/json'
        'Authorization': if $location.host().indexOf('provisioning-gamestop') > -1 then gs else prod
        'X-Provisioning-User': StorageService.get('userKey')
        'X-Provisioning-User-Identifier': StorageService.get('userEmail')
        'X-Provisioning-Distributor': StorageService.get('currentDistributorKey')
      }
      config
  }
  interceptor


app.config ($httpProvider) ->
  $httpProvider.interceptors.push 'RequestInterceptor'
