(function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement",["ngAnimate","ngCookies","ngTouch","ngSanitize","restangular","ui.router","hSweetAlert","ui.bootstrap"]),e.config(["$stateProvider","$urlRouterProvider","RestangularProvider",function(e,t,i){return e.state("home",{url:"/",templateUrl:"app/main/main.html",controller:"MainCtrl"}),e.state("domain",{url:"/domain",templateUrl:"app/domain/domain.html",controller:"DomainCtrl"}),e.state("deviceEdit",{url:"/deviceEdit",templateUrl:"app/device/device.editor.html",controller:"DeviceEditorCtrl",controllerAs:"deviceEdit"}),e.state("tenants",{url:"/tenants",templateUrl:"app/tenant/tenants.html",controller:"TenantsCtrl",controllerAs:"tenantsCtrl"}),e.state("newTenant",{url:"/tenants/new",templateUrl:"app/tenant/tenant-detail.html",controller:"TenantDetailsCtrl",controllerAs:"tenantDetailsCtrl"}),e.state("editTenant",{url:"/tenants/:tenantKey",templateUrl:"app/tenant/tenant-detail.html",controller:"TenantDetailsCtrl",controllerAs:"tenantDetailsCtrl"}),e.state("editDevice",{url:"/devices/:deviceKey",templateUrl:"app/device/device-detail.html",controller:"DeviceDetailsCtrl",controllerAs:"deviceDetailsCtrl"}),e.state("apiTest",{url:"/api_testing",templateUrl:"app/api_test/api_test.html",controller:"ApiTestCtrl",controllerAs:"apiTest"}),e.state("remote_control",{url:"/remote_control",templateUrl:"app/remote_control/index.html",controller:"RemoteControlCtrl",controllerAs:"remoteControlCtrl"}),t.otherwise("/"),i.setBaseUrl("/api/v1"),i.setDefaultHeaders({"Content-Type":"application/json",Accept:"application/json",Authorization:"6C346588BD4C6D722A1165B43C51C"}),i.addRequestInterceptor(function(e,t){return"remove"===t?void 0:e}),i.setRestangularFields({id:"key"})}])}).call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("NavbarCtrl",["$scope",function(){}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.factory("TenantsService",["Restangular",function(e){var t;return new(t=function(){function t(){}return t.prototype.save=function(t){var i;return i=void 0!==t.key?t.put():e.service("tenants").post(t)},t.prototype.fetchAllTenants=function(){var t;return t=e.all("tenants").getList()},t.prototype.getTenantByKey=function(t){var i;return i=e.oneUrl("tenants","api/v1/tenants/"+t).get()},t.prototype["delete"]=function(t){var i;return void 0!==t.key?i=e.one("tenants",t.key).remove():void 0},t}())}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").factory("DevicesService",["$http","$log","Restangular",function(e,t,i){var a;return new(a=function(){function e(){}return e.uriBase="v1/devices",e.prototype.getDeviceByMacAddress=function(e){return i.oneUrl("api/v1/devices","api/v1/devices?mac_address="+e).get()},e.prototype.getDeviceByKey=function(e){var t;return t=i.oneUrl("devices","api/v1/devices/"+e).get()},e.prototype.getDevicesByTenant=function(e){var t;return void 0!==e?t=i.one("tenants",e).doGET("devices"):void 0},e}())}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("TenantsCtrl",["$state","TenantsService",function(e,t){return this.tenants=[],this.initialize=function(){var e;return e=t.fetchAllTenants(),e.then(function(e){return function(t){return e.tenants=t}}(this))},this.editItem=function(t){return e.go("editTenant",{tenantKey:t.key})},this.deleteItem=function(e){return function(i){var a;return a=t["delete"](i),a.then(function(){return e.initialize()})}}(this),this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("TenantDetailsCtrl",["$stateParams","TenantsService","DevicesService","$state",function(e,t,i,a){var n,r;return this.currentTenant={key:void 0,name:void 0,tenant_code:void 0,admin_email:void 0,content_server_url:void 0,chrome_device_domain:void 0,active:!0},this.currentTenantDevices=[],this.editMode=!!e.tenantKey,this.editMode&&(r=t.getTenantByKey(e.tenantKey),r.then(function(e){return function(t){return e.currentTenant=t}}(this)),n=i.getDevicesByTenant(e.tenantKey),n.then(function(e){return function(t){return e.currentTenantDevices=t}}(this))),this.onClickSaveButton=function(){var e;return e=t.save(this.currentTenant),e.then(function(){return a.go("tenants")})},this.autoGenerateTenantCode=function(){var e;return this.currentTenant.key?void 0:(e="",this.currentTenant.name&&(e=this.currentTenant.name.toLowerCase(),e=e.replace(/\s+/g,"_"),e=e.replace(/\W+/g,"")),this.currentTenant.tenant_code=e)},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("RemoteControlCtrl",["DevicesService",function(){return this.devices=[],this.currentDevice={id:void 0,name:void 0},this.initialize=function(){return this.devices=[{id:1,name:"Device 1"},{id:2,name:"Device 2"},{id:3,name:"Device 3"},{id:4,name:"Device 4"}]},this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("MainCtrl",["$scope",function(e){return e.awesomeThings=[1,2,3,4,5,6],this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("DomainCtrl",["$scope",function(){return this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("DeviceEditorCtrl",["$scope","$log","sweet","DevicesService",function(e,t,i){return this.onClickSaveButton=function(){return i.show("Sweet Jebus","You've done it!","success")},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("DeviceDetailsCtrl",["$stateParams","DevicesService",function(e,t){var i;return this.currentDevice={key:void 0,gcmRegistrationId:void 0,annotatedUser:void 0,apiKey:void 0,deviceId:void 0,bootMode:void 0,chromeDeviceDomain:void 0,contentServerUrl:void 0,etag:void 0,ethernetMacAddress:void 0,macAddress:void 0,firmwareVersion:void 0,kind:void 0,lastEnrollmentTime:void 0,lastSync:void 0,model:void 0,orgUnitPath:void 0,osVersion:void 0,platformVersion:void 0,serialNumber:void 0,status:void 0,tenantCode:void 0,created:void 0,updated:void 0},this.editMode=!!e.deviceKey,this.editMode&&(i=t.getDeviceByKey(e.deviceKey),i.then(function(e){return function(t){return e.currentDevice=t}}(this))),this.onClickSaveButton=function(){},this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("ApiTestCtrl",["$scope","$log","sweet","DevicesService",function(e,t,i,a){return this.macAddress=void 0,this.onClickFindByMacAddressButton=function(){var e;return e=a.getDeviceByMacAddress(this.macAddress),i.show("Success!",JSON.stringify(e),"success")},this}])}.call(this),angular.module("skykitDisplayDeviceManagement").run(["$templateCache",function(e){e.put("app/api_test/api_test.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">API testing</h1></div></div><div class="row"><div class="col-lg-12"><fieldset><legend>Find device by MAC address</legend><form><div class="form-group"><label for="macAddress">MAC address</label> <input type="text" class="form-control" id="macAddress" placeholder="Enter MAC address" ng_model="apiTest.macAddress"></div><button type="submit" class="btn btn-primary btn-default" ng-click="apiTest.onClickFindByMacAddressButton()">Query</button></form></fieldset></div></div></div></div></div>'),e.put("app/device/device-detail.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Device key: {{ deviceDetailsCtrl.currentDevice.key | limitTo: 10 }}...{{ deviceDetailsCtrl.currentDevice.key | limitTo: 10 : deviceDetailsCtrl.currentDevice.key.length - 10}}</h1></div></div><div><tabset><tab heading="General"><div style="margin-top: 1px;">&nbsp;</div><div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Device properties</h3></div><div class="panel-body"><form name="deviceForm" class="form-horizontal" ng-submit="deviceDetailsCtrl.onClickSaveButton()" novalidate=""><div class="form-group" ng-class="{ \'has-error\' : deviceForm.key.$invalid && !deviceForm.key.$pristine }"><label for="key" class="col-sm-3 control-label">Key</label><div class="col-sm-9"><input type="text" class="form-control" name="key" id="key" readonly="" value="{{ deviceDetailsCtrl.currentDevice.key }}"></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.serialNumber.$invalid && !deviceForm.serialNumber.$pristine }"><label for="serialNumber" class="col-sm-3 control-label">Serial number</label><div class="col-sm-4"><input type="text" class="form-control" name="serialNumber" id="serialNumber" readonly="" ng-model="deviceDetailsCtrl.currentDevice.serialNumber"></div><div class="col-sm-5"><p ng-show="deviceForm.serialNumber.$invalid && !deviceForm.serialNumber.$pristine" class="help-block">The device serial number is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.gcmRegistrationId.$invalid && !deviceForm.gcmRegistrationId.$pristine }"><label for="gcmRegistrationId" class="col-sm-3 control-label">GCM registration ID</label><div class="col-sm-4"><input type="text" class="form-control" name="gcmRegistrationId" id="gcmRegistrationId" readonly="" ng-model="deviceDetailsCtrl.currentDevice.gcmRegistrationId"></div><div class="col-sm-5"><p ng-show="deviceForm.gcmRegistrationId.$invalid && !deviceForm.gcmRegistrationId.$pristine" class="help-block">The device GCM registration ID is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.annotatedUser.$invalid && !deviceForm.annotatedUser.$pristine }"><label for="annotatedUser" class="col-sm-3 control-label">Annotated user</label><div class="col-sm-4"><input type="text" class="form-control" name="annotatedUser" id="annotatedUser" readonly="" ng-model="deviceDetailsCtrl.currentDevice.annotatedUser"></div><div class="col-sm-5"><p ng-show="deviceForm.annotatedUser.$invalid && !deviceForm.annotatedUser.$pristine" class="help-block">The device annotated user is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.apiKey.$invalid && !deviceForm.apiKey.$pristine }"><label for="apiKey" class="col-sm-3 control-label">API key</label><div class="col-sm-4"><input type="text" class="form-control" name="apiKey" id="apiKey" readonly="" ng-model="deviceDetailsCtrl.currentDevice.apiKey"></div><div class="col-sm-5"><p ng-show="deviceForm.apiKey.$invalid && !deviceForm.apiKey.$pristine" class="help-block">The device API key is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.deviceId.$invalid && !deviceForm.deviceId.$pristine }"><label for="deviceId" class="col-sm-3 control-label">Device ID</label><div class="col-sm-4"><input type="text" class="form-control" name="deviceId" id="deviceId" readonly="" ng-model="deviceDetailsCtrl.currentDevice.deviceId"></div><div class="col-sm-5"><p ng-show="deviceForm.deviceId.$invalid && !deviceForm.deviceId.$pristine" class="help-block">The device ID is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.bootMode.$invalid && !deviceForm.bootMode.$pristine }"><label for="bootMode" class="col-sm-3 control-label">Boot mode</label><div class="col-sm-4"><input type="text" class="form-control" name="bootMode" id="bootMode" readonly="" ng-model="deviceDetailsCtrl.currentDevice.bootMode"></div><div class="col-sm-5"><p ng-show="deviceForm.bootMode.$invalid && !deviceForm.bootMode.$pristine" class="help-block">The device boot mode is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.chromeDeviceDomain.$invalid && !deviceForm.chromeDeviceDomain.$pristine }"><label for="chromeDeviceDomain" class="col-sm-3 control-label">Chrome device domain</label><div class="col-sm-4"><input type="text" class="form-control" name="chromeDeviceDomain" id="chromeDeviceDomain" readonly="" ng-model="deviceDetailsCtrl.currentDevice.chromeDeviceDomain"></div><div class="col-sm-5"><p ng-show="deviceForm.chromeDeviceDomain.$invalid && !deviceForm.chromeDeviceDomain.$pristine" class="help-block">The Chrome device domain is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.contentServerUrl.$invalid && !deviceForm.contentServerUrl.$pristine }"><label for="contentServerUrl" class="col-sm-3 control-label">Content server URL</label><div class="col-sm-4"><input type="text" class="form-control" name="contentServerUrl" id="contentServerUrl" readonly="" ng-model="deviceDetailsCtrl.currentDevice.contentServerUrl"></div><div class="col-sm-5"><p ng-show="deviceForm.contentServerUrl.$invalid && !deviceForm.contentServerUrl.$pristine" class="help-block">The device content server URL is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.etag.$invalid && !deviceForm.etag.$pristine }"><label for="etag" class="col-sm-3 control-label">Etag</label><div class="col-sm-4"><input type="text" class="form-control" name="etag" id="etag" readonly="" ng-model="deviceDetailsCtrl.currentDevice.etag"></div><div class="col-sm-5"><p ng-show="deviceForm.etag.$invalid && !deviceForm.etag.$pristine" class="help-block">The device Etag is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.ethernetMacAddress.$invalid && !deviceForm.ethernetMacAddress.$pristine }"><label for="ethernetMacAddress" class="col-sm-3 control-label">Ethernet MAC address</label><div class="col-sm-4"><input type="text" class="form-control" name="ethernetMacAddress" id="ethernetMacAddress" readonly="" ng-model="deviceDetailsCtrl.currentDevice.ethernetMacAddress"></div><div class="col-sm-5"><p ng-show="deviceForm.ethernetMacAddress.$invalid && !deviceForm.ethernetMacAddress.$pristine" class="help-block">The device ethernet MAC address is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.macAddress.$invalid && !deviceForm.macAddress.$pristine }"><label for="macAddress" class="col-sm-3 control-label">MAC address</label><div class="col-sm-4"><input type="text" class="form-control" name="macAddress" id="macAddress" readonly="" ng-model="deviceDetailsCtrl.currentDevice.macAddress"></div><div class="col-sm-5"><p ng-show="deviceForm.macAddress.$invalid && !deviceForm.macAddress.$pristine" class="help-block">The device MAC address is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.firmwareVersion.$invalid && !deviceForm.firmwareVersion.$pristine }"><label for="firmwareVersion" class="col-sm-3 control-label">Firmware version</label><div class="col-sm-4"><input type="text" class="form-control" name="firmwareVersion" id="firmwareVersion" readonly="" ng-model="deviceDetailsCtrl.currentDevice.firmwareVersion"></div><div class="col-sm-5"><p ng-show="deviceForm.firmwareVersion.$invalid && !deviceForm.firmwareVersion.$pristine" class="help-block">The device firmware version is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.kind.$invalid && !deviceForm.kind.$pristine }"><label for="kind" class="col-sm-3 control-label">Kind</label><div class="col-sm-4"><input type="text" class="form-control" name="kind" id="kind" readonly="" ng-model="deviceDetailsCtrl.currentDevice.kind"></div><div class="col-sm-5"><p ng-show="deviceForm.kind.$invalid && !deviceForm.kind.$pristine" class="help-block">The device kind is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.lastEnrollmentTime.$invalid && !deviceForm.lastEnrollmentTime.$pristine }"><label for="lastEnrollmentTime" class="col-sm-3 control-label">Last enrollment timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="lastEnrollmentTime" id="lastEnrollmentTime" readonly="" ng-model="deviceDetailsCtrl.currentDevice.lastEnrollmentTime"></div><div class="col-sm-5"><p ng-show="deviceForm.lastEnrollmentTime.$invalid && !deviceForm.lastEnrollmentTime.$pristine" class="help-block">The device last enrollment timestamp is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.lastSync.$invalid && !deviceForm.lastSync.$pristine }"><label for="lastSync" class="col-sm-3 control-label">Last sync timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="lastSync" id="lastSync" readonly="" ng-model="deviceDetailsCtrl.currentDevice.lastSync"></div><div class="col-sm-5"><p ng-show="deviceForm.lastSync.$invalid && !deviceForm.lastSync.$pristine" class="help-block">The device last sync timestamp is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.model.$invalid && !deviceForm.model.$pristine }"><label for="model" class="col-sm-3 control-label">Model</label><div class="col-sm-4"><input type="text" class="form-control" name="model" id="model" readonly="" ng-model="deviceDetailsCtrl.currentDevice.model"></div><div class="col-sm-5"><p ng-show="deviceForm.model.$invalid && !deviceForm.model.$pristine" class="help-block">The device model is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.orgUnitPath.$invalid && !deviceForm.orgUnitPath.$pristine }"><label for="orgUnitPath" class="col-sm-3 control-label">Organizational unit path</label><div class="col-sm-4"><input type="text" class="form-control" name="orgUnitPath" id="orgUnitPath" readonly="" ng-model="deviceDetailsCtrl.currentDevice.orgUnitPath"></div><div class="col-sm-5"><p ng-show="deviceForm.orgUnitPath.$invalid && !deviceForm.orgUnitPath.$pristine" class="help-block">The device organizational unit path is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.osVersion.$invalid && !deviceForm.osVersion.$pristine }"><label for="osVersion" class="col-sm-3 control-label">Operating system version</label><div class="col-sm-4"><input type="text" class="form-control" name="osVersion" id="osVersion" readonly="" ng-model="deviceDetailsCtrl.currentDevice.osVersion"></div><div class="col-sm-5"><p ng-show="deviceForm.osVersion.$invalid && !deviceForm.osVersion.$pristine" class="help-block">The device OS version is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.platformVersion.$invalid && !deviceForm.platformVersion.$pristine }"><label for="platformVersion" class="col-sm-3 control-label">Platform version</label><div class="col-sm-4"><input type="text" class="form-control" name="platformVersion" id="platformVersion" readonly="" ng-model="deviceDetailsCtrl.currentDevice.platformVersion"></div><div class="col-sm-5"><p ng-show="deviceForm.platformVersion.$invalid && !deviceForm.platformVersion.$pristine" class="help-block">The device platform version is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.status.$invalid && !deviceForm.status.$pristine }"><label for="status" class="col-sm-3 control-label">Status</label><div class="col-sm-4"><input type="text" class="form-control" name="status" id="status" readonly="" ng-model="deviceDetailsCtrl.currentDevice.status"></div><div class="col-sm-5"><p ng-show="deviceForm.status.$invalid && !deviceForm.status.$pristine" class="help-block">The device status is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.tenantCode.$invalid && !deviceForm.tenantCode.$pristine }"><label for="tenantCode" class="col-sm-3 control-label">Tenant code</label><div class="col-sm-4"><input type="text" class="form-control" name="tenantCode" id="tenantCode" readonly="" ng-model="deviceDetailsCtrl.currentDevice.tenantCode"></div><div class="col-sm-5"><p ng-show="deviceForm.tenantCode.$invalid && !deviceForm.tenantCode.$pristine" class="help-block">The device tenant code is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.created.$invalid && !deviceForm.created.$pristine }"><label for="created" class="col-sm-3 control-label">Created timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="created" id="created" readonly="" ng-model="deviceDetailsCtrl.currentDevice.created"></div><div class="col-sm-5"><p ng-show="deviceForm.created.$invalid && !deviceForm.created.$pristine" class="help-block">The device created timestamp is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : deviceForm.updated.$invalid && !deviceForm.updated.$pristine }"><label for="updated" class="col-sm-3 control-label">Updated timestamp</label><div class="col-sm-4"><input type="text" class="form-control" name="updated" id="updated" readonly="" ng-model="deviceDetailsCtrl.currentDevice.updated"></div><div class="col-sm-5"><p ng-show="deviceForm.updated.$invalid && !deviceForm.updated.$pristine" class="help-block">The device updated timestamp is required.</p></div></div></form></div></div></tab></tabset></div></div></div></div>'),e.put("app/device/device.editor.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Domain <small>Subtitle</small></h1></div></div><div class="row"><div class="col-lg-12"><fieldset><legend>Device</legend><form><div class="form-group"><label for="device-name">Device name</label> <input type="text" class="form-control" id="device-name" placeholder="Enter device name"></div><div class="form-group"><label for="device-location">Location</label> <input type="text" class="form-control" id="device-location" placeholder="Enter location"></div><div class="form-group"><label for="mac-address">MAC address</label> <input type="text" class="form-control" id="mac-address" placeholder="Enter MAC address"></div><div class="form-group"><label for="device-id">Device ID</label> <input type="text" class="form-control" id="device-id" placeholder="Enter device ID"></div><button type="submit" class="btn btn-primary btn-default" ng-click="deviceEdit.onClickSaveButton()">Save</button></form></fieldset></div></div></div></div></div>'),e.put("app/domain/domain.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Device <small>Subtitle</small></h1></div></div><div class="row"><div class="col-lg-12"><fieldset><legend>Devices</legend><div class="col-md-12 toolbar"><a id="button-add-device" class="btn btn-default btn-success" href="#/deviceEdit"><i class="glyphicon glyphicon-plus"></i> Add device</a></div><table class="table table-bordered table-responsive table-striped"><thead><tr><th>Name</th><th>Location</th><th>MAC address</th><th>Device ID</th></tr></thead><tbody><tr><td>Test ChromeOS device 001</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 002</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 003</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 004</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr></tbody></table></fieldset></div></div></div></div></div>'),e.put("app/main/main.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Skykit Provisioning</h1></div></div></div></div></div>'),e.put("app/remote_control/index.html",'<div id="wrapper" ng-init="remoteControlCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Remote control</h1></div></div><div class="row" data-ng-controller="RemoteControlCtrl"><div class="col-lg-4"><label for="device">Choose a device:</label><select id="device" data-ng-model="remoteControlCtrl.currentDevice" data-ng-options="c.name for c in remoteControlCtrl.devices"><option value="">Select device</option></select></div><div class="col-lg-8"><div ng-show="remoteControlCtrl.currentDevice.name != undefined">selected device: {{ remoteControlCtrl.currentDevice}}</div></div></div></div></div></div>'),e.put("app/tenant/tenant-detail.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">{{ tenantDetailsCtrl.currentTenant.name }}</h1></div></div><div><tabset><tab heading="General"><div style="margin-top: 1px;">&nbsp;</div><div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Tenant properties</h3></div><div class="panel-body"><form name="tenantForm" class="form-horizontal" ng-submit="tenantDetailsCtrl.onClickSaveButton()" novalidate=""><div class="form-group" ng-class="{ \'has-error\' : tenantForm.name.$invalid && !tenantForm.name.$pristine }"><label for="name" class="col-sm-2 control-label">Name</label><div class="col-sm-4"><input type="text" class="form-control" name="name" id="name" required="" placeholder="Enter tenant name" ng-model="tenantDetailsCtrl.currentTenant.name" ng-change="tenantDetailsCtrl.autoGenerateTenantCode()" autofocus=""></div><div class="col-sm-6"><p ng-show="tenantForm.name.$invalid && !tenantForm.name.$pristine" class="help-block">The tenant name is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.tenantCode.$invalid && !tenantForm.tenantCode.$pristine }"><label for="tenantCode" class="col-sm-2 control-label">Tenant code</label><div class="col-sm-4"><input type="text" class="form-control" name="tenantCode" id="tenantCode" required="" placeholder="Enter tenant code (must match tenant code in Google Device Management)" ng-model="tenantDetailsCtrl.currentTenant.tenant_code"></div><div class="col-sm-6"><p ng-show="tenantForm.tenantCode.$invalid && !tenantForm.tenantCode.$pristine" class="help-block">The tenant lookup code is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.adminEmail.$invalid && !tenantForm.adminEmail.$pristine }"><label for="adminEmail" class="col-sm-2 control-label">Admin email address</label><div class="col-sm-4"><input type="text" required="" class="form-control" name="adminEmail" id="adminEmail" placeholder="Enter admin email" ng-model="tenantDetailsCtrl.currentTenant.admin_email"></div><div class="col-sm-6"><p ng-show="tenantForm.adminEmail.$invalid && !tenantForm.adminEmail.$pristine" class="help-block">The tenant admin email address is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.chromeDeviceDomain.$invalid && !tenantForm.chromeDeviceDomain.$pristine }"><label for="chromeDeviceDomain" class="col-sm-2 control-label">Chrome device domain</label><div class="col-sm-4"><input type="text" required="" class="form-control" name="chromeDeviceDomain" id="chromeDeviceDomain" placeholder="Enter Chrome device domain" ng-model="tenantDetailsCtrl.currentTenant.chrome_device_domain"></div><div class="col-sm-6"><p ng-show="tenantForm.chromeDeviceDomain.$invalid && !tenantForm.chromeDeviceDomain.$pristine" class="help-block">The Chrome device domain is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.contentServerUrl.$invalid && !tenantForm.contentServerUrl.$pristine }"><label for="contentServerUrl" class="col-sm-2 control-label">Content server URL</label><div class="col-sm-4"><input type="url" required="" class="form-control" name="contentServerUrl" id="contentServerUrl" placeholder="Enter content server URL" ng-model="tenantDetailsCtrl.currentTenant.content_server_url" ng-pattern="/^https:\\/\\/\\S+$/"></div><div class="col-sm-6"><p ng-show="tenantForm.contentServerUrl.$invalid && !tenantForm.contentServerUrl.$pristine" class="help-block">The content server URL is required to be a secure URL.</p></div></div><div class="form-group"><div class="col-sm-offset-2 col-sm-6"><input type="checkbox" id="active" ng-model="tenantDetailsCtrl.currentTenant.active"> <label for="active">Active</label></div></div><hr><div class="form-group"><div class="col-sm-offset-2 col-sm-10"><button type="submit" class="btn btn-primary btn-default" ng-disabled="tenantForm.$invalid"><i class="fa fa-fw fa-save"></i> Save</button></div></div></form></div></div></tab><tab heading="Linked devices"><div style="margin-top: 1px;">&nbsp;</div><div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Devices</h3></div><div class="panel-body"><table name="tenant-devices-table" class="table table-bordered table-condensed table-responsive table-striped"><thead><tr><th>Key</th><th>Device ID</th><th>MAC address</th></tr></thead><tbody><tr ng-hide="tenantDetailsCtrl.currentTenantDevices.length"><td name="no-tenants" colspan="3" class="text-center text-danger">No devices</td></tr><tr ng-repeat="device in tenantDetailsCtrl.currentTenantDevices | orderBy:\'-created\'"><td class="tenant-device-key"><a href="#/devices/{{ device.key }}"><span class="entity-key">{{ device.key | limitTo: 10 }}...{{ device.key | limitTo: 10 : device.key.length - 10}}</span></a></td><td class="tenant-device-id">{{ device.device_id }}</td><td class="tenant-device-mac-address">{{ device.macAddress }}</td></tr></tbody></table></div></div></tab></tabset></div></div></div></div>'),e.put("app/tenant/tenants.html",'<div id="wrapper" ng-init="tenantsCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Tenants</h1></div></div><div class="row"><div class="col-lg-12"><div class="col-md-12 toolbar"><a id="button-add-tenant" class="btn btn-success" href="#/tenants/new"><i class="fa fa-fw fa-plus"></i> Add tenant</a></div><table name="tenant-table" class="table table-bordered table-responsive table-striped"><thead><tr><th>Name</th><th>Email</th><th>Content Server URL</th><th></th></tr></thead><tbody><tr ng-hide="tenantsCtrl.tenants.length"><td name="no-tenants" colspan="5">No tenants</td></tr><tr ng-repeat="item in tenantsCtrl.tenants | orderBy:\'-created\'"><td class="tenant-name">{{item.name}}</td><td class="tenant-admin-email">{{item.admin_email}}</td><td class="content-server-url">{{item.content_server_url}}</td><td class="text-center"><a name="edit-tenant" class="btn" ng-click="tenantsCtrl.editItem(item)" title="Edit tenant"><i class="fa fa-fw fa-edit"></i></a> <a name="delete-tenant" class="btn" ng-click="tenantsCtrl.deleteItem(item)" title="Delete tenant"><i class="fa fa-fw fa-trash"></i></a></td></tr></tbody></table></div></div></div></div></div>'),e.put("app/components/navbar/navbar.html",'<nav class="navbar navbar-default navbar-fixed-top" role="navigation"><div class="navbar-header"><button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse"><span class="sr-only">Toggle navigation</span> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span></button> <a class="navbar-brand" href="/"><img src="assets/images/skykit_logo2.png"></a></div><ul class="nav navbar-right top-nav"></ul><div class="collapse navbar-collapse navbar-ex1-collapse"><ul class="nav navbar-nav side-nav"><li><a id="navbar-tenants" href="#/tenants"><i class="fa fa-fw fa-users"></i> Tenants</a></li><li><a id="navbar-remote_control" href="#/remote_control"><i class="fa fa-fw fa-building"></i> Remote control</a></li></ul></div></nav>')
}]);