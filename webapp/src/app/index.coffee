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
  'directive.g+signin',
  'ngProgress'
])

skykitDisplayDeviceManagement.config ($stateProvider, $urlRouterProvider, RestangularProvider) ->
  $cookies = undefined
  angular.injector([ 'ngCookies' ]).invoke (_$cookies_) ->
    $cookies = _$cookies_

  $stateProvider.state("sign_in", {
    resolve: {
      identity: (IdentityService) ->
        IdentityService.getIdentity()
    },
    url: "/sign_in",
    templateUrl: "app/authentication/sign_in.html",
    controller: "AuthenticationCtrl",
    controllerAs: 'authenticationCtrl',
  })
  $stateProvider.state("sign_out", {
    resolve: {
      identity: (IdentityService) ->
        IdentityService.getIdentity()
    },
    url: "/sign_out",
    templateUrl: "app/authentication/sign_out.html",
    controller: "AuthenticationCtrl",
    controllerAs: 'authenticationCtrl',
  })
  $stateProvider.state("distributor_selection", {
    url: "/distributor_selection",
    templateUrl: "app/distributor/distributor_selector.html",
    controller: "DistributorSelectorCtrl",
    controllerAs: 'distributorSelectorCtrl',
  })
  $stateProvider.state("home", {
    url: "/",
    templateUrl: "app/welcome/welcome.html",
    resolve: {
      identity: (IdentityService) ->
        IdentityService.getIdentity()
    },
    controller: "WelcomeCtrl",
    controllerAs: 'welcomeCtrl',
    ncyBreadcrumb: {
      label: 'Home page'
    }
  })
  $stateProvider.state("welcome", {
    url: "/welcome",
    templateUrl: "app/welcome/welcome.html",
    resolve: {
      identity: (IdentityService) ->
        IdentityService.getIdentity()
    },
    controller: "WelcomeCtrl"
    controllerAs: 'welcomeCtrl',
    ncyBreadcrumb: {
      label: 'Home page'
    }
  })
  $stateProvider.state("version", {
    url: "/version",
    templateUrl: "app/version/versions.html",
    controller: "VersionsCtrl",
    controllerAs: 'versionsCtrl',
    ncyBreadcrumb: {
      label: 'Version'
    }
  })
  $stateProvider.state("domains", {
    url: "/domains",
    templateUrl: "app/domain/domains-listing.html",
    controller: "DomainsCtrl",
    controllerAs: 'domainsCtrl',
    ncyBreadcrumb: {
      label: 'Domains'
    }
  })
  $stateProvider.state("newDomain", {
    url: "/domains/new",
    templateUrl: "app/domain/domain-detail.html",
    controller: "DomainDetailsCtrl",
    controllerAs: 'domainDetailsCtrl',
    ncyBreadcrumb: {
      label: 'New domain',
      parent: 'domains'
    }
  })
  $stateProvider.state("editDomain", {
    url: "/domains/:domainKey",
    templateUrl: "app/domain/domain-detail.html",
    controller: "DomainDetailsCtrl",
    controllerAs: 'domainDetailsCtrl',
    ncyBreadcrumb: {
      label: '{{ domainDetailsCtrl.currentDomain.name }}',
      parent: 'domains'
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
      label: 'Devices'
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
  $stateProvider.state("deviceReset", {
    url: "/devices/:deviceKey/commands/reset",
    templateUrl: "app/device/device-detail.html",
    ncyBreadcrumb: {
      label: '{{ deviceDetailsCtrl.currentDevice.key }}'
      parent: 'devices'
    },
    controller: 'DeviceDetailsCtrl'
    controllerAs: 'deviceDetailsCtrl'
  })
  $stateProvider.state("deviceVolume", {
    url: "/devices/:deviceKey/commands/volume",
    templateUrl: "app/device/device-detail.html",
    ncyBreadcrumb: {
      label: '{{ deviceDetailsCtrl.currentDevice.key }}'
      parent: 'devices'
    },
    controller: 'DeviceDetailsCtrl'
    controllerAs: 'deviceDetailsCtrl'
  })
  $stateProvider.state("deviceCustom", {
    url: "/devices/:deviceKey/commands/custom",
    templateUrl: "app/device/device-detail.html",
    ncyBreadcrumb: {
      label: '{{ deviceDetailsCtrl.currentDevice.key }}'
      parent: 'devices'
    },
    controller: 'DeviceDetailsCtrl'
    controllerAs: 'deviceDetailsCtrl'
  })

  $urlRouterProvider.otherwise '/sign_in'

  RestangularProvider.setBaseUrl '/api/v1'

  RestangularProvider.addRequestInterceptor (elem, operation) ->
    RestangularProvider.setDefaultHeaders {
      'Content-Type': 'application/json'
      'Accept': 'application/json'
      'Authorization': '6C346588BD4C6D722A1165B43C51C'
      'X-Provisioning-User': $cookies.get('userKey')
      'X-Provisioning-Distributor': $cookies.get('currentDistributorKey')
    }
    if operation == 'remove'
      return undefined
    elem

  RestangularProvider.addResponseInterceptor (data, operation, resourceType, url, response, deferred) ->
    result = data
    # Uncomment this for pagination support when using PagingListHandlerMixin on the Python side.
    #    if resourceType == 'devices' and operation = 'getList' and url == '/api/v1/devices'
    #      result = data.objects
    result

  RestangularProvider.setRestangularFields {
    id: 'key'
  }

#skykitDisplayDeviceManagement.run (IdentityService) ->
#  IdentityService.getIdentity()
