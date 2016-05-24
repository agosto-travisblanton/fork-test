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
  $stateProvider.state("signed_out", {
    resolve: {
      identity: (IdentityService) ->
        IdentityService.getIdentity()
    },
    url: "/signed_out",
    templateUrl: "app/authentication/signed_out.html",
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
    controllerAs: 'vm',
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
  $stateProvider.state("addDomain", {
    url: "/domains/add",
    templateUrl: "app/domain/domain-detail.html",
    controller: "DomainDetailsCtrl",
    controllerAs: 'domainDetailsCtrl',
    ncyBreadcrumb: {
      label: 'Add domain',
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
  $stateProvider.state("addTenant", {
    url: "/tenants/add",
    templateUrl: "app/tenant/tenant-add.html",
    controller: "TenantAddCtrl",
    controllerAs: 'tenantAddCtrl',
    ncyBreadcrumb: {
      label: 'Add tenant',
      parent: 'tenants'
    }
  })
  $stateProvider.state("tenantDetails", {
    url: "/tenants/:tenantKey/details",
    templateUrl: "app/tenant/tenant-details.html",
    controller: "TenantDetailsCtrl",
    controllerAs: 'tenantDetailsCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantDetailsCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("tenantManagedDevices", {
    url: "/tenants/:tenantKey/managed",
    templateUrl: "app/tenant/tenant-managed-devices.html",
    controller: "TenantManagedDevicesCtrl",
    controllerAs: 'tenantManagedDevicesCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantManagedDevicesCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("tenantUnmanagedDevices", {
    url: "/tenants/:tenantKey/unmanaged",
    templateUrl: "app/tenant/tenant-unmanaged-devices.html",
    controller: "TenantUnmanagedDevicesCtrl",
    controllerAs: 'tenantUnmanagedDevicesCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantUnmanagedDevicesCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("tenantLocations", {
    url: "/tenants/:tenantKey/locations",
    templateUrl: "app/tenant/tenant-locations.html",
    controller: "TenantLocationsCtrl",
    controllerAs: 'tenantLocationsCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantLocationsCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("editLocation", {
    url: "/locations/:locationKey",
    templateUrl: "app/tenant/tenant-location.html",
    controller: "TenantLocationCtrl",
    controllerAs: 'tenantLocationCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantLocationCtrl.tenantName }}  / {{ tenantLocationCtrl.locationName }}',
      parent: 'tenants'
    }
  })
  $stateProvider.state("addLocation", {
    url: "/tenants/:tenantKey/location",
    templateUrl: "app/tenant/tenant-location.html",
    controller: "TenantLocationCtrl",
    controllerAs: 'tenantLocationCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantLocationCtrl.tenantName }}  / Location',
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
    url: "/devices/:deviceKey?tenantKey?fromDevices",
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
    templateUrl: "app/proof/main.html",
    controller: "ProofOfPlayCtrl",
    controllerAs: 'vm',
    ncyBreadcrumb: {
      label: 'Proof of Play'
    }
  })
  $stateProvider.state("proofDetail", {
    url: "/proof/:tenant",
    templateUrl: "app/proof/detail.html",
    controller: "ProofOfPlayCtrl",
    controllerAs: 'vm',
    ncyBreadcrumb: {
      label: 'Proof of Play'
    }
  })
  $stateProvider.state("admin", {
    url: "/admin",
    templateUrl: "app/admin/main.html",
    controller: "AdminCtrl",
    controllerAs: 'vm',
    ncyBreadcrumb: {
      label: 'Admin'
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
