'use strict'

skykitDisplayDeviceManagement = angular.module('skykitDisplayDeviceManagement', [
  'ngAnimate',
  'ngCookies',
  'ngTouch',
  'ngSanitize',
  'restangular',
  'ui.router',
  'hSweetAlert',
  'ui.bootstrap',
  'ncy-angular-breadcrumb',
  'directive.g+signin'
])

skykitDisplayDeviceManagement.config ($stateProvider, $urlRouterProvider, RestangularProvider) ->
  $stateProvider.state("home", {
    url: "/",
    templateUrl: "app/welcome/welcome.html",
    controller: "WelcomeCtrl"
    controllerAs: 'welcomeCtrl',
    ncyBreadcrumb: {
      label: 'Home page'
    }
  })
  $stateProvider.state("welcome", {
    url: "/welcome",
    templateUrl: "app/welcome/welcome.html",
    controller: "WelcomeCtrl"
    controllerAs: 'welcomeCtrl',
    ncyBreadcrumb: {
      label: 'Home page'
    }
  })
  $stateProvider.state("domain", {
    url: "/domain",
    templateUrl: "app/domain/domain.html",
    controller: "DomainCtrl",
    ncyBreadcrumb: {
      label: 'Domains'
    }
  })
  $stateProvider.state("tenants", {
    url: "/tenants",
    templateUrl: "app/tenant/tenants.html",
    controller: "TenantsCtrl",
    controllerAs: 'tenantsCtrl',
    ncyBreadcrumb: {
      label: 'Tenants'
    }
  })
  $stateProvider.state("newTenant", {
    url: "/tenants/new",
    templateUrl: "app/tenant/tenant-detail.html",
    controller: "TenantDetailsCtrl",
    controllerAs: 'tenantDetailsCtrl',
    ncyBreadcrumb: {
      label: 'New tenant',
      parent: 'tenants'
    }
  })
  $stateProvider.state("editTenant", {
    url: "/tenants/:tenantKey",
    templateUrl: "app/tenant/tenant-detail.html",
    controller: "TenantDetailsCtrl",
    controllerAs: 'tenantDetailsCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantDetailsCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("devices", {
    url: "/devices",
    templateUrl: "app/device/devices-listing.html",
    controller: "DevicesListingCtrl",
    controllerAs: 'devicesListingCtrl',
    ncyBreadcrumb: {
      label: 'Displays'
    }
  })
  $stateProvider.state("editDevice", {
    url: "/devices/:deviceKey?tenantKey",
    templateUrl: "app/device/device-detail.html",
    ncyBreadcrumb: {
      label: '{{ deviceDetailsCtrl.currentDevice.key }}'
      parent: 'devices'
    },
    controller: 'DeviceDetailsCtrl'
    function: ($scope, $stateParams) ->
      $scope.tenantKey = $stateParams.tenantKey
      return
    controllerAs: 'deviceDetailsCtrl'
  })
  $stateProvider.state("remote_control", {
    url: "/remote_control",
    templateUrl: "app/remote_control/index.html",
    controller: "RemoteControlCtrl",
    controllerAs: 'remoteControlCtrl',
    ncyBreadcrumb: {
      label: 'Remote control'
    }
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

  RestangularProvider.addResponseInterceptor (data, operation, resourceType, url, response, deferred) ->
    result = data
    if resourceType == 'devices' and operation = 'getList' and url == '/api/v1/devices'
      result = data.objects
    result

  RestangularProvider.setRestangularFields {
    id: 'key'
  }
