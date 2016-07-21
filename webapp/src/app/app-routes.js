export function routes($stateProvider, $urlRouterProvider, RestangularProvider) {
  $stateProvider.state("sign_in", {
    resolve: {
      identity(IdentityService) {
        return IdentityService.getIdentity();
      },
      notAuthenticated(AuthorizationService) {
        return AuthorizationService.notAuthenticated();
      }
    },
    url: "/sign_in",
    templateUrl: "app/authentication/sign_in.html",
    controller: "AuthenticationCtrl",
    controllerAs: 'authenticationCtrl',
  });
  $stateProvider.state("signed_out", {
    url: "/signed_out",
    resolve: {
      identity(IdentityService) {
        return IdentityService.getIdentity();
      },
      notAuthenticated(AuthorizationService) {
        return AuthorizationService.notAuthenticated();
      }
    },
    templateUrl: "app/authentication/signed_out.html",
    controller: "AuthenticationCtrl",
    controllerAs: 'authenticationCtrl',
  });
  $stateProvider.state("sign_out", {
    resolve: {
      identity(IdentityService) {
        return IdentityService.getIdentity();
      },
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/sign_out",
    templateUrl: "app/authentication/sign_out.html",
    controller: "AuthenticationCtrl",
    controllerAs: 'authenticationCtrl',
  });
  $stateProvider.state("distributor_selection", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/distributor_selection",
    templateUrl: "app/distributor/distributor_selector.html",
    controller: "DistributorSelectorCtrl",
    controllerAs: 'vm',
  });
  $stateProvider.state("home", {
    url: "/",
    templateUrl: "app/welcome/welcome.html",
    resolve: {
      identity(IdentityService) {
        return IdentityService.getIdentity();
      },
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    controller: "WelcomeCtrl",
    controllerAs: 'welcomeCtrl',
    ncyBreadcrumb: {
      label: 'Skykit Provisioning'
    }
  });
  $stateProvider.state("welcome", {
    url: "/welcome",
    templateUrl: "app/welcome/welcome.html",
    resolve: {
      identity(IdentityService) {
        return IdentityService.getIdentity();
      },
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    controller: "WelcomeCtrl",
    controllerAs: 'welcomeCtrl',
    ncyBreadcrumb: {
      label: 'Skykit Provisioning'
    }
  });
  $stateProvider.state("domains", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/domains",
    templateUrl: "app/domain/domains-listing.html",
    controller: "DomainsCtrl",
    controllerAs: 'domainsCtrl',
    ncyBreadcrumb: {
      label: 'Domains'
    }
  });
  $stateProvider.state("addDomain", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/domains/add",
    templateUrl: "app/domain/domain-detail.html",
    controller: "DomainDetailsCtrl",
    controllerAs: 'domainDetailsCtrl',
    ncyBreadcrumb: {
      label: 'Add domain',
      parent: 'domains'
    }
  });
  $stateProvider.state("editDomain", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/domains/:domainKey",
    templateUrl: "app/domain/domain-detail.html",
    controller: "DomainDetailsCtrl",
    controllerAs: 'domainDetailsCtrl',
    ncyBreadcrumb: {
      label: '{{ domainDetailsCtrl.currentDomain.name }}',
      parent: 'domains'
    }
  });
  $stateProvider.state("tenants", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/tenants",
    templateUrl: "app/tenant/tenants-listing.html",
    controller: "TenantsCtrl",
    controllerAs: 'tenantsCtrl',
    ncyBreadcrumb: {
      label: 'Tenants'
    }
  });
  $stateProvider.state("addTenant", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/tenants/add",
    templateUrl: "app/tenant/tenant-add.html",
    controller: "TenantAddCtrl",
    controllerAs: 'tenantAddCtrl',
    ncyBreadcrumb: {
      label: 'Add tenant',
      parent: 'tenants'
    }
  });
  $stateProvider.state("tenantDetails", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/tenants/:tenantKey/details",
    templateUrl: "app/tenant/tenant-details.html",
    controller: "TenantDetailsCtrl",
    controllerAs: 'tenantDetailsCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantDetailsCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  });
  $stateProvider.state("tenantManagedDevices", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/tenants/:tenantKey/managed",
    templateUrl: "app/tenant/tenant-managed-devices.html",
    controller: "TenantManagedDevicesCtrl",
    controllerAs: 'tenantManagedDevicesCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantManagedDevicesCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  });
  $stateProvider.state("tenantUnmanagedDevices", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/tenants/:tenantKey/unmanaged",
    templateUrl: "app/tenant/tenant-unmanaged-devices.html",
    controller: "TenantUnmanagedDevicesCtrl",
    controllerAs: 'tenantUnmanagedDevicesCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantUnmanagedDevicesCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  });
  $stateProvider.state("tenantLocations", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/tenants/:tenantKey/locations",
    templateUrl: "app/tenant/tenant-locations.html",
    controller: "TenantLocationsCtrl",
    controllerAs: 'tenantLocationsCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantLocationsCtrl.currentTenant.name }}',
      parent: 'tenants'
    }
  });
  $stateProvider.state("editLocation", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/locations/:locationKey",
    templateUrl: "app/tenant/tenant-location.html",
    controller: "TenantLocationCtrl",
    controllerAs: 'tenantLocationCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantLocationCtrl.tenantName }}  / {{ tenantLocationCtrl.locationName }}',
      parent: 'tenants'
    }
  });
  $stateProvider.state("addLocation", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/tenants/:tenantKey/location",
    templateUrl: "app/tenant/tenant-location.html",
    controller: "TenantLocationCtrl",
    controllerAs: 'tenantLocationCtrl',
    ncyBreadcrumb: {
      label: '{{ tenantLocationCtrl.tenantName }}  / Location',
      parent: 'tenants'
    }
  });
  $stateProvider.state("devices", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/devices",
    templateUrl: "app/device/devices-listing.html",
    controller: "DevicesListingCtrl",
    controllerAs: 'devicesListingCtrl',
    ncyBreadcrumb: {
      label: 'Devices'
    }
  });
  $stateProvider.state("editDevice", {
    resolve: {
      identity(IdentityService) {
        return IdentityService.getIdentity();
      },
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/devices/:deviceKey?tenantKey?fromDevices",
    templateUrl: "app/device/device-detail.html",
    ncyBreadcrumb: {
      label: '{{ deviceDetailsCtrl.currentDevice.key }}',
      parent: 'devices'
    },
    controller: 'DeviceDetailsCtrl',
    function($scope, $stateParams) {
      $scope.tenantKey = $stateParams.tenantKey;
      return;
    },
    controllerAs: 'deviceDetailsCtrl'
  });
  $stateProvider.state("proof", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/proof",
    templateUrl: "app/proof/main.html",
    controller: "ProofOfPlayCtrl",
    controllerAs: 'vm',
    ncyBreadcrumb: {
      label: 'Proof of Play'
    }
  });
  $stateProvider.state("proofDetail", {
    resolve: {
      authenticated(AuthorizationService) {
        return AuthorizationService.authenticated();
      }
    },
    url: "/proof/:tenant",
    templateUrl: "app/proof/detail.html",
    controller: "ProofOfPlayCtrl",
    controllerAs: 'vm',
    ncyBreadcrumb: {
      label: 'Proof of Play'
    }
  });
  $stateProvider.state("admin", {
    resolve: {
      isAdmin(AuthorizationService) {
        return AuthorizationService.isAdminOrDistributorAdmin();
      }
    },
    url: "/admin",
    templateUrl: "app/admin/admin.html",
    controller: "AdminCtrl",
    controllerAs: 'vm',
    ncyBreadcrumb: {
      label: 'Admin'
    }
  });

  $urlRouterProvider.otherwise('/sign_in');

  RestangularProvider.setBaseUrl('/api/v1');

  RestangularProvider.addResponseInterceptor(function (data, operation, resourceType, url, response, deferred) {
    let result = data;
    // Uncomment this for pagination support when using PagingListHandlerMixin on the Python side.
    //    if resourceType == 'devices' and operation = 'getList' and url == '/api/v1/devices'
    //      result = data.objects
    return result;
  });

  return RestangularProvider.setRestangularFields({
    id: 'key'
  });
}

routes.$inject = ["$stateProvider", "$urlRouterProvider", "RestangularProvider"]
