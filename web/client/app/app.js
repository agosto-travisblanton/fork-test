import angular from 'angular';
import uiRouter from 'angular-ui-router';
import moment from 'moment';
import "font-awesome/css/font-awesome.css";
import 'normalize.css';
import "bootstrap-webpack";
import './components/ngProgress/ngProgress';
import './components/ngProgress/ngProgress.css';
import './components/angularBreadcrumb/angularBreadcrumb';
import './components/angular-material-datetimepicker'
import './components/angular-directive.g-signin/google-plus-signin'
import './components/angular-h-sweetalert/ngSweetAlert.min'
import 'restangular';
import 'angular-material'
import 'sweetalert';
import 'angular-h-sweetalert';
import 'angular-toastr';
import 'angular-cookies';
import 'angular-sanitize';
import 'angular-ui-bootstrap';
import 'ngclipboard';
import 'jquery';
import 'angular-breadcrumb'
import 'angular-material';
// Import angular
import 'angular/angular.js';
// Material design css
import 'angular-material/angular-material.css';
import './scss/vendor.scss'
import './scss/index.scss'
import _ from 'lodash';
window._ = _;


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
import {TenantAddCtrl} from './tenant/tenant-add.controller'
import {TenantDetailsCtrl} from './tenant/tenant-details.controller'
import {TenantLocationCtrl} from './tenant/tenant-location.controller'
import {TenantManagedDevicesCtrl} from './tenant/tenant-managed-devices.controller'
import {TenantUnmanagedDevicesCtrl} from './tenant/tenant-unmanaged-devices.controller'
import {TenantsCtrl} from './tenant/tenants.controller'
// Welcome
import {WelcomeCtrl} from './welcome/welcome-controller'
// Config
import {routes} from './app-routes'
import {RestangularConfig} from './app-config'
import {appRun} from './app-run';

let app = angular.module('skykitProvisioning', [
  uiRouter,
  'ngAnimate',
  'ngCookies',
  'ngSanitize',
  'restangular',
  'hSweetAlert',
  'ui.bootstrap',
  'ngMaterialDatePicker',
  'hSweetAlert',
  'ncy-angular-breadcrumb',
  'directive.g+signin',
  'ngProgress',
  'ngMaterial',
  'ngclipboard',
  'toastr',
])
// Services
  .factory("StorageService", StorageService.storageServiceFactory)
  .factory("AdminService", AdminService.adminServiceFactory)
  .factory("AuthorizationService", AuthorizationService.authorizationServiceFactory)
  .factory("CommandsService", CommandsService.commandServiceFactory)
  .factory("DateManipulationService", DateManipulationService.datemanipulationServiceFactory)
  .factory("DevicesService", DevicesService.devicesServiceFactory)
  .factory("DistributorsService", DistributorsService.distributorServiceFactory)
  .factory("DomainsService", DomainsService.domainServiceFactory)
  .factory("IdentityService", IdentityService.identityServiceFactory)
  .factory("IntegrationEvents", IntegrationEvents.integrationEventsServiceFactory)
  .factory("LocationsService", LocationsService.locationsServiceFactory)
  .factory("ProgressBarService", ProgressBarService.progressBarServiceFactory)
  .factory("ProofPlayService", ProofPlayService.proofplayServiceFactory)
  .factory("SessionsService", SessionsService.sessionsServiceFactory)
  .factory("TenantsService", TenantsService.tenantsServiceFactory)
  .factory("TimezonesService", TimezonesService.timezoneServiceFactory)
  .factory("ToastsService", ToastsService.toastsServiceFactory)
  .factory("VersionsService", VersionsService.versionsServiceFactory)
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
  .controller("TenantAddCtrl", TenantAddCtrl)
  .controller("TenantDetailsCtrl", TenantDetailsCtrl)
  .controller("TenantLocationCtrl", TenantLocationCtrl)
  .controller("TenantManagedDevicesCtrl", TenantManagedDevicesCtrl)
  .controller("TenantUnmanagedDevicesCtrl", TenantUnmanagedDevicesCtrl)
  .controller("TenantsCtrl", TenantsCtrl)
  // Welcome
  .controller("WelcomeCtrl", WelcomeCtrl)
  // appRun Block
  .run(appRun)
  // Config
  .config(routes)

// Request Interceptor
app.factory('RequestInterceptor', function (StorageService, $location) {
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
