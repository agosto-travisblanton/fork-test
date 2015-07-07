(function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement",["ngAnimate","ngCookies","ngTouch","ngSanitize","restangular","ui.router","hSweetAlert","ui.bootstrap"]),e.config(["$stateProvider","$urlRouterProvider","RestangularProvider",function(e,t,n){return e.state("home",{url:"/",templateUrl:"app/main/main.html",controller:"MainCtrl"}),e.state("domain",{url:"/domain",templateUrl:"app/domain/domain.html",controller:"DomainCtrl"}),e.state("deviceEdit",{url:"/deviceEdit",templateUrl:"app/device/device.editor.html",controller:"DeviceEditorCtrl",controllerAs:"deviceEdit"}),e.state("tenants",{url:"/tenants",templateUrl:"app/tenant/tenants.html",controller:"TenantsCtrl",controllerAs:"tenantsCtrl"}),e.state("newTenant",{url:"/tenants/new",templateUrl:"app/tenant/tenant-detail.html",controller:"TenantDetailsCtrl",controllerAs:"tenantDetailsCtrl"}),e.state("editTenant",{url:"/tenants/:tenantKey",templateUrl:"app/tenant/tenant-detail.html",controller:"TenantDetailsCtrl",controllerAs:"tenantDetailsCtrl"}),e.state("apiTest",{url:"/api_testing",templateUrl:"app/api_test/api_test.html",controller:"ApiTestCtrl",controllerAs:"apiTest"}),e.state("remote_control",{url:"/remote_control",templateUrl:"app/remote_control/index.html",controller:"RemoteControlCtrl",controllerAs:"remoteControlCtrl"}),t.otherwise("/"),n.setBaseUrl("/api/v1"),n.setDefaultHeaders({"Content-Type":"application/json",Accept:"application/json",Authorization:"6C346588BD4C6D722A1165B43C51C"}),n.addRequestInterceptor(function(e,t){return"remove"===t?void 0:e}),n.setRestangularFields({id:"key"})}])}).call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("NavbarCtrl",["$scope",function(){}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("TenantsCtrl",["$state","TenantsService",function(e,t){return this.tenants=[],this.initialize=function(){var e;return e=t.fetchAllTenants(),e.then(function(e){return function(t){return e.tenants=t}}(this))},this.editItem=function(t){return e.go("editTenant",{tenantKey:t.key})},this.deleteItem=function(e){return function(n){var a;return a=t["delete"](n),a.then(function(){return e.initialize()})}}(this),this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("TenantDetailsCtrl",["$stateParams","TenantsService","DevicesService","$state",function(e,t,n,a){var i,r;return this.currentTenant={key:void 0,name:void 0,tenant_code:void 0,admin_email:void 0,content_server_url:void 0,chrome_device_domain:void 0,active:!0},this.currentTenantDevices=[],this.editMode=!!e.tenantKey,this.editMode&&(r=t.getTenantByKey(e.tenantKey),r.then(function(e){return function(t){return e.currentTenant=t}}(this)),i=n.getDevicesByTenant(e.tenantKey),i.then(function(e){return function(t){return e.currentTenantDevices=t}}(this))),this.onClickSaveButton=function(){var e;return e=t.save(this.currentTenant),e.then(function(){return a.go("tenants")})},this.autoGenerateTenantCode=function(){var e;return this.currentTenant.key?void 0:(e="",this.currentTenant.name&&(e=this.currentTenant.name.toLowerCase(),e=e.replace(/\s+/g,"_"),e=e.replace(/\W+/g,"")),this.currentTenant.tenant_code=e)},this}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.factory("TenantsService",["Restangular",function(e){var t;return new(t=function(){function t(){}return t.prototype.save=function(t){var n;return n=void 0!==t.key?t.put():e.service("tenants").post(t)},t.prototype.fetchAllTenants=function(){var t;return t=e.all("tenants").getList()},t.prototype.getTenantByKey=function(t){var n;return n=e.oneUrl("tenants","api/v1/tenants/"+t).get()},t.prototype["delete"]=function(t){var n;return void 0!==t.key?n=e.one("tenants",t.key).remove():void 0},t}())}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").factory("DevicesService",["$http","$log","Restangular",function(e,t,n){var a;return new(a=function(){function e(){}return e.uriBase="v1/devices",e.prototype.getDeviceByMacAddress=function(e){return n.oneUrl("api/v1/devices","api/v1/devices?mac_address="+e).get()},e.prototype.getDeviceList=function(){},e.prototype.getDevicesByTenant=function(e){var t;return void 0!==e?t=n.one("tenants",e).doGET("devices"):void 0},e}())}])}.call(this),function(){"use strict";var e;e=angular.module("skykitDisplayDeviceManagement"),e.controller("RemoteControlCtrl",["DevicesService",function(){return this.devices=[],this.currentDevice={id:void 0,name:void 0},this.initialize=function(){return this.devices=[{id:1,name:"Device 1"},{id:2,name:"Device 2"},{id:3,name:"Device 3"},{id:4,name:"Device 4"}]},this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("MainCtrl",["$scope",function(e){return e.awesomeThings=[1,2,3,4,5,6],this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("DomainCtrl",["$scope",function(){return this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("DeviceEditorCtrl",["$scope","$log","sweet","DevicesService",function(e,t,n){return this.onClickSaveButton=function(){return n.show("Sweet Jebus","You've done it!","success")},this}])}.call(this),function(){"use strict";angular.module("skykitDisplayDeviceManagement").controller("ApiTestCtrl",["$scope","$log","sweet","DevicesService",function(e,t,n,a){return this.macAddress=void 0,this.onClickFindByMacAddressButton=function(){var e;return e=a.getDeviceByMacAddress(this.macAddress),n.show("Success!",JSON.stringify(e),"success")},this}])}.call(this),angular.module("skykitDisplayDeviceManagement").run(["$templateCache",function(e){e.put("app/api_test/api_test.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">API testing</h1></div></div><div class="row"><div class="col-lg-12"><fieldset><legend>Find device by MAC address</legend><form><div class="form-group"><label for="macAddress">MAC address</label> <input type="text" class="form-control" id="macAddress" placeholder="Enter MAC address" ng_model="apiTest.macAddress"></div><button type="submit" class="btn btn-primary btn-default" ng-click="apiTest.onClickFindByMacAddressButton()">Query</button></form></fieldset></div></div></div></div></div>'),e.put("app/device/device.editor.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Domain <small>Subtitle</small></h1></div></div><div class="row"><div class="col-lg-12"><fieldset><legend>Device</legend><form><div class="form-group"><label for="device-name">Device name</label> <input type="text" class="form-control" id="device-name" placeholder="Enter device name"></div><div class="form-group"><label for="device-location">Location</label> <input type="text" class="form-control" id="device-location" placeholder="Enter location"></div><div class="form-group"><label for="mac-address">MAC address</label> <input type="text" class="form-control" id="mac-address" placeholder="Enter MAC address"></div><div class="form-group"><label for="device-id">Device ID</label> <input type="text" class="form-control" id="device-id" placeholder="Enter device ID"></div><button type="submit" class="btn btn-primary btn-default" ng-click="deviceEdit.onClickSaveButton()">Save</button></form></fieldset></div></div></div></div></div>'),e.put("app/domain/domain.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Device <small>Subtitle</small></h1></div></div><div class="row"><div class="col-lg-12"><fieldset><legend>Devices</legend><div class="col-md-12 toolbar"><a id="button-add-device" class="btn btn-default btn-success" href="#/deviceEdit"><i class="glyphicon glyphicon-plus"></i> Add device</a></div><table class="table table-bordered table-responsive table-striped"><thead><tr><th>Name</th><th>Location</th><th>MAC address</th><th>Device ID</th></tr></thead><tbody><tr><td>Test ChromeOS device 001</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 002</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 003</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr><tr><td>Test ChromeOS device 004</td><td>Mars Landing</td><td>01:23:45:67:89:ab</td><td>d67786976dfsd87765</td></tr></tbody></table></fieldset></div></div></div></div></div>'),e.put("app/main/main.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Skykit Provisioning</h1></div></div></div></div></div>'),e.put("app/tenant/tenant-detail.html",'<div id="wrapper"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">{{ tenantDetailsCtrl.currentTenant.name }}</h1></div></div><div><tabset><tab heading="General"><div style="margin-top: 1px;">&nbsp;</div><div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Tenant properties</h3></div><div class="panel-body"><form name="tenantForm" class="form-horizontal" ng-submit="tenantDetailsCtrl.onClickSaveButton()" novalidate=""><div class="form-group" ng-class="{ \'has-error\' : tenantForm.name.$invalid && !tenantForm.name.$pristine }"><label for="name" class="col-sm-2 control-label">Name</label><div class="col-sm-4"><input type="text" class="form-control" name="name" id="name" required="" placeholder="Enter tenant name" ng-model="tenantDetailsCtrl.currentTenant.name" ng-change="tenantDetailsCtrl.autoGenerateTenantCode()" autofocus=""></div><div class="col-sm-6"><p ng-show="tenantForm.name.$invalid && !tenantForm.name.$pristine" class="help-block">The tenant name is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.tenantCode.$invalid && !tenantForm.tenantCode.$pristine }"><label for="tenantCode" class="col-sm-2 control-label">Tenant code</label><div class="col-sm-4"><input type="text" class="form-control" name="tenantCode" id="tenantCode" required="" placeholder="Enter tenant code (must match tenant code in Google Device Management)" ng-model="tenantDetailsCtrl.currentTenant.tenant_code"></div><div class="col-sm-6"><p ng-show="tenantForm.tenantCode.$invalid && !tenantForm.tenantCode.$pristine" class="help-block">The tenant lookup code is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.adminEmail.$invalid && !tenantForm.adminEmail.$pristine }"><label for="adminEmail" class="col-sm-2 control-label">Admin email address</label><div class="col-sm-4"><input type="text" required="" class="form-control" name="adminEmail" id="adminEmail" placeholder="Enter admin email" ng-model="tenantDetailsCtrl.currentTenant.admin_email"></div><div class="col-sm-6"><p ng-show="tenantForm.adminEmail.$invalid && !tenantForm.adminEmail.$pristine" class="help-block">The tenant admin email address is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.chromeDeviceDomain.$invalid && !tenantForm.chromeDeviceDomain.$pristine }"><label for="chromeDeviceDomain" class="col-sm-2 control-label">Chrome device domain</label><div class="col-sm-4"><input type="text" required="" class="form-control" name="chromeDeviceDomain" id="chromeDeviceDomain" placeholder="Enter Chrome device domain" ng-model="tenantDetailsCtrl.currentTenant.chrome_device_domain"></div><div class="col-sm-6"><p ng-show="tenantForm.chromeDeviceDomain.$invalid && !tenantForm.chromeDeviceDomain.$pristine" class="help-block">The Chrome device domain is required.</p></div></div><div class="form-group" ng-class="{ \'has-error\' : tenantForm.contentServerUrl.$invalid && !tenantForm.contentServerUrl.$pristine }"><label for="contentServerUrl" class="col-sm-2 control-label">Content server URL</label><div class="col-sm-4"><input type="text" required="" class="form-control" name="contentServerUrl" id="contentServerUrl" placeholder="Enter content server URL" ng-model="tenantDetailsCtrl.currentTenant.content_server_url"></div><div class="col-sm-6"><p ng-show="tenantForm.contentServerUrl.$invalid && !tenantForm.contentServerUrl.$pristine" class="help-block">The content server URL is required.</p></div></div><div class="form-group"><div class="col-sm-offset-2 col-sm-6"><input type="checkbox" id="active" ng-model="tenantDetailsCtrl.currentTenant.active"> <label for="active">Active</label></div></div><hr><div class="form-group"><div class="col-sm-offset-2 col-sm-10"><button type="submit" class="btn btn-primary btn-default" ng-disabled="tenantForm.$invalid"><i class="fa fa-fw fa-save"></i> Save</button></div></div></form></div></div></tab><tab heading="Linked devices"><div style="margin-top: 1px;">&nbsp;</div><div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Devices</h3></div><div class="panel-body"><table name="tenant-devices-table" class="table table-bordered table-condensed table-responsive table-striped"><thead><tr><th>Key</th><th>Device ID</th><th>MAC address</th></tr></thead><tbody><tr ng-hide="tenantDetailsCtrl.currentTenantDevices.length"><td name="no-tenants" colspan="" class="text-center text-danger">No devices</td></tr><tr ng-repeat="device in tenantDetailsCtrl.currentTenantDevices | orderBy:\'-created\'"><td class="tenant-device-key"><code>\n                                            {{ device.key | limitTo: 10 }}...{{ device.key | limitTo: 10 : device.key.length - 10}}\n                                          </code></td><td class="tenant-device-id">{{ device.device_id }}</td><td class="tenant-device-mac-address"></td><td class="text-center"></td></tr></tbody></table></div></div></tab></tabset></div></div></div></div>'),e.put("app/tenant/tenants.html",'<div id="wrapper" ng-init="tenantsCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Tenants</h1></div></div><div class="row"><div class="col-lg-12"><div class="col-md-12 toolbar"><a id="button-add-tenant" class="btn btn-success" href="#/tenants/new"><i class="fa fa-fw fa-plus"></i> Add tenant</a></div><table name="tenant-table" class="table table-bordered table-responsive table-striped"><thead><tr><th>Name</th><th>Email</th><th>Content Server URL</th><th></th></tr></thead><tbody><tr ng-hide="tenantsCtrl.tenants.length"><td name="no-tenants" colspan="5">No tenants</td></tr><tr ng-repeat="item in tenantsCtrl.tenants | orderBy:\'-created\'"><td class="tenant-name">{{item.name}}</td><td class="tenant-admin-email">{{item.admin_email}}</td><td class="content-server-url">{{item.content_server_url}}</td><td class="text-center"><a name="edit-tenant" class="btn" ng-click="tenantsCtrl.editItem(item)" title="Edit tenant"><i class="fa fa-fw fa-edit"></i></a> <a name="delete-tenant" class="btn" ng-click="tenantsCtrl.deleteItem(item)" title="Delete tenant"><i class="fa fa-fw fa-trash"></i></a></td></tr></tbody></table></div></div></div></div></div>'),e.put("app/remote_control/index.html",'<div id="wrapper" ng-init="remoteControlCtrl.initialize()"><div ng-include="\'app/components/navbar/navbar.html\'"></div><div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12"><h1 class="page-header">Remote control</h1></div></div><div class="row" data-ng-controller="RemoteControlCtrl"><div class="col-lg-4"><label for="device">Choose a device:</label><select id="device" data-ng-model="remoteControlCtrl.currentDevice" data-ng-options="c.name for c in remoteControlCtrl.devices"><option value="">Select device</option></select></div><div class="col-lg-8"><div ng-show="remoteControlCtrl.currentDevice.name != undefined">selected device: {{ remoteControlCtrl.currentDevice}}</div></div></div></div></div></div>'),e.put("app/components/navbar/navbar.html",'<nav class="navbar navbar-default navbar-fixed-top" role="navigation"><div class="navbar-header"><button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse"><span class="sr-only">Toggle navigation</span> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span></button> <a class="navbar-brand" href="/">SkyKit Display Provisioning</a></div><ul class="nav navbar-right top-nav"></ul><div class="collapse navbar-collapse navbar-ex1-collapse"><ul class="nav navbar-nav side-nav"><li><a id="navbar-tenants" href="#/tenants"><i class="fa fa-fw fa-users"></i> Tenants</a></li><li><a id="navbar-remote_control" href="#/remote_control"><i class="fa fa-fw fa-building"></i> Remote control</a></li></ul></div></nav>')}]);