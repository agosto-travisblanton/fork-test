angular.module 'skykitDisplayDeviceManagement', [
  'ngAnimate',
  'ngCookies',
  'ngTouch',
  'ngSanitize',
  'ngMaterial',
  'restangular',
  'ui.router',
  'ui.bootstrap',
  'hSweetAlert'
]
  .config ($stateProvider, $urlRouterProvider) ->
    $stateProvider
      .state "home",
        url: "/",
        templateUrl: "app/main/main.html",
        controller: "MainCtrl"

    $urlRouterProvider.otherwise '/'

