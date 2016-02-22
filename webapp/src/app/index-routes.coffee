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
  $stateProvider.state("tenantDetails", {
    url: "/tenants2/:tenantKey/details",
    templateUrl: "app/tenant/tenant.html",
    controller: "TenantCtrl",
    controllerAs: 'tenantCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("tenantManagedDevices", {
    url: "/tenants2/:tenantKey/managed",
    templateUrl: "app/tenant/tenant-managed-devices.html",
    controller: "TenantManagedDevicesCtrl",
    controllerAs: 'tenantManagedDevicesCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantManagedDevicesCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("tenantUnmanagedDevices", {
    url: "/tenants2/:tenantKey/unmanaged",
    templateUrl: "app/tenant/tenant-unmanaged-devices.html",
    controller: "TenantUnmanagedDevicesCtrl",
    controllerAs: 'tenantUnmanagedDevicesCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantUnmanagedDevicesCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("tenantLocations", {
    url: "/tenants2/:tenantKey/locations",
    templateUrl: "app/tenant/tenant-locations.html",
    controller: "TenantLocationsCtrl",
    controllerAs: 'tenantLocationsCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantLocationsCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
#  .state('tabs.player', {
#    url: '/player',
#    data: {
#      'selectedTab': 0
#    },
#    views: {
#      'player': {
#        controller: playerController
#      }
#    }
#  })

#  $stateProvider.state("view1", {
#    url: "/tenants/:tenantKey/details",
#    templateUrl: "app/tenant/partials/details.html",
#  })
#  $stateProvider.state("view2", {
#    url: "/tenants/:tenantKey/locations",
#    templateUrl: "app/tenant/partials/locations.html",
#  })
#  $stateProvider.state("view3", {
#    url: "/tenants/:tenantKey/managed",
#    templateUrl: "app/tenant/partials/managed.html",
#  })
#  $stateProvider.state("view4", {
#    url: "/tenants/:tenantKey/unmanaged",
#    templateUrl: "app/tenant/partials/unmanaged.html",
#  })


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
  $stateProvider.state("proof", {
    url: "/proof",
    templateUrl: "app/proof/index.html",
    controller: "ProofOfPlayCtrl",
    controllerAs: 'vm',
    ncyBreadcrumb: {
      label: 'Proof of Play'
    }
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
