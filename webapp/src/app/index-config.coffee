'use strict'

app = angular.module 'skykitProvisioning'

app.config ($stateProvider, $urlRouterProvider, RestangularProvider) ->
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
      label: 'Skykit Provisioning'
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
      label: 'Skykit Provisioning'
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
    templateUrl: "app/tenant/tenants-listing.html",
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

  RestangularProvider.addResponseInterceptor (data, operation, resourceType, url, response, deferred) ->
    result = data
    # Uncomment this for pagination support when using PagingListHandlerMixin on the Python side.
    #    if resourceType == 'devices' and operation = 'getList' and url == '/api/v1/devices'
    #      result = data.objects
    result

  RestangularProvider.setRestangularFields {
    id: 'key'
  }
