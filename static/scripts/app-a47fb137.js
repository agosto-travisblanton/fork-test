(function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement",["ngAnimate","ngCookies","ngTouch","ngSanitize","restangular","ui.router","hSweetAlert","ui.bootstrap","ncy-angular-breadcrumb"]),e.config(["$stateProvider","$urlRouterProvider","RestangularProvider",function(e,t,i){return e.state("home",{url:"/",templateUrl:"app/welcome/welcome.html",controller:"WelcomeCtrl",controllerAs:"welcomeCtrl",ncyBreadcrumb:{label:"Home page"}}),e.state("welcome",{url:"/welcome",templateUrl:"app/welcome/welcome.html",controller:"WelcomeCtrl",controllerAs:"welcomeCtrl",ncyBreadcrumb:{label:"Home page"}}),e.state("domain",{url:"/domain",templateUrl:"app/domain/domain.html",controller:"DomainCtrl",ncyBreadcrumb:{label:"Domains"}}),e.state("tenants",{url:"/tenants",templateUrl:"app/tenant/tenants.html",controller:"TenantsCtrl",controllerAs:"tenantsCtrl",ncyBreadcrumb:{label:"Tenants"}}),e.state("newTenant",{url:"/tenants/new",templateUrl:"app/tenant/tenant-detail.html",controller:"TenantDetailsCtrl",controllerAs:"tenantDetailsCtrl",ncyBreadcrumb:{label:"New tenant",parent:"tenants"}}),e.state("editTenant",{url:"/tenants/:tenantKey",templateUrl:"app/tenant/tenant-detail.html",controller:"TenantDetailsCtrl",controllerAs:"tenantDetailsCtrl",ncyBreadcrumb:{label:"{{ tenantDetailsCtrl.currentTenant.name }}",parent:"tenants"}}),e.state("devices",{url:"/devices",templateUrl:"app/device/devices-listing.html",controller:"DevicesListingCtrl",controllerAs:"devicesListingCtrl",ncyBreadcrumb:{label:"Displays"}}),e.state("editDevice",{url:"/devices/:deviceKey?tenantKey",templateUrl:"app/device/device-detail.html",ncyBreadcrumb:{label:"{{ deviceDetailsCtrl.currentDevice.key }}",parent:"devices"},controller:"DeviceDetailsCtrl","function":function(e,t){e.tenantKey=t.tenantKey},controllerAs:"deviceDetailsCtrl"}),e.state("remote_control",{url:"/remote_control",templateUrl:"app/remote_control/index.html",controller:"RemoteControlCtrl",controllerAs:"remoteControlCtrl",ncyBreadcrumb:{label:"Remote control"}}),t.otherwise("/"),i.setBaseUrl("/api/v1"),i.setDefaultHeaders({"Content-Type":"application/json",Accept:"application/json",Authorization:"6C346588BD4C6D722A1165B43C51C"}),i.addRequestInterceptor(function(e,t){return"remove"===t?void 0:e}),i.addResponseInterceptor(function(e,t,i,a){var n;return n=e,"devices"===i&&(t="getList"&&"/api/v1/devices"===a)&&(n=e.objects),n}),i.setRestangularFields({id:"key"})}])}).call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("NavbarCtrl",["$scope",function(){}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("WelcomeCtrl",["$state","DistributorsService",function(e,t){return this.distributors=[],this.currentDistributor=void 0,this.initialize=function(){var e;return e=t.fetchAll(),e.then(function(e){return function(t){return e.distributors=t}}(this))},this.selectDistributor=function(){return this.currentDistributor&&null!==this.currentDistributor?t.currentDistributor=this.currentDistributor:void 0},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("TenantsCtrl",["$state","TenantsService","sweet",function(e,t,i){return this.tenants=[],this.initialize=function(){var e;return e=t.fetchAllTenants(),e.then(function(e){return function(t){return e.tenants=t}}(this))},this.editItem=function(t){return e.go("editTenant",{tenantKey:t.key})},this.deleteItem=function(e){return function(a){var n;return n=function(){var i;return i=t["delete"](a),i.then(function(){return e.initialize()})},i.show({title:"Are you sure?",text:"This will permanently remove the tenant from the system.",type:"warning",showCancelButton:!0,confirmButtonColor:"#DD6B55",confirmButtonText:"Yes, remove the tenant!",closeOnConfirm:!0},n)}}(this),this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("TenantDetailsCtrl",["$stateParams","TenantsService","DevicesService","$state",function(e,t,i,a){var n,r;return this.currentTenant={key:void 0,name:void 0,tenant_code:void 0,admin_email:void 0,content_server_url:void 0,chrome_device_domain:void 0,active:!0},this.currentTenantDisplays=[],this.editMode=!!e.tenantKey,this.editMode&&(r=t.getTenantByKey(e.tenantKey),r.then(function(e){return function(t){return e.currentTenant=t}}(this)),n=i.getDevicesByTenant(e.tenantKey),n.then(function(e){return function(t){return e.currentTenantDisplays=t.objects}}(this))),this.onClickSaveButton=function(){var e;return e=t.save(this.currentTenant),e.then(function(){return a.go("tenants")})},this.editItem=function(t){return a.go("editDevice",{deviceKey:t.key,tenantKey:e.tenantKey})},this.autoGenerateTenantCode=function(){var e;return this.currentTenant.key?void 0:(e="",this.currentTenant.name&&(e=this.currentTenant.name.toLowerCase(),e=e.replace(/\s+/g,"_"),e=e.replace(/\W+/g,"")),this.currentTenant.tenant_code=e)},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("DeviceDetailsCtrl",["$stateParams","$state","DevicesService","TenantsService",function(e,t,i,a){var n,r;return this.currentDevice={key:void 0,gcm_registration_id:void 0,annotated_location:void 0,annotated_user:void 0,api_key:void 0,device_id:void 0,boot_mode:void 0,chrome_device_domain:void 0,content_server_url:void 0,etag:void 0,ethernet_mac_address:void 0,mac_address:void 0,firmware_version:void 0,kind:void 0,last_enrollment_time:void 0,last_sync:void 0,model:void 0,org_unit_path:void 0,os_version:void 0,platform_version:void 0,serial_number:void 0,status:void 0,tenant_key:void 0,created:void 0,updated:void 0},this.editMode=!!e.deviceKey,r=a.fetchAllTenants(),r.then(function(e){return function(t){return e.tenants=t}}(this)),this.editMode&&(n=i.getDeviceByKey(e.deviceKey),n.then(function(e){return function(t){return e.currentDevice=t}}(this))),this.onClickSaveButton=function(){var e;return e=i.save(this.currentDevice),e.then(function(){return t.go("devices")})},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.factory("TenantsService",["Restangular",function(e){var t;return new(t=function(){function t(){}return t.prototype.save=function(t){var i;return i=void 0!==t.key?t.put():e.service("tenants").post(t)},t.prototype.fetchAllTenants=function(){var t;return t=e.all("tenants").getList()},t.prototype.getTenantByKey=function(t){var i;return i=e.oneUrl("tenants","api/v1/tenants/"+t).get()},t.prototype["delete"]=function(t){var i;return void 0!==t.key?i=e.one("tenants",t.key).remove():void 0},t}())}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.factory("DistributorsService",["Restangular",function(e){var t;return new(t=function(){function t(){}var i;return i="distributors",t.currentDistributor=void 0,t.prototype.save=function(t){var a;return a=void 0!==t.key?t.put():e.service(i).post(t)},t.prototype.fetchAll=function(){var t;return t=e.all(i).getList()},t.prototype.getByKey=function(t){var a;return a=e.oneUrl(i,"distributors/"+t).get()},t.prototype["delete"]=function(t){var a;return t.key?a=e.one(i,t.key).remove():void 0},t}())}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").factory("DevicesService",["$http","$log","Restangular",function(e,t,i){var a;return new(a=function(){function e(){}var t;return t="devices",e.uriBase="v1/devices",e.prototype.getDeviceByMacAddress=function(e){return i.oneUrl("api/v1/devices","api/v1/devices?mac_address="+e).get()},e.prototype.getDeviceByKey=function(e){var a;return a=i.oneUrl(t,"api/v1/devices/"+e).get()},e.prototype.getDevicesByTenant=function(e){var a;return void 0!==e?a=i.one("tenants",e).doGET(t):void 0},e.prototype.getDevices=function(){var e,a;return e={},a=i.all(t).getList()},e.prototype.save=function(e){var t;return t=void 0!==e.key?e.put():i.service("devices").post(e)},e}())}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("MainCtrl",["$scope",function(e){return e.awesomeThings=[1,2,3,4,5,6],this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("RemoteControlCtrl",["DevicesService",function(){return this.devices=[],this.currentDevice={id:void 0,name:void 0},this.initialize=function(){return this.devices=[{id:1,name:"Device 1"},{id:2,name:"Device 2"},{id:3,name:"Device 3"},{id:4,name:"Device 4"}]},this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("DomainCtrl",["$scope",function(){return this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("DevicesListingCtrl",["$stateParams","DevicesService","$state",function(e,t,i){var a;return this.devices=[],a=t.getDevices(),a.then(function(e){return function(t){return e.devices=t}}(this)),this.editItem=function(e){return i.go("editDevice",{deviceKey:e.key,tenantKey:""})},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("DeviceDetailsCtrl",["$stateParams","$state","DevicesService","TenantsService",function(e,t,i,a){var n,r;return this.tenantKey=e.tenantKey,this.currentDevice={key:void 0,gcm_registration_id:void 0,annotated_location:void 0,annotated_user:void 0,api_key:void 0,device_id:void 0,boot_mode:void 0,chrome_device_domain:void 0,content_server_url:void 0,etag:void 0,ethernet_mac_address:void 0,mac_address:void 0,firmware_version:void 0,kind:void 0,last_enrollment_time:void 0,last_sync:void 0,model:void 0,org_unit_path:void 0,os_version:void 0,platform_version:void 0,serial_number:void 0,status:void 0,tenant_key:void 0,created:void 0,updated:void 0},this.editMode=!!e.deviceKey,r=a.fetchAllTenants(),r.then(function(e){return function(t){return e.tenants=t}}(this)),this.editMode&&(n=i.getDeviceByKey(e.deviceKey),n.then(function(e){return function(t){return e.currentDevice=t}}(this))),this.onClickSaveButton=function(){var e;return e=i.save(this.currentDevice),e.then(function(){return t.go("devices")})},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("DistributorsCtrl",["$state",function(){return this.distributors=[],this.initialize=function(){},this}])}.call(this),angular.module("skykitDisplayDeviceManagement").run(["$templateCache",function(e){e.put("app/distributor/distributors.html",'<div id="wrapper" ng-init="tenantsCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div><h1 class="page-header">Distributors</h1></div></div><div class="row"><div class="col-lg-12"></div></div></div></div></div>'),e.put("app/device/device-detail.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div><div ng-show="deviceDetailsCtrl.tenantKey.length > 0"><a href="/#/tenants/{{deviceDetailsCtrl.tenantKey}}">back to Tenant</a></div></div></div><div><div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Display properties</h3></div><div class="panel-body"><form name="deviceForm" class="form-horizontal" ng-submit="deviceDetailsCtrl.onClickSaveButton()" novalidate=""><div class="form-group" ng-class="{ \'has-error\' : deviceForm.serial_number.$invalid && !deviceForm.serial_number.$pristine }"><label for="serialNumber" class="col-sm-3 control-label">Serial number</label><div class="col-sm-4"><input type="text" class="form-control" name="serialNumber" id="serialNumber" readonly="" ng-model="deviceDetailsCtrl.currentDevice.serial_number"></div><div class="col-sm-5"><p ng-show="deviceForm.serial_number.$invalid && !deviceForm.serial_number.$pristine" class="help-block">The display serial number is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.gcm_registration_id.$invalid && !deviceForm.gcm_registration_id.$pristine }"><label for="gcmRegistrationId" class="col-sm-3 control-label">GCM registration ID</label><div class="col-sm-4"><input type="text" class="form-control" name="gcmRegistrationId" id="gcmRegistrationId" readonly="" ng-model="deviceDetailsCtrl.currentDevice.gcm_registration_id"></div><div class="col-sm-5"><p ng-show="deviceForm.gcm_registration_id.$invalid && !deviceForm.gcm_registration_id.$pristine" class="help-block">The display GCM registration ID is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.annotated_location.$invalid && !deviceForm.annotated_location.$pristine }"><label for="annotatedLocation" class="col-sm-3 control-label">Annotated location</label><div class="col-sm-4"><input type="text" class="form-control" name="annotatedLocation" id="annotatedLocation" readonly="" ng-model="deviceDetailsCtrl.currentDevice.annotated_location"></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.annotated_user.$invalid && !deviceForm.annotated_user.$pristine }"><label for="annotatedUser" class="col-sm-3 control-label">Annotated user</label><div class="col-sm-4"><input type="text" class="form-control" name="annotatedUser" id="annotatedUser" readonly="" ng-model="deviceDetailsCtrl.currentDevice.annotated_user"></div><div class="col-sm-5"><p ng-show="deviceForm.annotated_user.$invalid && !deviceForm.annotated_user.$pristine" class="help-block">The display annotated user is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.api_key.$invalid && !deviceForm.api_key.$pristine }"><label for="apiKey" class="col-sm-3 control-label">API key</label><div class="col-sm-4"><input type="text" class="form-control" name="apiKey" id="apiKey" readonly="" ng-model="deviceDetailsCtrl.currentDevice.api_key"></div><div class="col-sm-5"><p ng-show="deviceForm.api_key.$invalid && !deviceForm.api_key.$pristine" class="help-block">The display API key is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.display_id.$invalid && !deviceForm.display_id.$pristine }"><label for="displayId" class="col-sm-3 control-label">Display ID</label><div class="col-sm-4"><input type="text" class="form-control" name="displayId" id="displayId" readonly="" ng-model="deviceDetailsCtrl.currentDevice.display_id"></div><div class="col-sm-5"><p ng-show="deviceForm.display_id.$invalid && !deviceForm.display_id.$pristine" class="help-block">The display ID is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.boot_mode.$invalid && !deviceForm.boot_mode.$pristine }"><label for="bootMode" class="col-sm-3 control-label">Boot mode</label><div class="col-sm-4"><input type="text" class="form-control" name="bootMode" id="bootMode" readonly="" ng-model="deviceDetailsCtrl.currentDevice.boot_mode"></div><div class="col-sm-5"><p ng-show="deviceForm.boot_mode.$invalid && !deviceForm.boot_mode.$pristine" class="help-block">The display boot mode is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.chrome_display_domain.$invalid && !deviceForm.chrome_display_domain.$pristine }"><label for="chromeDisplayDomain" class="col-sm-3 control-label">Chrome display domain</label><div class="col-sm-4"><input type="text" class="form-control" name="chromeDisplayDomain" id="chromeDisplayDomain" readonly="" ng-model="deviceDetailsCtrl.currentDevice.chrome_display_domain"></div><div class="col-sm-5"><p ng-show="deviceForm.chrome_display_domain.$invalid && !deviceForm.chrome_display_domain.$pristine" class="help-block">The Chrome display domain is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.content_server_url.$invalid && !deviceForm.content_server_url.$pristine }"><label for="contentServerUrl" class="col-sm-3 control-label">Content server URL</label><div class="col-sm-4"><input type="text" class="form-control" name="contentServerUrl" id="contentServerUrl" readonly="" ng-model="deviceDetailsCtrl.currentDevice.content_server_url"></div><div class="col-sm-5"><p ng-show="deviceForm.content_server_url.$invalid && !deviceForm.content_server_url.$pristine" class="help-block">The display content server URL is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.etag.$invalid && !deviceForm.etag.$pristine }"><label for="etag" class="col-sm-3 control-label">Etag</label><div class="col-sm-4"><input type="text" class="form-control" name="etag" id="etag" readonly="" ng-model="deviceDetailsCtrl.currentDevice.etag"></div><div class="col-sm-5"><p ng-show="deviceForm.etag.$invalid && !deviceForm.etag.$pristine" class="help-block">The display Etag is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.ethernet_mac_address.$invalid && !deviceForm.ethernet_mac_address.$pristine }"><label for="ethernetMacAddress" class="col-sm-3 control-label">Ethernet MAC address</label><div class="col-sm-4"><input type="text" class="form-control" name="ethernetMacAddress" id="ethernetMacAddress" readonly="" ng-model="deviceDetailsCtrl.currentDevice.ethernet_mac_address"></div><div class="col-sm-5"><p ng-show="deviceForm.ethernet_mac_address.$invalid && !deviceForm.ethernet_mac_address.$pristine" class="help-block">The display ethernet MAC address is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.mac_address.$invalid && !deviceForm.mac_address.$pristine }"><label for="macAddress" class="col-sm-3 control-label">MAC address</label><div class="col-sm-4"><input type="text" class="form-control" name="macAddress" id="macAddress" readonly="" ng-model="deviceDetailsCtrl.currentDevice.mac_address"></div><div class="col-sm-5"><p ng-show="deviceForm.mac_address.$invalid && !deviceForm.mac_address.$pristine" class="help-block">The display MAC address is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.firmware_version.$invalid && !deviceForm.firmware_version.$pristine }"><label for="firmwareVersion" class="col-sm-3 control-label">Firmware version</label><div class="col-sm-4"><input type="text" class="form-control" name="firmwareVersion" id="firmwareVersion" readonly="" ng-model="deviceDetailsCtrl.currentDevice.firmware_version"></div><div class="col-sm-5"><p ng-show="deviceForm.firmware_version.$invalid && !deviceForm.firmware_version.$pristine" class="help-block">The display firmware version is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.kind.$invalid && !deviceForm.kind.$pristine }"><label for="kind" class="col-sm-3 control-label">Kind</label><div class="col-sm-4"><input type="text" class="form-control" name="kind" id="kind" readonly="" ng-model="deviceDetailsCtrl.currentDevice.kind"></div><div class="col-sm-5"><p ng-show="deviceForm.kind.$invalid && !deviceForm.kind.$pristine" class="help-block">The display kind is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.last_enrollment_time.$invalid && !deviceForm.last_enrollment_time.$pristine }"><label for="lastEnrollmentTime" class="col-sm-3 control-label">Last enrollment timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="lastEnrollmentTime" id="lastEnrollmentTime" readonly="" ng-model="deviceDetailsCtrl.currentDevice.last_enrollment_time"></div><div class="col-sm-5"><p ng-show="deviceForm.last_enrollment_time.$invalid && !deviceForm.last_enrollment_time.$pristine" class="help-block">The display last enrollment timestamp is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.last_sync.$invalid && !deviceForm.last_sync.$pristine }"><label for="lastSync" class="col-sm-3 control-label">Last sync timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="lastSync" id="lastSync" readonly="" ng-model="deviceDetailsCtrl.currentDevice.last_sync"></div><div class="col-sm-5"><p ng-show="deviceForm.last_sync.$invalid && !deviceForm.last_sync.$pristine" class="help-block">The display last sync timestamp is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.model.$invalid && !deviceForm.model.$pristine }"><label for="model" class="col-sm-3 control-label">Model</label><div class="col-sm-4"><input type="text" class="form-control" name="model" id="model" readonly="" ng-model="deviceDetailsCtrl.currentDevice.model"></div><div class="col-sm-5"><p ng-show="deviceForm.model.$invalid && !deviceForm.model.$pristine" class="help-block">The display model is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.org_unit_path.$invalid && !deviceForm.org_unit_path.$pristine }"><label for="orgUnitPath" class="col-sm-3 control-label">Organizational unit path</label><div class="col-sm-4"><input type="text" class="form-control" name="orgUnitPath" id="orgUnitPath" readonly="" ng-model="deviceDetailsCtrl.currentDevice.org_unit_path"></div><div class="col-sm-5"><p ng-show="deviceForm.org_unit_path.$invalid && !deviceForm.org_unit_path.$pristine" class="help-block">The display organizational unit path is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.os_version.$invalid && !deviceForm.os_version.$pristine }"><label for="osVersion" class="col-sm-3 control-label">Operating system version</label><div class="col-sm-4"><input type="text" class="form-control" name="osVersion" id="osVersion" readonly="" ng-model="deviceDetailsCtrl.currentDevice.os_version"></div><div class="col-sm-5"><p ng-show="deviceForm.os_version.$invalid && !deviceForm.os_version.$pristine" class="help-block">The display OS version is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.platform_version.$invalid && !deviceForm.platform_version.$pristine }"><label for="platformVersion" class="col-sm-3 control-label">Platform version</label><div class="col-sm-4"><input type="text" class="form-control" name="platformVersion" id="platformVersion" readonly="" ng-model="deviceDetailsCtrl.currentDevice.platform_version"></div><div class="col-sm-5"><p ng-show="deviceForm.platform_version.$invalid && !deviceForm.platform_version.$pristine" class="help-block">The display platform version is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.status.$invalid && !deviceForm.status.$pristine }"><label for="status" class="col-sm-3 control-label">Status</label><div class="col-sm-4"><input type="text" class="form-control" name="status" id="status" readonly="" ng-model="deviceDetailsCtrl.currentDevice.status"></div><div class="col-sm-5"><p ng-show="deviceForm.status.$invalid && !deviceForm.status.$pristine" class="help-block">The display status is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.tenant.$invalid && !deviceForm.tenant.$pristine }"><label for="tenantCode" class="col-sm-3 control-label">Tenant code</label><div class="col-sm-4"><input type="text" class="form-control" name="tenantCode" id="tenantCode" readonly="" ng-model="deviceDetailsCtrl.currentDevice.tenant_code"></div><div class="col-sm-5"><p ng-show="deviceForm.tenant.$invalid && !deviceForm.tenant.$pristine" class="help-block">The display tenant is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.notes.$invalid && !deviceForm.notes.$pristine }"><label for="notes" class="col-sm-3 control-label">Notes</label><div class="col-sm-4"><input type="text" class="form-control" name="notes" id="notes" readonly="" ng-model="deviceDetailsCtrl.currentDevice.notes"></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.created.$invalid && !deviceForm.created.$pristine }"><label for="created" class="col-sm-3 control-label">Created timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="created" id="created" readonly="" ng-model="deviceDetailsCtrl.currentDevice.created"></div><div class="col-sm-5"><p ng-show="deviceForm.created.$invalid && !deviceForm.created.$pristine" class="help-block">The display created timestamp is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.updated.$invalid && !deviceForm.updated.$pristine }"><label for="updated" class="col-sm-3 control-label">Updated timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="updated" id="updated" readonly="" ng-model="deviceDetailsCtrl.currentDevice.updated"></div><div class="col-sm-5"><p ng-show="deviceForm.updated.$invalid && !deviceForm.updated.$pristine" class="help-block">The display updated timestamp is required.</p></div></div><hr><div class="form-group"><div class="col-sm-offset-3 col-sm-4"><button type="submit" class="btn btn-primary btn-default" ng-disabled="!deviceForm.$dirty || deviceForm.$invalid"><i class="fa fa-fw fa-save"></i> Save</button></div></div></form></div></div></div></div></div></div>'),e.put("app/device/devices-listing.html",'<div id="wrapper" ng-init="devicesListingCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div><h1 class="page-header">Displays</h1></div></div><div class="row"><div class="col-lg-12"><table name="tenant-table" class="table table-bordered table-responsive table-striped"><thead><tr><th>Serial number</th><th>Tenant code</th><th>Wifi mac address</th><th>Ether mac address</th><th>Provisioning date</th></tr></thead><tbody><tr ng-hide="devicesListingCtrl.devices.length"><td class="no-devices text-center text-danger" colspan="5">No displays</td></tr><tr ng-repeat="item in devicesListingCtrl.devices | orderBy:\'-created\'" ng-click="devicesListingCtrl.editItem(item)"><td class="display-serial-number">{{ item.serial_number }}</td><td class="display-tenant-code">{{ item.tenant_code }}</td><td class="display-mac-address">{{ item.mac_address }}</td><td class="display-ethernet-mac-address">{{ item.ethernet_mac_address }}</td><td class="display-provisioning-date">{{ item.created }}</td></tr></tbody></table></div></div></div></div></div>'),e.put("app/domain/domain.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div><h1 class="page-header">Device <small>Subtitle</small></h1></div></div><div class="row"><div class="col-lg-12"><fieldset><legend>Devices</legend><div class="col-md-12 toolbar"><a id="button-add-device" class="btn btn-default btn-success" href="#/deviceEdit"><i class="glyphicon glyphicon-plus"></i> Add device</a></div><table class="table table-bordered table-responsive table-striped"><thead><tr><th>Name</th><th>Location</th><th>MAC address</th><th>Device ID</th></tr></thead><tbody><tr><td>Test ChromeOS device 001</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 002</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 003</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 004</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr></tbody></table></fieldset></div></div></div></div></div>'),e.put("app/main/main.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div><h1 class="page-header">Skykit Provisioning</h1></div></div></div></div></div>'),e.put("app/remote_control/index.html",'<div id="wrapper" ng-init="remoteControlCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div><h1 class="page-header">Remote control</h1></div></div><div class="row" data-ng-controller="RemoteControlCtrl"><div class="col-lg-4"><label for="device">Choose a device:</label><select id="device" data-ng-model="remoteControlCtrl.currentDevice" data-ng-options="c.name for c in remoteControlCtrl.devices"><option value="">Select device</option></select></div><div class="col-lg-8"><div ng-show="remoteControlCtrl.currentDevice.name != undefined">selected device: {{ remoteControlCtrl.currentDevice}}</div></div></div></div></div></div>'),e.put("app/tenant/tenant-detail.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div></div></div><div><tabset><tab heading="Linked displays"><div style="margin-top: 1px;">&nbsp;</div><div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">{{tenantDetailsCtrl.currentTenant.name}}</h3></div><div class="panel-body"><table class="table table-bordered table-condensed table-responsive table-striped"><thead><tr><th>Serial number</th><th>Device ID</th><th>Wifi mac address</th><th>Ether mac address</th><th>Provisioning date</th></tr></thead><tbody><tr ng-hide="tenantDetailsCtrl.currentTenantDisplays.length"><td colspan="5" class="text-center text-danger">No displays</td></tr><tr ng-repeat="item in tenantDetailsCtrl.currentTenantDisplays | orderBy:\'-created\'" ng-click="tenantDetailsCtrl.editItem(item)"><td class="tenant-display-serial-number">{{ item.serial_number }}</td><td class="tenant-display-id">{{ item.device_id }}</td><td class="tenant-display-mac-address">{{ item.mac_address }}</td><td class="tenant-display-ethernet-mac-address">{{ item.ethernet_mac_address }}</td><td class="tenant-display-provisioning-date">{{ item.created }}</td></tr></tbody></table></div></div></tab><tab heading="General"><div style="margin-top: 1px;">&nbsp;</div><div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title">{{ tenantDetailsCtrl.currentTenant.name }}</h4></div><div class="panel-body"><form name="tenantForm" class="form-horizontal" ng-submit="tenantDetailsCtrl.onClickSaveButton()" novalidate=""><div class="form-group" ng-class="{ \'has-error\' : tenantForm.name.$invalid && !tenantForm.name.$pristine }"><label for="name" class="col-sm-2 control-label">Name</label><div class="col-sm-4"><input type="text" class="form-control" name="name" id="name" required="" placeholder="Enter tenant name" ng-model="tenantDetailsCtrl.currentTenant.name" ng-change="tenantDetailsCtrl.autoGenerateTenantCode()" autofocus=""></div><div class="col-sm-6"><p ng-show="tenantForm.name.$invalid && !tenantForm.name.$pristine" class="help-block">The tenant name is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.tenantCode.$invalid && !tenantForm.tenantCode.$pristine }"><label for="tenantCode" class="col-sm-2 control-label">Tenant code</label><div class="col-sm-4"><input type="text" class="form-control" name="tenantCode" id="tenantCode" required="" placeholder="Enter tenant code (must match tenant code in Google Device Management)" ng-model="tenantDetailsCtrl.currentTenant.tenant_code"></div><div class="col-sm-6"><p ng-show="tenantForm.tenantCode.$invalid && !tenantForm.tenantCode.$pristine" class="help-block">The tenant lookup code is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.adminEmail.$invalid && !tenantForm.adminEmail.$pristine }"><label for="adminEmail" class="col-sm-2 control-label">Admin email address</label><div class="col-sm-4"><input type="text" required="" class="form-control" name="adminEmail" id="adminEmail" placeholder="Enter admin email" ng-model="tenantDetailsCtrl.currentTenant.admin_email"></div><div class="col-sm-6"><p ng-show="tenantForm.adminEmail.$invalid && !tenantForm.adminEmail.$pristine" class="help-block">The tenant admin email address is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.chromeDeviceDomain.$invalid && !tenantForm.chromeDeviceDomain.$pristine }"><label for="chromeDeviceDomain" class="col-sm-2 control-label">Chrome device domain</label><div class="col-sm-4"><input type="text" required="" class="form-control" name="chromeDeviceDomain" id="chromeDeviceDomain" placeholder="Enter Chrome device domain" ng-model="tenantDetailsCtrl.currentTenant.chrome_device_domain"></div><div class="col-sm-6"><p ng-show="tenantForm.chromeDeviceDomain.$invalid && !tenantForm.chromeDeviceDomain.$pristine" class="help-block">The Chrome device domain is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.contentServerUrl.$invalid && !tenantForm.contentServerUrl.$pristine }"><label for="contentServerUrl" class="col-sm-2 control-label">Content server URL</label><div class="col-sm-4"><input type="url" required="" class="form-control" name="contentServerUrl" id="contentServerUrl" placeholder="Enter content server URL" ng-model="tenantDetailsCtrl.currentTenant.content_server_url" ng-pattern="/^https:\\/\\/\\S+$/"></div><div class="col-sm-6"><p ng-show="tenantForm.contentServerUrl.$invalid && !tenantForm.contentServerUrl.$pristine" class="help-block">The content server URL is required to be a secure URL.</p></div></div><div class="form-group"><div class="col-sm-offset-2 col-sm-6"><input type="checkbox" id="active" ng-model="tenantDetailsCtrl.currentTenant.active"> <label for="active">Active</label></div></div><hr><div class="form-group"><div class="col-sm-offset-2 col-sm-10"><button type="submit" class="btn btn-primary btn-default" ng-disabled="tenantForm.$invalid"><i class="fa fa-fw fa-save"></i> Save</button></div></div></form><hr><div class="col-sm-12"><label class="control-label">key:</label><br><small>{{tenantDetailsCtrl.currentTenant.key}}</small></div></div></div></tab></tabset></div></div></div></div>'),e.put("app/tenant/tenants.html",'<div id="wrapper" ng-init="tenantsCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><div ncy-breadcrumb=""></div><h1 class="page-header">Tenants</h1></div></div><div class="row"><div class="col-lg-12"><div class="col-md-12 toolbar"><a id="button-add-tenant" class="btn btn-success" href="#/tenants/new"><i class="fa fa-fw fa-plus"></i> Add tenant</a></div><table name="tenant-table" class="table table-bordered table-responsive table-striped"><thead><tr><th>Name</th><th>Email</th><th>Content Server URL</th></tr></thead><tbody><tr ng-hide="tenantsCtrl.tenants.length"><td name="no-tenants" colspan="3">No tenants</td></tr><tr ng-repeat="item in tenantsCtrl.tenants | orderBy:\'name\'" ng-click="tenantsCtrl.editItem(item)"><td class="tenant-name">{{item.name}}</td><td class="tenant-admin-email">{{item.admin_email}}</td><td class="content-server-url">{{item.content_server_url}}</td></tr></tbody></table></div></div></div></div></div>'),e.put("app/welcome/welcome.html",'<div id="wrapper" ng-init="welcomeCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div ncy-breadcrumb=""></div><div class="row"><div class="col-lg-12"><h1 class="page-header">Welcome to Skykit Provisioning</h1></div></div><div class="row"><div class="col-lg-12"><label for="distributor">Choose a distributor:</label><select id="distributor" data-ng-model="welcomeCtrl.currentDistributor" data-ng-options="c.name for c in welcomeCtrl.distributors" ng-change="welcomeCtrl.selectDistributor()"><option value="">Select distributor</option></select></div></div></div></div></div>'),e.put("app/components/navbar/navbar.html",'<nav class="navbar navbar-default navbar-fixed-top" role="navigation"><div class="navbar-header"><button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse"><span class="sr-only">Toggle navigation</span> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span></button> <a class="navbar-brand" href="/"><img src="assets/images/skykit_logo2.png"></a></div><div class="collapse navbar-collapse navbar-ex1-collapse"><ul class="nav navbar-nav side-nav"><li><a id="navbar-tenants" href="#/tenants"><i class="fa fa-fw fa-users"></i> Tenants</a></li><li><a id="navbar-devices" href="#/devices"><i class="fa fa-fw fa-desktop"></i> Displays</a></li><li><a id="navbar-remote_control" href="#/remote_control"><i class="fa fa-fw fa-building"></i> Remote control</a></li></ul></div></nav>')
}]);