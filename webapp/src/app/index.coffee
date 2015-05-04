angular.module 'skykitDisplayDeviceManagement', [
  'ngAnimate',
  'ngCookies',
  'ngTouch',
  'ngSanitize',
  'restangular',
  'ui.router',
  'hSweetAlert'
]
.config ($stateProvider, $urlRouterProvider) ->
  $stateProvider
  .state("home", {url: "/", templateUrl: "app/main/main.html", controller: "MainCtrl"})
  .state("domain", {url: "/domain", templateUrl: "app/domain/domain.html", controller: "DomainCtrl"})
  .state("deviceEdit",
    {
      url: "/deviceEdit",
      templateUrl: "app/device/device.editor.html",
      controller: "DeviceEditorCtrl",
      controllerAs: 'deviceEdit'
    })

  $urlRouterProvider.otherwise '/'

