(function () {


  let appModule = angular.module('skykitProvisioning');

  appModule.controller('TenantUnmanagedDevicesCtrl',
    function ($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) {
      let vm = this;
      vm.currentTenant = {
        key: undefined,
        name: undefined,
        tenant_code: undefined,
        admin_email: undefined,
        content_server_url: undefined,
        content_manager_base_url: undefined,
        domain_key: undefined,
        notification_emails: undefined,
        proof_of_play_logging: false,
        active: true
      };
      vm.gcmidDevices = [];
      vm.tenantDevices = [];
      vm.devicesPrev = null;
      vm.devicesNext = null;
      vm.selectedButton = "MAC";
      vm.serialDevices = {};
      vm.disabled = true;
      vm.macDevices = {};
      vm.editMode = !!$stateParams.tenantKey;
      vm.tenantKey = $stateParams.tenantKey;

      vm.getUnmanagedDevices = function (tenantKey, prev_cursor, next_cursor) {
        ProgressBarService.start();
        let devicesPromise = DevicesService.getUnmanagedDevicesByTenant(tenantKey, prev_cursor, next_cursor);
        return devicesPromise.then(function (data) {
          vm.devicesPrev = data["prev_cursor"];
          vm.devicesNext = data["next_cursor"];
          vm.tenantDevices = data["devices"];
          return ProgressBarService.complete();
        });
      };

      vm.refreshDevices = function () {
        vm.devicesPrev = null;
        vm.devicesNext = null;
        vm.tenantDevices = null;
        return vm.getUnmanagedDevices(vm.tenantKey, vm.devicesPrev, vm.devicesNext);
      };

      if (vm.editMode) {
        let tenantPromise = TenantsService.getTenantByKey(vm.tenantKey);
        tenantPromise.then(tenant => vm.currentTenant = tenant);
        vm.getUnmanagedDevices(vm.tenantKey, null, null);
      }

      $scope.tabIndex = 2;

      $scope.$watch('tabIndex', function (toTab, fromTab) {
        if (toTab !== undefined) {
          switch (toTab) {
            case 0:
              return $state.go('tenantDetails', {tenantKey: vm.tenantKey});
            case 1:
              return $state.go('tenantManagedDevices', {tenantKey: vm.tenantKey});
            case 2:
              return $state.go('tenantUnmanagedDevices', {tenantKey: vm.tenantKey});
            case 3:
              return $state.go('tenantLocations', {tenantKey: vm.tenantKey});
          }
        }
      });

      vm.editItem = item => $state.go('editDevice', {
        deviceKey: item.key,
        tenantKey: vm.tenantKey,
        fromDevices: false
      });

      // todo move this into a service
      vm.convertArrayToDictionary = function (theArray, mac, gcm) {
        let devices = {};
        for (let i = 0; i < theArray.length; i++) {
          let item = theArray[i];
          if (mac) {
            devices[item.mac] = item;
          } else if (gcm) {
            devices[item.gcmid] = item;
          } else {
            devices[item.serial] = item;
          }
        }

        return devices;
      };

      vm.changeRadio = function () {
        vm.searchText = '';
        vm.disabled = true;
        vm.serialDevices = {};
        return vm.macDevices = {};
      };


      vm.searchDevices = function (partial_search) {
        if (partial_search) {
          if (partial_search.length > 2) {
            if (vm.selectedButton === "Serial Number") {
              return DevicesService.searchDevicesByPartialSerialByTenant(vm.tenantKey, partial_search, true)
                .then(function (res) {
                  let result = res["matches"];
                  vm.serialDevices = vm.convertArrayToDictionary(result, false);

                  let deviceSerials = [];
                  for (let i = 0; i < result.length; i++) {
                    let each = result[i];
                    deviceSerials.push(each.serial);
                  }
                  return deviceSerials;
                });

            } else if (vm.selectedButton === "MAC") {
              return DevicesService.searchDevicesByPartialMacByTenant(vm.tenantKey, partial_search, true)
                .then(function (res) {
                  let result = res["matches"];
                  vm.macDevices = vm.convertArrayToDictionary(result, true);
                  let deviceMacs = [];
                  for (let i = 0; i < result.length; i++) {
                    let each = result[i];
                    deviceMacs.push(each.mac);
                  }
                  return deviceMacs;
                })
            } else {
              return DevicesService.searchDistributorDevicesByPartialGCMid(vm.tenantKey, partial_search, true)
                .then(function (res) {
                  let result = res["matches"];

                  vm.gcmidDevices = vm.convertArrayToDictionary(result, false, true);

                  let gcmidDevices = [];

                  for (let i = 0; i < result.length; i++) {
                    let each = result[i];
                    gcmidDevices.push(each.gcmid);
                  }

                  return gcmidDevices;
                });
            }

          } else {
            return [];
          }
        } else {
          return [];
        }
      };

      vm.paginateCall = function (forward) {
        if (forward) {
          return vm.getUnmanagedDevices(vm.tenantKey, null, vm.devicesNext);

        } else {
          return vm.getUnmanagedDevices(vm.tenantKey, vm.devicesPrev, null);
        }
      };


      vm.prepareForEditView = function (searchText) {
        let mac, serial, gcmid;

        mac = vm.selectedButton === "MAC";
        serial = vm.selectedButton === "Serial Number";
        gcmid = vm.selectedButton === "GCM ID"


        if (mac) {
          return vm.editItem(vm.macDevices[searchText]);
        } else if (serial) {
          return vm.editItem(vm.serialDevices[searchText]);
        } else {
          return vm.editItem(vm.gcmidDevices[searchText])
        }

      };


      vm.controlOpenButton = function (isMatch) {
        vm.disabled = !isMatch;
        return vm.loadingDisabled = false;
      };

      vm.isResourceValid = function (resource) {
        let mac, serial, gcmid;
        if (resource) {
          if (resource.length > 2) {
            mac = vm.selectedButton === "MAC";
            serial = vm.selectedButton === "Serial Number";
            gcmid = vm.selectedButton === "GCM ID";

            if (mac) {
              return DevicesService.matchDevicesByFullMacByTenant(vm.tenantKey, resource, true)
                .then(res => vm.controlOpenButton(res["is_match"]));

            } else if (serial) {
              return DevicesService.matchDevicesByFullSerialByTenant(vm.tenantKey, resource, true)
                .then(res => vm.controlOpenButton(res["is_match"]));
            } else {
              return DevicesService.matchDevicesByFullGCMid(vm.tenantKey, resource, true)
                .then(res => vm.controlOpenButton(res["is_match"]));
            }

          } else {
            return vm.controlOpenButton(false);
          }

        } else {
          return vm.controlOpenButton(false);
        }
      };

      return vm;
    });


})
();
