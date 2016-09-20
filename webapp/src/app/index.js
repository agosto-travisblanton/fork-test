import {app} from './app'
// Device
import {DeviceDetailsCommandsCtrl} from './device/device-detail-command'
import {DeviceDetailsCtrl} from './device/device-details.controller'
import {DevicesListingCtrl} from './device/devices-listing.controller'
// Admin
import {AdminCtrl} from './admin/admin-controller'
// Authentication
import {AuthenticationCtrl} from './authentication/authentication-controller'
// App
import {AppController} from './app/app-controller'
// Distributors
import {DistributorSelectorCtrl} from './distributor/distributor-selector-controller'
import {DistributorsCtrl} from './distributor/distributors-controller'
// Domains
import {DomainsCtrl} from './domain/domains.controller'
import {DomainDetailsCtrl} from './domain/domain-details.controller'
// ProofPlay
import {ProofOfPlayMultiLocationCtrl} from './proof/multi-location.controller'
import {ProofOfPlayMultiDisplayCtrl} from './proof/multi-display.controller'
import {ProofOfPlayMultiResourceCtrl} from './proof/multi-resource.controller'
import {ProofOfPlayCtrl} from './proof/proof-of-play.controller'
// Services
import ImageService from './services/image.service'
import AdminService from './services/admin.service'
import AuthorizationService from './services/authorization.service'
import CommandsService from './services/commands.service'
import DateManipulationService from './services/datemanipulation.service'
import DevicesService from './services/devices.service'
import DistributorsService from './services/distributors.service'
import DomainsService from './services/domains.service'
import IdentityService from './services/identity.service'
import IntegrationEvents from './services/integration-events.service'
import LocationsService from './services/locations.service'
import ProgressBarService from './services/progressbar.service'
import ProofPlayService from './services/proofplay.service'
import SessionsService from './services/sessions.service'
import StorageService from './services/storage.service'
import TenantsService from './services/tenants.service'
import TimezonesService from './services/timezones.service'
import ToastsService from './services/toasts.service'
import VersionsService from './services/versions.service'
// Tenant
import {TenantOverlaysCtrl} from './tenant/tenant-overlays.controller'
import {TenantAddCtrl} from './tenant/tenant-add.controller'
import {TenantDetailsCtrl} from './tenant/tenant-details.controller'
import {TenantLocationCtrl} from './tenant/tenant-location.controller'
import {TenantLocationsCtrl} from './tenant/tenant-locations.controller'
import {TenantManagedDevicesCtrl} from './tenant/tenant-managed-devices.controller'
import {TenantUnmanagedDevicesCtrl} from './tenant/tenant-unmanaged-devices.controller'
import {TenantsCtrl} from './tenant/tenants.controller'
// Welcome
import {WelcomeCtrl} from './welcome/welcome-controller'
// Config
import {routes} from './app-routes'
import {appRun} from './app-run';
import {toastrConfig, breadcrumbProvider} from './app-config'


app
// Services
  .service("StorageService", StorageService)
  .service("AdminService", AdminService)
  .service("AuthorizationService", AuthorizationService)
  .service("CommandsService", CommandsService)
  .service("DateManipulationService", DateManipulationService)
  .service("DevicesService", DevicesService)
  .service("DistributorsService", DistributorsService)
  .service("DomainsService", DomainsService)
  .service("IdentityService", IdentityService)
  .service("IntegrationEvents", IntegrationEvents)
  .service("LocationsService", LocationsService)
  .service("ProgressBarService", ProgressBarService)
  .service("ProofPlayService", ProofPlayService)
  .service("SessionsService", SessionsService)
  .service("TenantsService", TenantsService)
  .service("TimezonesService", TimezonesService)
  .service("ToastsService", ToastsService)
  .service("VersionsService", VersionsService)
  .service("ImageService", ImageService)
  // Device
  .controller("DeviceDetailsCommandsCtrl", DeviceDetailsCommandsCtrl)
  .controller("DeviceDetailsCtrl", DeviceDetailsCtrl)
  .controller("DevicesListingCtrl", DevicesListingCtrl)
  // Admin
  .controller("AdminCtrl", AdminCtrl)
  // Authentication
  .controller("AuthenticationCtrl", AuthenticationCtrl)
  // App
  .controller("AppController", AppController)
  // Distributors
  .controller("DistributorSelectorCtrl", DistributorSelectorCtrl)
  .controller("DistributorsCtrl", DistributorsCtrl)
  // Domains
  .controller("DomainsCtrl", DomainsCtrl)
  .controller("DomainDetailsCtrl", DomainDetailsCtrl)
  // ProofPlay
  .controller("ProofOfPlayMultiLocationCtrl", ProofOfPlayMultiLocationCtrl)
  .controller("ProofOfPlayMultiDisplayCtrl", ProofOfPlayMultiDisplayCtrl)
  .controller("ProofOfPlayMultiResourceCtrl", ProofOfPlayMultiResourceCtrl)
  .controller("ProofOfPlayCtrl", ProofOfPlayCtrl)
  // Tenants
  .controller("TenantOverlaysCtrl", TenantOverlaysCtrl)
  .controller("TenantAddCtrl", TenantAddCtrl)
  .controller("TenantDetailsCtrl", TenantDetailsCtrl)
  .controller("TenantLocationCtrl", TenantLocationCtrl)
  .controller("TenantLocationsCtrl", TenantLocationsCtrl)
  .controller("TenantManagedDevicesCtrl", TenantManagedDevicesCtrl)
  .controller("TenantUnmanagedDevicesCtrl", TenantUnmanagedDevicesCtrl)
  .controller("TenantsCtrl", TenantsCtrl)
  // Welcome
  .controller("WelcomeCtrl", WelcomeCtrl)
  // appRun Block
  .run(appRun)
  // Config
  .config(routes)
  .config(toastrConfig)
  .config(breadcrumbProvider)

// Request Interceptor
app.service('RequestInterceptor', function (StorageService, $location) {
  "ngInject";
  let interceptor = {
    request(config) {
      let gs = '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g';
      let prod = '6C346588BD4C6D722A1165B43C51C';
      config.headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': $location.host().indexOf('provisioning-gamestop') > -1 ? gs : prod,
        'X-Provisioning-User': StorageService.get('userKey'),
        'X-Provisioning-User-Identifier': StorageService.get('userEmail'),
        'X-Provisioning-Distributor': StorageService.get('currentDistributorKey')
      };
      return config;
    }
  };
  return interceptor;
});


app.config($httpProvider => $httpProvider.interceptors.push('RequestInterceptor'));
