'use strict'

skykitDisplayDeviceManagement = angular.module('skykitDisplayDeviceManagement', [
  'ngAnimate',
  'ngCookies',
  'ngTouch',
  'ngSanitize',
  'restangular',
  'ui.router',
  'hSweetAlert',
  'ui.bootstrap'
])

skykitDisplayDeviceManagement.config ($stateProvider, $urlRouterProvider, RestangularProvider) ->
  $stateProvider.state("home", {url: "/", templateUrl: "app/main/main.html", controller: "MainCtrl"})
  $stateProvider.state("domain", {url: "/domain", templateUrl: "app/domain/domain.html", controller: "DomainCtrl"})
  $stateProvider.state("deviceEdit", {
    url: "/deviceEdit",
    templateUrl: "app/device/device.editor.html",
    controller: "DeviceEditorCtrl",
    controllerAs: 'deviceEdit'
  })
  $stateProvider.state("tenants", {
    url: "/tenants",
    templateUrl: "app/tenant/tenants.html",
    controller: "TenantsCtrl",
    controllerAs: 'tenantsCtrl'
  })
  $stateProvider.state("newTenant", {
    url: "/tenants/new",
    templateUrl: "app/tenant/tenant-detail.html",
    controller: "TenantDetailsCtrl",
    controllerAs: 'tenantDetailsCtrl'
  })
  $stateProvider.state("editTenant", {
    url: "/tenants/:tenantKey",
    templateUrl: "app/tenant/tenant-detail.html",
    controller: "TenantDetailsCtrl",
    controllerAs: 'tenantDetailsCtrl'
  })
  $stateProvider.state("editDevice", {
    url: "/devices/:deviceKey",
    templateUrl: "app/device/device-detail.html",
    controller: "DeviceDetailsCtrl",
    controllerAs: 'deviceDetailsCtrl'
  })
  $stateProvider.state("apiTest", {
    url: "/api_testing",
    templateUrl: "app/api_test/api_test.html",
    controller: "ApiTestCtrl",
    controllerAs: 'apiTest'
  })
  $stateProvider.state("remote_control", {
    url: "/remote_control",
    templateUrl: "app/remote_control/index.html",
    controller: "RemoteControlCtrl",
    controllerAs: 'remoteControlCtrl'
  })
  $urlRouterProvider.otherwise '/'

  RestangularProvider.setBaseUrl '/api/v1'

  RestangularProvider.setDefaultHeaders {
    'Content-Type': 'application/json'
    'Accept': 'application/json'
    'Authorization': '6C346588BD4C6D722A1165B43C51C'
  }

  RestangularProvider.addRequestInterceptor (elem, operation) ->
    if operation == 'remove'
      return undefined
    elem

  RestangularProvider.setRestangularFields {
    id: 'key'
  }
