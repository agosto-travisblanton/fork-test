'use strict'

skykitDisplayDeviceManagement = angular.module('skykitDisplayDeviceManagement', [
  'ngAnimate',
  'ngCookies',
  'ngTouch',
  'ngSanitize',
  'restangular',
  'ui.router',
  'hSweetAlert'
])


skykitDisplayDeviceManagement.config ($stateProvider, $urlRouterProvider) ->
  $stateProvider.state("home", {url: "/", templateUrl: "app/main/main.html", controller: "MainCtrl"})
  $stateProvider.state("domain", {url: "/domain", templateUrl: "app/domain/domain.html", controller: "DomainCtrl"})
  $stateProvider.state("deviceEdit", {
    url: "/deviceEdit",
    templateUrl: "app/device/device.editor.html",
    controller: "DeviceEditorCtrl",
    controllerAs: 'deviceEdit'
  })
  $stateProvider.state("apiTest", {
    url: "/api_testing",
    templateUrl: "app/api_test/api_test.html",
    controller: "ApiTestCtrl",
    controllerAs: 'apiTest'
  })
  $urlRouterProvider.otherwise '/'


skykitDisplayDeviceManagement.config (RestangularProvider) ->
  RestangularProvider.setBaseUrl '/api'
  RestangularProvider.setDefaultHeaders {
    'Content-Type': 'application/json'
    'Accept': 'application/json'
  }
